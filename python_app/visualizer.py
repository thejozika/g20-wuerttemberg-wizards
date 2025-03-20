import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from python_app.data_loader import common_grid, modis_land_raster_datastruct, modis_gpp_datastruct, \
    climate_precipitation_datastruct, population_density_datastruct, glw_sheep_datastruct, glw_goat_datastruct, \
    glw_cattle_datastruct
from python_app.analytics import reproject_overlay, analytics_data


def replace_nodata_with_nan(array, nodata_val=65535.0):
    #return  for the fucking other modis set
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


def visualize_analytics_cutout(lon1, lat1, lon2, lat2, year=0):
    data = analytics_data
    max_val = np.nanmax(data)
    # Reproject overlay
    dst_array, dst_transform = reproject_overlay(
        data,
        lon1, lat1, lon2, lat2
    )
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(dst_array, cmap='plasma', vmax=max_val)
    ax.set_axis_off()  # Remove axes, ticks, labels

    # Save to in-memory buffer with no extra margins
    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    # Rewind the BytesIO buffer
    png_bytes.seek(0)
    return png_bytes

def visualize_gpp_cutout(lon1, lat1, lon2, lat2, year=0):
    data = modis_gpp_datastruct.array
    meta = common_grid.copy()
    meta['dtype'] = modis_gpp_datastruct.dtype
    meta['nodata'] = modis_gpp_datastruct.nodata
    data_nan = np.where(data >= 6500, np.nan, data)
    max_val = np.nanmax(data_nan)
    # Reproject overlay
    dst_array, dst_transform = reproject_overlay(
        data_nan[year],
        lon1, lat1, lon2, lat2
    )
    # Replace nodata

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(dst_array, cmap='BuGn', vmax=max_val)
    ax.set_axis_off()  # Remove axes, ticks, labels

    # Save to in-memory buffer with no extra margins
    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    # Rewind the BytesIO buffer
    png_bytes.seek(0)
    return png_bytes


def visualize_land_cutout(lon1, lat1, lon2, lat2, year=0):
    """
    Perform the cutout and return a PNG bytes object, with only the image shown.
    """
    data = modis_land_raster_datastruct.array
    meta = common_grid.copy()
    meta['dtype'] = modis_land_raster_datastruct.dtype
    meta['nodata'] = modis_land_raster_datastruct.nodata

    # Reproject overlay
    dst_array, dst_transform = reproject_overlay(
        data[year],
        lon1, lat1, lon2, lat2,
    )
    # Replace nodata
    data_nan = replace_nodata_with_nan(dst_array, nodata_val=meta['nodata'])
    meta['transform'] = dst_transform

    # Define categorical classes (example)
    classes = {
        0: ("Water", "#1f78b4"),
        1: ("Evergreen Needleleaf Forest", "#33a02c"),
        2: ("Evergreen Broadleaf Forest", "#b2df8a"),
        3: ("Deciduous Needleleaf Forest", "#006400"),
        4: ("Deciduous Broadleaf Forest", "#8dd3c7"),
        5: ("Mixed Forest", "#ffffb3"),
        6: ("Closed Shrublands", "#8B4513"),
        7: ("Open Shrublands", "#bc8f8f"),
        8: ("Woody Savannas", "#d9d9d9"),
        9: ("Savannas", "#fdbf6f"),
        10: ("Grasslands", "#55FF55"),
        11: ("Permanent Wetlands", "#1ecbe1"),
        12: ("Croplands", "#00FFFF"),
        13: ("Urban and Built-Up Lands", "#FF0000"),
        14: ("Cropland/Natural Vegetation", "#00FFFF"),
        15: ("Snow and Ice", "#ffffff"),
        16: ("Barren or sparsely vegetated", "#FFFFAA"),
        17: ("Fill Value/Unclassified", "#00000000")
    }

    sorted_keys = sorted(classes.keys())
    color_list = [classes[k][1] for k in sorted_keys]
    cmap = mcolors.ListedColormap(color_list, name='LandCoverMap')
    boundaries = sorted_keys + [max(sorted_keys) + 1]
    norm = mcolors.BoundaryNorm(boundaries, cmap.N)

    # Create figure in memory
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(data_nan, cmap=cmap, norm=norm)
    ax.set_axis_off()  # Remove axes, ticks, labels

    # Save to in-memory buffer with no extra margins
    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    # Rewind the BytesIO buffer
    png_bytes.seek(0)
    return png_bytes


# Climate Precipitation
def visualize_precipitation_cutout(lon1, lat1, lon2, lat2, year=0):
    data = climate_precipitation_datastruct.array
    meta = common_grid.copy()
    meta['dtype'] = climate_precipitation_datastruct.dtype
    meta['nodata'] = climate_precipitation_datastruct.nodata
    data_nan = np.where(data == meta['nodata'], np.nan, data)
    max_val = np.nanmax(data_nan)

    dst_array, dst_transform = reproject_overlay(
        data_nan[year], lon1, lat1, lon2, lat2
    )

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(dst_array, cmap='Blues', vmax=max_val)
    ax.set_axis_off()

    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    png_bytes.seek(0)
    return png_bytes

# Population Density
def visualize_population_density_cutout(lon1, lat1, lon2, lat2, year=0):
    data = population_density_datastruct.array
    meta = common_grid.copy()
    meta['dtype'] = population_density_datastruct.dtype
    meta['nodata'] = population_density_datastruct.nodata
    data_nan = np.where(data == meta['nodata'], np.nan, data)
    max_val = np.nanmax(data_nan)

    dst_array, dst_transform = reproject_overlay(
        data_nan[year], lon1, lat1, lon2, lat2
    )

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(dst_array, cmap='OrRd', vmax=max_val)
    ax.set_axis_off()

    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    png_bytes.seek(0)
    return png_bytes

# GLW Sheep
def visualize_glw_sheep_cutout(lon1, lat1, lon2, lat2, year=0):
    data = glw_sheep_datastruct.array
    meta = common_grid.copy()
    meta['dtype'] = glw_sheep_datastruct.dtype
    meta['nodata'] = glw_sheep_datastruct.nodata
    data_nan = np.where(data == meta['nodata'], np.nan, data)
    max_val = np.nanmax(data_nan)

    dst_array, dst_transform = reproject_overlay(
        data_nan[year], lon1, lat1, lon2, lat2
    )

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(dst_array, cmap='Purples', vmax=max_val)
    ax.set_axis_off()

    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    png_bytes.seek(0)
    return png_bytes

# GLW Goat
def visualize_glw_goat_cutout(lon1, lat1, lon2, lat2, year=0):
    data = glw_goat_datastruct.array
    meta = common_grid.copy()
    meta['dtype'] = glw_goat_datastruct.dtype
    meta['nodata'] = glw_goat_datastruct.nodata
    data_nan = np.where(data == meta['nodata'], np.nan, data)
    max_val = np.nanmax(data_nan)

    dst_array, dst_transform = reproject_overlay(
        data_nan[year], lon1, lat1, lon2, lat2
    )

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(dst_array, cmap='Greys', vmax=max_val)
    ax.set_axis_off()

    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    png_bytes.seek(0)
    return png_bytes

# GLW Cattle
def visualize_glw_cattle_cutout(lon1, lat1, lon2, lat2, year=0):
    data = glw_cattle_datastruct.array
    meta = common_grid.copy()
    meta['dtype'] = glw_cattle_datastruct.dtype
    meta['nodata'] = glw_cattle_datastruct.nodata
    data_nan = np.where(data == meta['nodata'], np.nan, data)
    max_val = np.nanmax(data_nan)

    dst_array, dst_transform = reproject_overlay(
        data_nan[year], lon1, lat1, lon2, lat2
    )

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(dst_array, cmap='YlOrBr', vmax=max_val)
    ax.set_axis_off()

    png_bytes = io.BytesIO()
    fig.savefig(png_bytes, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    png_bytes.seek(0)
    return png_bytes


if __name__ == '__main__':
    visualize_land_cutout(-11.2843,16.9779,-12.3143,16.4229)