import rasterio
from rasterio.plot import show
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from data_loader import load_raster_set



# Open your raster file
data = load_raster_set('../datasets/Gridded_Population_Density_Data/Assaba_Pop_2010.tif')
# Create a figure and axis object
fig, ax = plt.subplots(figsize=(10, 10))
# Plot the raster data on the axis
show(data["array"], ax=ax)
plt.show()



import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# Open your raster file
with rasterio.open('../datasets/Gridded_Population_Density_Data/Assaba_Pop_2010.tif') as src:
    # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(10, 10))
    # Plot the raster data on the axis
    show(src, ax=ax)
    plt.show()
