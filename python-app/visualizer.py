import rasterio
from rasterio.plot import show
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from data_loader import get_strucured_data



# Open your raster file
all_data = get_strucured_data()
data = all_data.population_density_mrt.get('2021')
# Create a figure and axis object
fig, ax = plt.subplots(figsize=(10, 10))
# Plot the raster data on the axis
show(data["array"],transform=data["meta"]["transform"], ax=ax, vmin=0)
plt.show()
