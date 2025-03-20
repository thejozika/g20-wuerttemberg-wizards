import numpy as np

from python_app.data_loader import population_density_raster_layers, climate_precipitation_raster_layers, \
    modis_gpp_raster_layers, modis_land_raster_layers
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def replace_nodata_with_nan(array, nodata_val=65535.0):
    return np.where(array == nodata_val, np.nan, array)


def transform(data:np.array , meta:dict)->(np.ndarray,dict):
    print('implement me')


def visualize(data:np.array , meta:dict):
    data_nan = replace_nodata_with_nan(data, nodata_val=meta['nodata'])

    plt.figure(figsize=(10, 8))
    img = plt.imshow(data_nan, cmap='viridis')
    plt.title(f"Raster Visualization: {'2010R'}")
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.colorbar(img, label='Pixel Values')
    plt.show()

def visualize_land(data: np.ndarray, meta: dict):
    """
    Visualize the land-cover raster using a discrete colormap
    based on categorical classes.
    """
    # Replace nodata with NaN
    data_nan = replace_nodata_with_nan(data, nodata_val=meta['nodata'])

    # Define class labels and colors (adjust the colors as you like)
    classes = {
        0:  ("Water",                         "#1f78b4"),
        1:  ("Evergreen Needleleaf Forest",   "#33a02c"),
        2:  ("Evergreen Broadleaf Forest",    "#b2df8a"),
        3:  ("Deciduous Needleleaf Forest",   "#006400"),
        4:  ("Deciduous Broadleaf Forest",    "#8dd3c7"),
        5:  ("Mixed Forest",                  "#ffffb3"),
        6:  ("Closed Shrublands",             "#8B4513"),
        7:  ("Open Shrublands",               "#bc8f8f"),
        8:  ("Woody Savannas",                "#d9d9d9"),
        9:  ("Savannas",                      "#fdbf6f"),
        10: ("Grasslands",                    "#ff7f00"),
        11: ("Permanent Wetlands",            "#1ecbe1"),
        12: ("Croplands",                     "#fb9a99"),
        13: ("Urban and Built-Up Lands",      "#e31a1c"),
        14: ("Cropland/Natural Vegetation",   "#cab2d6"),
        15: ("Snow and Ice",                  "#ffffff"),
        16: ("Barren or sparsely vegetated",  "#aaaaaa"),
        17: ("Fill Value/Unclassified",       "#000000")
    }

    sorted_keys = sorted(classes.keys())
    color_list = [classes[k][1] for k in sorted_keys]
    label_list = [classes[k][0] for k in sorted_keys]

    cmap = mcolors.ListedColormap(color_list, name='LandCoverMap')
    # Create boundaries such that each class gets its own "bin"
    boundaries = sorted_keys + [max(sorted_keys) + 1]
    norm = mcolors.BoundaryNorm(boundaries, cmap.N)

    # Plot
    plt.figure(figsize=(10, 8))
    img = plt.imshow(data_nan, cmap=cmap, norm=norm)
    plt.title("Raster Visualization: 2010R")
    plt.xlabel('Columns')
    plt.ylabel('Rows')

    # Create a colorbar with one tick per class, centered between boundaries
    cbar = plt.colorbar(img, ticks=[k + 0.5 for k in sorted_keys])
    cbar.ax.set_yticklabels(label_list)

    plt.show()

if __name__ == "__main__":
    data = modis_land_raster_layers['2011LCT']["array"]
    meta = modis_land_raster_layers['2011LCT']["meta"]
    visualize_land(data,meta)