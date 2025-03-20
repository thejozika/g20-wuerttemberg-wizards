import os
import glob
import re
import geopandas as gpd
import rasterio
from typing import TypedDict, Dict, Literal

from contourpy.util import data


def load_vector_dataset(dataset_path: str) -> dict:
    """
    Load all shapefiles in the given dataset folder.
    Returns a dict mapping the base name of the shapefile to its GeoDataFrame.
    """
    vector_layers = {}
    shp_files = glob.glob(os.path.join(dataset_path, "*.shp"))
    for shp in shp_files:
        layer_name = os.path.splitext(os.path.basename(shp))[0]
        try:
            gdf = gpd.read_file(shp)
            vector_layers[layer_name] = gdf
        except Exception as e:
            print(f"Error loading shapefile {shp}: {e}")
    return vector_layers


def load_raster_dataset(dataset_path: str) -> dict:
    """
    Load all raster files in the given dataset folder.
    Instead of vectorizing, this function loads the raster as an array with metadata.
    Returns a dict mapping the base name of the raster to a dictionary with keys 'array' and 'meta'.
    """
    raster_layers = {}
    tif_files = glob.glob(os.path.join(dataset_path, "*.tif"))
    for tif in tif_files:
        base_name = os.path.splitext(os.path.basename(tif))[0]
        try:
            with rasterio.open(tif) as src:
                array = src.read(1)  # read the first band
                meta = src.meta
            raster_layers[base_name] = {"array": array, "meta": meta}
        except Exception as e:
            print(f"Error loading raster {tif}: {e}")
    return raster_layers


def load_raster_set(path: str) -> dict:
    data = {}
    try:
        with rasterio.open(path) as src:
            data["array"] = src.read(1)  # Read the first band as an array
            data["meta"] = src.meta  # Get metadata such as transform, crs, etc.
    except Exception as e:
        print(f"Error loading raster {path}: {e}")
    return data


def load_all_datasets(base_dir: str = "./datasets") -> dict:
    """
    Walk through the top-level datasets folder and load each sub-folder.

    For each sub-folder:
      - If it contains shapefiles (.shp), load it as a vector dataset.
      - If it contains TIFF files (.tif), load it as a raster dataset (without vectorizing).

    Returns a dictionary mapping dataset names (folder names) to their loaded data.
    """
    datasets = {}
    for dataset_name in os.listdir(base_dir):
        dataset_path = os.path.join(base_dir, dataset_name)
        if os.path.isdir(dataset_path):
            shp_files = glob.glob(os.path.join(dataset_path, "*.shp"))
            if shp_files:
                print(f"Loading vector dataset: {dataset_name}")
                datasets[dataset_name] = load_vector_dataset(dataset_path)
            else:
                tif_files = glob.glob(os.path.join(dataset_path, "*.tif"))
                if tif_files:
                    print(f"Loading raster dataset: {dataset_name}")
                    datasets[dataset_name] = load_raster_dataset(dataset_path)
                else:
                    print(f"No recognized data found in {dataset_name}")
    return datasets


# Define a literal type for the years
TimeSeriesYears = Literal[
    "2010", "2011", "2012", "2013", "2014", "2015",
    "2016", "2017", "2018", "2019", "2020", "2021",
    "2022", "2023"
]

# Define the time series dataset type as a dictionary with those keys
TimeSeriesDataset = Dict[TimeSeriesYears, object]  # object shall be raster dict


# You may have other typed structures; adjust these as needed.
class DataStructure:
    land_cover: TimeSeriesDataset  #Modis_Land_Cover_Data
    precipitation: TimeSeriesDataset  #Climate_Precipitation_Data
    gpp: TimeSeriesDataset  #MODIS_Gross_Primary_Production
    population_density_assaba: TimeSeriesDataset  #Gridded_Population_Density_Data - mrt_pd_2005_1km
    population_density_mrt: TimeSeriesDataset  #Gridded_Population_Density_Data - mrt_pd_2005_1km
    streamwater: gpd.GeoDataFrame  #Streamwater_Line_Road_Network - Streamwater
    main_road: gpd.GeoDataFrame  #Streamwater_Line_Road_Network - Main_Road
    assaba_region: gpd.GeoDataFrame  #Admin_layers - Assaba_Region_Layers
    assaba_district: gpd.GeoDataFrame  #Admin_layers - Assaba_District_Layers


def build_typed_structure(all_data: dict) -> DataStructure:
    """
    Build a structured data dictionary from all_data.

    For time series datasets (land_cover, precipitation, gpp), we assume that
    the data are provided with keys that include a year, possibly with extra suffix.

    For population density datasets, the raw data only exist for a subset of years
    (e.g., 2010, 2015, and 2020). For the missing years in our target range (2010-2023),
    a linear interpolation (or extrapolation) is performed on the underlying arrays.

    For vector layers, we assume that they are stored in the all_data dictionary
    under specific keys.
    """
    # Define the target years as integers (based on our TimeSeriesYears literal)
    target_years = [int(y) for y in ["2010", "2011", "2012", "2013", "2014", "2015",
                                     "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]]

    def clean_keys_time_series(raw_data: dict) -> dict:
        """
        For each key in raw_data, extract the 4-digit year using regex.
        This handles keys that may have additional suffixes after the year.
        Returns a new dictionary with keys as year strings and the associated value.
        """
        cleaned = {}
        for key, value in raw_data.items():
            match = re.search(r"(\d{4})", key)
            if match:
                year = match.group(1)
                cleaned[year] = value
        return cleaned

    # Process land cover data by cleaning its keys.
    raw_land_cover = all_data.get("Modis_Land_Cover_Data", {})
    land_cover = clean_keys_time_series(raw_land_cover)

    # For precipitation and GPP we assume the keys are already pure years.
    precipitation = all_data.get("Climate_Precipitation_Data", {})
    gpp = all_data.get("MODIS_Gross_Primary_Production", {})

    def interpolate_time_series(raw_data: dict) -> dict:
        """
        Given raw_data with keys as available years (as strings) and values as raster dicts,
        perform linear interpolation (or extrapolation) to generate data for every target year.
        Returns a dictionary mapping target years (as strings) to interpolated raster dicts.
        """
        # Convert available keys to integers.
        available = {}
        for key, value in raw_data.items():
            try:
                yr = int(key)
                available[yr] = value
            except ValueError:
                continue
        if not available:
            return {}
        available_years = sorted(available.keys())
        result = {}
        for ty in target_years:
            if ty in available:
                # Exact match available.
                result[str(ty)] = available[ty]
            elif ty < available_years[0]:
                # Extrapolate backwards using the first two available years.
                y0, y1 = available_years[0], available_years[1] if len(available_years) > 1 else (
                    available_years[0], available_years[0])
                data0 = available[y0]["array"]
                data1 = available[y1]["array"]
                slope = (data1 - data0) / (y1 - y0)
                interp_array = data0 + slope * (ty - y0)
                result[str(ty)] = {"array": interp_array, "meta": available[y0]["meta"]}
            elif ty > available_years[-1]:
                # Extrapolate forwards using the last two available years.
                if len(available_years) > 1:
                    y0, y1 = available_years[-2], available_years[-1]
                else:
                    y0, y1 = available_years[-1], available_years[-1]
                data0 = available[y0]["array"]
                data1 = available[y1]["array"]
                slope = (data1 - data0) / (y1 - y0)
                interp_array = data1 + slope * (ty - y1)
                result[str(ty)] = {"array": interp_array, "meta": available[y1]["meta"]}
            else:
                # Find the two available years that bracket the target year.
                for i in range(len(available_years) - 1):
                    y0 = available_years[i]
                    y1 = available_years[i + 1]
                    if y0 < ty < y1:
                        data0 = available[y0]["array"]
                        data1 = available[y1]["array"]
                        fraction = (ty - y0) / (y1 - y0)
                        interp_array = data0 + (data1 - data0) * fraction
                        # Using meta from the earlier year (assuming meta remains similar)
                        result[str(ty)] = {"array": interp_array, "meta": available[y0]["meta"]}
                        break
        return result

    # Process the population density datasets.
    # We assume that the raw population density data for each region is stored under these keys.
    pop_assaba_raw = all_data.get("Gridded_Population_Density_Assaba", {})
    pop_mrt_raw = all_data.get("Gridded_Population_Density_MRT", {})

    population_density_assaba = interpolate_time_series(pop_assaba_raw)
    population_density_mrt = interpolate_time_series(pop_mrt_raw)

    # Extract vector datasets.
    # For the streamwater and main road layers, assume they are in a dataset named "Streamwater_Line_Road_Network".
    streamwater = None
    main_road = None
    if "Streamwater_Line_Road_Network" in all_data:
        vector_data = all_data["Streamwater_Line_Road_Network"]
        streamwater = vector_data.get("Streamwater", None)
        main_road = vector_data.get("Main_Road", None)

    # For the administrative layers, assume they are in a dataset named "Admin_layers".
    assaba_region = None
    assaba_district = None
    if "Admin_layers" in all_data:
        admin_data = all_data["Admin_layers"]
        assaba_region = admin_data.get("Assaba_Region_layer", None)
        assaba_district = admin_data.get("Assaba_District_layer", None)

    return DataStructure(
        land_cover=land_cover,
        precipitation=precipitation,
        gpp=gpp,
        population_density_assaba=population_density_assaba,
        population_density_mrt=population_density_mrt,
        streamwater=streamwater,
        main_road=main_road,
        assaba_region=assaba_region,
        assaba_district=assaba_district
    )



def get_strucured_data() -> DataStructure:
    # Adjust the base_dir as needed
    base_dir = "../datasets"
    all_data = load_all_datasets(base_dir)
    return  build_typed_structure(all_data)
