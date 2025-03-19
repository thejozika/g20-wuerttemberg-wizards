import os
import glob
import geopandas as gpd
import rasterio
import rasterio.features
from shapely.geometry import shape, box


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


def vectorize_raster(raster_path: str) -> gpd.GeoDataFrame:
    """
    Open a raster file, read the first band, and vectorize it into polygons.
    The resulting GeoDataFrame will have a 'value' column containing the pixel value.
    """
    features = []
    try:
        with rasterio.open(raster_path) as src:
            band = src.read(1)  # read the first band
            # Create a mask if your raster has a defined nodata value
            mask = band != src.nodata if src.nodata is not None else None
            # Extract shapes and corresponding values
            for geom, value in rasterio.features.shapes(band, mask=mask, transform=src.transform):
                features.append({"geometry": shape(geom), "value": value})
            crs = src.crs
    except Exception as e:
        print(f"Error vectorizing raster {raster_path}: {e}")
        return gpd.GeoDataFrame()  # return empty GeoDataFrame in case of error

    return gpd.GeoDataFrame(features, crs=crs)


def load_raster_dataset(dataset_path: str) -> dict:
    """
    Load all raster files in the given dataset folder, vectorize each raster,
    and return a dict mapping a base name (e.g., '2010R') to its vectorized GeoDataFrame.
    """
    raster_layers = {}
    tif_files = glob.glob(os.path.join(dataset_path, "*.tif"))
    for tif in tif_files:
        base_name = os.path.splitext(os.path.basename(tif))[0]
        try:
            vectorized_gdf = vectorize_raster(tif)
            raster_layers[base_name] = vectorized_gdf
        except Exception as e:
            print(f"Error loading raster {tif}: {e}")
    return raster_layers


def load_all_datasets(base_dir: str = "./datasets") -> dict:
    """
    Walk through the top-level datasets folder and load each sub-folder.

    For each sub-folder:
      - If it contains shapefiles (.shp), load it as a vector dataset.
      - If it contains TIFF files (.tif), load it as a raster dataset and vectorize it.

    Returns a dictionary mapping dataset names (folder names) to their loaded data.
    """
    datasets = {}
    # List sub-folders in the base_dir
    for dataset_name in os.listdir(base_dir):
        dataset_path = os.path.join(base_dir, dataset_name)
        if os.path.isdir(dataset_path):
            # Try loading as vector data first
            shp_files = glob.glob(os.path.join(dataset_path, "*.shp"))
            if shp_files:
                print(f"Loading vector dataset: {dataset_name}")
                datasets[dataset_name] = load_vector_dataset(dataset_path)
            else:
                # If no shapefiles, look for rasttt()er files
                tif_files = glob.glob(os.path.join(dataset_path, "*.tif"))
                if tif_files:
                    print(f"Loading raster dataset (vectorized): {dataset_name}")
                    datasets[dataset_name] = load_raster_dataset(dataset_path)
                else:
                    print(f"No recognized data found in {dataset_name}")
    return datasets


# Example usage:
if __name__ == "__main__":
    all_data = load_all_datasets("../datasets")
    # Print a summary of loaded datasets
    for name, data in all_data.items():
        print(f"Dataset: {name}")
        if isinstance(data, dict):
            for layer, content in data.items():
                if isinstance(content, gpd.GeoDataFrame):
                    print(f"  Layer: {layer}, {len(content)} features, CRS: {content.crs}")
                else:
                    print(f"  Unknown format for layer: {layer}")
        else:
            print("  Unknown data format")
