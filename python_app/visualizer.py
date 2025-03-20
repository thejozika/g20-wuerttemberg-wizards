import numpy as np

from python_app.data_loader import population_density_raster_layers, climate_precipitation_raster_layers, \
    modis_gpp_raster_layers, modis_land_raster_layers
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def replace_nodata_with_nan(array, nodata_val=65535.0):
    return np.where(array == nodata_val, np.nan, array)


if __name__ == "__main__":
    data = climate_precipitation_raster_layers['2010R']["array"]
    meta = climate_precipitation_raster_layers['2010R']["meta"]
    data_nan = replace_nodata_with_nan(data, nodata_val=65535)

    plt.figure(figsize=(10, 8))
    img = plt.imshow(data, cmap='viridis')
    plt.title(f"Raster Visualization: {'2010R'}")
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.colorbar(img, label='Pixel Values')
    plt.show()
