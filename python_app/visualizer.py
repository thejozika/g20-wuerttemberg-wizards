import io

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from python_app.data_loader import common_grid, modis_land_raster_datastruct, modis_gpp_datastruct, \
    climate_precipitation_datastruct, population_density_datastruct, glw_sheep_datastruct, glw_goat_datastruct, \
    glw_cattle_datastruct
from analytics import reproject_overlay


def replace_nodata_with_nan(array, nodata_val=65535.0):
    #return np.where(array >= 6500, np.nan, array) for the fucking other modis set
    return np.where(array == nodata_val, np.nan, array)


def visualize(data: np.array, meta: dict, year: int):
    data_nan = replace_nodata_with_nan(data, nodata_val=meta['nodata'])

    plt.figure(figsize=(10, 8))
    img = plt.imshow(data_nan, cmap='viridis')
    plt.title(f"Raster Visualization: {year}")
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.colorbar(img, label='Pixel Values')
    plt.show()


def visualize_land_cutout(lon1, lat1, lon2, lat2):
    """
    Perform the cutout and return a PNG bytes object.
    """
    data = modis_land_raster_datastruct.array
    meta = common_grid.copy()
    meta['dtype'] = modis_land_raster_datastruct.dtype
    meta['nodata'] = modis_land_raster_datastruct.nodata
    # Reproject overlay
    dst_array, dst_transform = reproject_overlay(
        data,
        meta,
        lon1, lat1, lon2, lat2,
        dst_width=854,
        dst_height=480
    )
    # Replace nodata
    data_nan = replace_nodata_with_nan(dst_array, nodata_val=meta['nodata'])

    # Define categorical classes (example)
    classes = {
        0:  ("Water", "#1f78b4"),
        1:  ("Evergreen Needleleaf Forest", "#33a02c"),
        2:  ("Evergreen Broadleaf Forest", "#b2df8a"),
        3:  ("Deciduous Needleleaf Forest", "#006400"),
        4:  ("Deciduous Broadleaf Forest", "#8dd3c7"),
        5:  ("Mixed Forest", "#ffffb3"),
        6:  ("Closed Shrublands", "#8B4513"),
        7:  ("Open Shrublands", "#bc8f8f"),
        8:  ("Woody Savannas", "#d9d9d9"),
        9:  ("Savannas", "#fdbf6f"),
        10: ("Grasslands", "#55FF55"),
        11: ("Permanent Wetlands", "#1ecbe1"),
        12: ("Croplands", "#00FFFF"),
        13: ("Urban and Built-Up Lands", "#FF0000"),
        14: ("Cropland/Natural Vegetation", "#00FFFF"),
        15: ("Snow and Ice", "#ffffff"),
        16: ("Barren or sparsely vegetated", "#FFFFAA"),
        17: ("Fill Value/Unclassified", "#000000")
    }

    sorted_keys = sorted(classes.keys())
    color_list = [classes[k][1] for k in sorted_keys]
    label_list = [classes[k][0] for k in sorted_keys]

    cmap = mcolors.ListedColormap(color_list, name='LandCoverMap')
    boundaries = sorted_keys + [max(sorted_keys) + 1]
    norm = mcolors.BoundaryNorm(boundaries, cmap.N)

    # Create figure in memory
    fig, ax = plt.subplots(figsize=(8, 6))
    img = ax.imshow(data_nan, cmap=cmap, norm=norm)
    ax.set_title("Land Cover Cutout")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Rows")

    cbar = plt.colorbar(img, ax=ax, ticks=[k + 0.5 for k in sorted_keys])
    cbar.ax.set_yticklabels(label_list)

    # Save to in-memory buffer
    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png', bbox_inches='tight')
    plt.close(fig)  # Close the figure

    # Rewind the BytesIO buffer
    png_bytes.seek(0)
    return png_bytes