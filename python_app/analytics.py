import numpy as np
from scipy.ndimage import convolve
from pyproj import Transformer
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling

from python_app.data_loader import common_grid,population_density_datastruct,modis_land_raster_datastruct

def reproject_overlay(src_array, lon_1, lat_1, lon_2, lat_2, dst_width=854, dst_height=480):
    src_crs = common_grid["crs"]
    src_transform = common_grid["transform"]
    transformer = Transformer.from_crs("EPSG:4326", src_crs, always_xy=True)

    # Transform to sinusoidal:
    x1, y1 = transformer.transform(lon_1, lat_1)
    x2, y2 = transformer.transform(lon_2, lat_2)

    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    # Initialize an array for the destination raster
    subset_transform = from_bounds(min_x, min_y, max_x, max_y, dst_width, dst_height)
    dst_array = np.empty((dst_height, dst_width), dtype=src_array.dtype)

    # Reproject the source array into the destination array.
    reproject(
        source=src_array,
        destination=dst_array,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_transform=subset_transform,
        dst_crs=src_crs,  # Change this if your destination CRS is different.
        resampling=Resampling.nearest  # Choose an appropriate resampling method.
    )

    return dst_array, subset_transform


def reproject_overlay_cubic(src_array, lon_1, lat_1, lon_2, lat_2, dst_width=854, dst_height=480):
    src_crs = common_grid["crs"]
    src_transform = common_grid["transform"]
    transformer = Transformer.from_crs("EPSG:4326", src_crs, always_xy=True)

    # Transform to sinusoidal:
    x1, y1 = transformer.transform(lon_1, lat_1)
    x2, y2 = transformer.transform(lon_2, lat_2)

    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    # Initialize an array for the destination raster
    subset_transform = from_bounds(min_x, min_y, max_x, max_y, dst_width, dst_height)
    dst_array = np.empty((dst_height, dst_width), dtype=src_array.dtype)

    # Reproject the source array into the destination array.
    reproject(
        source=src_array,
        destination=dst_array,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_transform=subset_transform,
        dst_crs=src_crs,  # Change this if your destination CRS is different.
        resampling=Resampling.cubic  # Choose an appropriate resampling method.
    )

    return dst_array, subset_transform


def map_land(array):
    mapped_arr = array.copy().astype("float32")
    # Now apply your custom mappings
    mapped_arr[array == 7] = 1
    mapped_arr[array == 10] = 2
    # Set 12, 13, 16 explicitly to 0
    mapped_arr[np.isin(array, [12, 13, 16])] = 0
    mapped_arr[array == 255] = np.nan
    return mapped_arr


def map_pop(array):
    cutout = np.where(array == 65535.0, np.nan, array)
    return np.where(cutout >= 60000, 0, cutout)




def analyze_correlation(past_1, future_1, past_2, future_2):
    kernel = np.array([
        [0.5, 1, 0.5],
        [1, 3, 1],
        [0.5, 1, 0.5]
    ])
    normalized_kernel = kernel / kernel.sum()

    # Apply convolution
    past_1_conv = convolve(past_1, normalized_kernel, mode='constant', cval=0)
    future_1_conv = convolve(future_1, normalized_kernel, mode='constant', cval=0)
    past_2_conv = convolve(past_2, normalized_kernel, mode='constant', cval=0)
    future_2_conv = convolve(future_2, normalized_kernel, mode='constant', cval=0)

    # Calculate relative changes, normalized by maximum absolute difference
    change_1 = future_1_conv - past_1_conv
    change_2 = future_2_conv - past_2_conv

    max_abs_1 = np.max(np.abs(change_1)) + 1e-8
    max_abs_2 = np.max(np.abs(change_2)) + 1e-8

    relative_change_1 = np.clip(change_1 / max_abs_1, -1, 1)
    relative_change_2 = np.clip(change_2 / max_abs_2, -1, 1)

    # Multiply matrices element-wise and calculate anti-correlation
    anti_correlation = (1 - (relative_change_1 * relative_change_2)) / 2
    return anti_correlation

maped_pop_1 = map_pop(population_density_datastruct.array[0])
maped_pop_2 = map_pop(population_density_datastruct.array[-1])
maped_land_1 = map_land(modis_land_raster_datastruct.array[0])
maped_land_2 = map_land(modis_land_raster_datastruct.array[-1])
analytics_data = np.nan_to_num(analyze_correlation(maped_pop_1,maped_pop_2,maped_land_1,maped_land_2),nan=0)

print('analytics data calculated')