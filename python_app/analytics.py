import numpy as np
from pyproj import Transformer
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling

from python_app.data_loader import common_grid


def reproject_overlay(src_array,lon_1,lat_1,lon_2,lat_2, dst_width=854, dst_height=480):
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
