import math
import os
import glob
import re
from typing import Union

import geopandas as gpd
import numpy as np
import rasterio
from affine import Affine
from rasterio import CRS
from rasterio.enums import Resampling
from rasterio.warp import reproject, calculate_default_transform


def load_vector_dataset(shp_path_name: str) -> gpd.GeoDataFrame:
    """
    Load all shapefiles in the given dataset folder.
    Returns a dict mapping the base name of the shapefile to its GeoDataFrame.
    """
    try:
        gdf = gpd.read_file(shp_path_name)
    except Exception as e:
        print(f"Error loading shapefile {shp_path_name}:")
    return gdf


#ALL dataset have only one band
def load_and_convert_raster_dataset(dataset_path: str) -> dict:
    raster_layers = {}
    tif_files = glob.glob(os.path.join(dataset_path, "*.tif"))
    for tif in tif_files:
        base_name = os.path.splitext(os.path.basename(tif))[0]
        try:
            with rasterio.open(tif) as src:
                array = src.read(1)
                meta = src.meta.copy()
            raster_layers[base_name] = {"array": array, "meta": meta}
        except Exception as e:
            print(f"Error loading raster {tif}: {e}")
    return raster_layers


def load_and_convert_raster_dataset_as_f32(dataset_path: str) -> dict:
    raster_layers = {}
    tif_files = glob.glob(os.path.join(dataset_path, "*.tif"))
    for tif in tif_files:
        base_name = os.path.splitext(os.path.basename(tif))[0]
        try:
            with rasterio.open(tif) as src:
                array = src.read(1).astype(np.float32)
                meta = src.meta.copy()
                meta.update(dtype="float32")
            raster_layers[base_name] = {"array": array, "meta": meta}
        except Exception as e:
            print(f"Error loading raster {tif}: {e}")
    return raster_layers


def check_important_meta_consistency(raster_layers: dict, keys=["crs", "transform", "width", "height"],
                                     eps=1e-9) -> bool:
    """
    Check if the important metadata are consistent across all raster files.
    Only the keys provided in 'keys' will be compared.

    'eps' sets the floating-point tolerance when comparing transform parameters.

    Parameters
    ----------
    raster_layers : dict
        A dict mapping raster names to their data and metadata.
    keys : list of str
        The metadata keys to compare.
    eps : float
        Tolerance for comparing floating-point transform parameters.

    Returns
    -------
    bool
        True if all files have the same important metadata, False otherwise.
    """
    if not raster_layers:
        print("No raster files loaded.")
        return True

    # --- Helper to build a standardized dict that allows "fuzzy" compare for float transforms. ---
    def standardize(meta):
        std = {}
        for k in keys:
            if k not in meta:
                continue
            value = meta[k]
            if k == "crs" and value is not None:
                # Convert CRS to its WKT string for comparison
                # (assuming value is already a rasterio CRS object or WKT string)
                # If it's a rasterio CRS, you might do: value = value.to_wkt()
                # If it's already a string, that might be enough
                if hasattr(value, "to_wkt"):
                    value = value.to_wkt()
                std[k] = value
            elif k == "transform" and value is not None:
                # Convert transform to a tuple of floats
                # We'll store them as-is (floats), but we won't directly
                # compare them as `==` later; we do a tolerance check
                std[k] = tuple(value)
            else:
                # width, height, or other keys can be used as-is
                std[k] = value
        return std

    # Get the first raster's metadata to compare against
    first_name, first_data = next(iter(raster_layers.items()))
    ref_meta = standardize(first_data["meta"])

    # --- Now check each subsequent raster ---
    for name, data in raster_layers.items():
        curr_meta = standardize(data["meta"])
        if not _compare_meta_dicts(ref_meta, curr_meta, eps=eps):
            print(f"Inconsistent metadata found in file: {name}")
            print("Reference:", ref_meta)
            print("Current  :", curr_meta)
            return False

    print("All important metadata are consistent.")
    return True


def _compare_meta_dicts(ref_meta, curr_meta, eps=1e-9) -> bool:
    """
    Compare two standardized metadata dicts with possible float transforms.
    Returns True if they are effectively the same within tolerance.
    """
    # Check that they have the same keys
    if ref_meta.keys() != curr_meta.keys():
        return False

    # Compare values
    for k in ref_meta:
        ref_val = ref_meta[k]
        curr_val = curr_meta[k]

        # If either is None, direct compare
        if ref_val is None or curr_val is None:
            if ref_val != curr_val:
                return False

        # For the transform, compare float-by-float with tolerance
        elif k == "transform":
            if len(ref_val) != len(curr_val):
                return False
            for rv, cv in zip(ref_val, curr_val):
                if not math.isclose(rv, cv, abs_tol=eps):
                    return False

        # For the CRS (strings) or for width/height (ints), direct compare
        else:
            if ref_val != curr_val:
                return False

    return True


common_grid = {
    "driver": "GTiff",
    "dtype": "float32",
    "nodata": 65535.0,
    "width": 565,
    "height": 769,
    "count": 1,
    "crs": CRS.from_wkt(
        'PROJCS["unnamed",GEOGCS["GCS_Unknown_datum_based_upon_the_custom_spheroid",'
        'DATUM["D_Not_specified_based_on_custom_spheroid",'
        'SPHEROID["Custom_spheroid",6371007.181,0]],'
        'PRIMEM["Greenwich",0],'
        'UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],'
        'PROJECTION["Sinusoidal"],'
        'PARAMETER["longitude_of_center",0],'
        'PARAMETER["false_easting",0],'
        'PARAMETER["false_northing",0],'
        'UNIT["metre",1,AUTHORITY["EPSG","9001"]],'
        'AXIS["Easting",EAST],'
        'AXIS["Northing",NORTH]]'
    ),
    "transform": Affine(463.31271652749996, 0.0, -1378818.64438684,
                        0.0, -463.31271652749996, 2036259.3891393621)
}


def reproject_raster_layer_to_common_grid(src_array, src_meta, resampling_method=Resampling.nearest):
    """
    Reproject a raster layer onto a common grid defined by common_grid.

    Parameters:
      - src_array: Source numpy array.
      - src_meta: Source metadata dictionary.
      - common_grid: Dictionary containing target grid parameters (width, height, transform, crs, nodata).
      - resampling_method: Resampling method to use.

    Returns:
      - dst_array: Reprojected numpy array on the common grid.
      - dst_meta: Updated metadata dictionary with common grid settings.
    """

    target_crs = common_grid["crs"]
    transform = common_grid["transform"]
    width = common_grid["width"]
    height = common_grid["height"]
    dst_nodata = common_grid.get("nodata", np.nan)

    # Create a new metadata dictionary based on the common grid.
    dst_meta = src_meta.copy()
    dst_meta.update({
        "crs": target_crs,
        "transform": transform,
        "width": width,
        "height": height,
        "nodata": dst_nodata
    })

    # Prepare an empty destination array filled with the nodata value.
    dst_array = np.empty((height, width), dtype=src_array.dtype)
    dst_array.fill(dst_nodata)

    # Perform the reprojection onto the common grid.
    reproject(
        source=src_array,
        destination=dst_array,
        src_transform=src_meta["transform"],
        src_crs=src_meta["crs"],
        dst_transform=transform,
        dst_crs=target_crs,
        resampling=resampling_method,
        src_nodata=src_meta.get("nodata"),
        dst_nodata=dst_nodata
    )

    return dst_array, dst_meta


def convert_all_raster_layers_to_common_grid(raster_layers: dict, resampling_method=Resampling.cubic) -> dict:
    """
    Reproject all raster layers onto a common grid.

    Returns:
      - A new dictionary with reprojected raster arrays and updated metadata.
    """
    new_layers = {}
    for name, data in raster_layers.items():
        src_array = data["array"]
        src_meta = data["meta"]
        dst_array, dst_meta = reproject_raster_layer_to_common_grid(src_array, src_meta, resampling_method)
        new_layers[name] = {"array": dst_array, "meta": dst_meta}
    return new_layers


class DataStruct:
    nodata: Union[int, float]
    array: np.ndarray
    dtype: np.dtype

    def __init__(self, nodata: Union[int, float], array: np.ndarray, dtype: np.dtype):
        self.nodata = nodata
        self.array = array
        self.dtype = dtype


def extract_year_from_key(key: str) -> int:
    """
    Extract a 4-digit year from a string such as 'Assaba_Pop_2010.tif' or '2010R.tif'.
    Raises ValueError if no valid year is found.
    """
    match = re.search(r'(\d{4})', key)
    if not match:
        raise ValueError(f"Could not find a 4-digit year in the key: {key}")
    return int(match.group(1))


def convert_standard_set(data: dict) -> DataStruct:
    sorted_years = sorted(data.keys())
    first_year = sorted_years[0]
    nodata = data[first_year]['meta']['nodata']
    dtype = data[first_year]['meta']['dtype']

    # Dynamically sort keys to ensure chronological order
    arrays = []
    for year in sorted(data.keys()):
        arrays.append(data[year]['array'])
    #Stack arrays along a new axis (0) to create a 3D array [year, rows, columns]
    stacked_array = np.stack(arrays, axis=0)
    return DataStruct(nodata, stacked_array, dtype)


def convert_modis_land_cover(data: dict) -> DataStruct:
    sorted_years = sorted(data.keys())
    first_year = sorted_years[0]
    first_array = data[first_year]['array']
    first_array_uint8 = np.where(first_array == -128, 255, first_array).astype(np.uint8)

    # Dynamically sort keys to ensure chronological order
    arrays = [first_array_uint8]
    for year in sorted_years[1:]:
        arrays.append(data[year]['array'])
    # Stack arrays along a new axis (0) to create a 3D array [year, rows, columns]
    stacked_array = np.stack(arrays, axis=0)

    # Now the unified nodata is 255
    return DataStruct(nodata=255, array=stacked_array, dtype=np.uint8)


def convert_standard_set_with_interpolation(
        data: dict,
        start_year: int = 2010,
        end_year: int = 2023
) -> DataStruct:
    """
    Given a dictionary with string keys (e.g., 'Assaba_Pop_2010.tif'),
    parse out the year, linearly interpolate missing years, and
    return a DataStruct with a year-by-year stack from start_year to end_year.
    """
    year_dict = {}
    for key, value in data.items():
        year = extract_year_from_key(key)
        year_dict[year] = value

    sorted_years = sorted(year_dict.keys())

    nodata = year_dict[sorted_years[0]]['meta']['nodata']
    dtype = year_dict[sorted_years[0]]['meta']['dtype']

    def get_array_for_year(y: int) -> np.ndarray:
        if y in year_dict:
            # Exact data for this year
            return year_dict[y]['array']
        if y < sorted_years[0]:
            y1, y2 = sorted_years[0], sorted_years[1]
            arr1, arr2 = year_dict[y1]['array'], year_dict[y2]['array']
            ratio = (y - y1) / (y2 - y1)  # will be negative
            return arr1 + ratio * (arr2 - arr1)

        if y > sorted_years[-1]:
            y1, y2 = sorted_years[-2], sorted_years[-1]
            arr1, arr2 = year_dict[y1]['array'], year_dict[y2]['array']
            ratio = (y - y1) / (y2 - y1)
            return arr2 + ratio * (arr2 - arr1)

        for i in range(1, len(sorted_years)):
            if sorted_years[i] > y:
                y1, y2 = sorted_years[i - 1], sorted_years[i]
                arr1, arr2 = year_dict[y1]['array'], year_dict[y2]['array']
                ratio = (y - y1) / (y2 - y1)
                return arr1 + ratio * (arr2 - arr1)

        return year_dict[sorted_years[-1]]['array']

    yearly_arrays = []
    for y in range(start_year, end_year + 1):
        arr = get_array_for_year(y)
        yearly_arrays.append(arr)
    stacked_array = np.stack(yearly_arrays, axis=0)

    return DataStruct(nodata=nodata, array=stacked_array, dtype=dtype)


modis_land_dataset_path = "./python_app/datasets/Modis_Land_Cover_Data"
modis_land_raster_layers = load_and_convert_raster_dataset(modis_land_dataset_path)
check_important_meta_consistency(modis_land_raster_layers)
modis_land_raster_datastruct = convert_modis_land_cover(modis_land_raster_layers)

modis_mask = (modis_land_raster_datastruct.array == 255)


modis_gpp_dataset_path = "./python_app/datasets/MODIS_Gross_Primary_Production_GPP"
modis_gpp_raster_layers = load_and_convert_raster_dataset_as_f32(modis_gpp_dataset_path)
check_important_meta_consistency(modis_gpp_raster_layers)
modis_gpp_datastruct = convert_standard_set(modis_gpp_raster_layers)

climate_precipitation_dataset_path = "./python_app/datasets/Climate_Precipitation_Data"
climate_precipitation_raster_layers = convert_all_raster_layers_to_common_grid(
    load_and_convert_raster_dataset(climate_precipitation_dataset_path))
check_important_meta_consistency(climate_precipitation_raster_layers)
climate_precipitation_datastruct = convert_standard_set(climate_precipitation_raster_layers)

population_density_dataset_path = "./python_app/datasets/Gridded_Population_Density_Data"
population_density_raster_layers = convert_all_raster_layers_to_common_grid(
    load_and_convert_raster_dataset(population_density_dataset_path))
check_important_meta_consistency(population_density_raster_layers)
population_density_datastruct = convert_standard_set_with_interpolation(population_density_raster_layers)

glw_sheep_dataset_path = "./python_app/datasets/GLW_Sheep"
glw_sheep_raster_layers = convert_all_raster_layers_to_common_grid(
    load_and_convert_raster_dataset(glw_sheep_dataset_path))
check_important_meta_consistency(glw_sheep_raster_layers)
glw_sheep_datastruct = convert_standard_set_with_interpolation(glw_sheep_raster_layers)
sheep_default_value = glw_sheep_datastruct.nodata
glw_sheep_datastruct.array[modis_mask] = sheep_default_value

glw_goat_dataset_path = "./python_app/datasets/GLW_Goats"
glw_goat_raster_layers = convert_all_raster_layers_to_common_grid(
    load_and_convert_raster_dataset(glw_goat_dataset_path))
check_important_meta_consistency(glw_goat_raster_layers)
glw_goat_datastruct = convert_standard_set_with_interpolation(glw_goat_raster_layers)

glw_cattle_dataset_path = "./python_app/datasets/GLW_Cattle"
glw_cattle_raster_layers = convert_all_raster_layers_to_common_grid(
    load_and_convert_raster_dataset(glw_cattle_dataset_path))
check_important_meta_consistency(glw_cattle_raster_layers)
glw_cattle_datastruct = convert_standard_set_with_interpolation(glw_cattle_raster_layers)

#print(dl.modis_land_raster_layers['2010LCT']["meta"])
