from fastapi import FastAPI, HTTPException
from shapely.geometry import box
from app.models import AreaQuery, DataResponse, PixelData, VectorData
from app.data_loader import load_all_data

# Path to your base data folder in the G-20 project
DATA_BASE_DIR = "./data"

# Load all data at startup (assume load_all_data returns a dict mapping year -> GeoDataFrame)
data_by_year = load_all_data(DATA_BASE_DIR)

app = FastAPI(
    title="Spatial Data API",
    description="API to query spatial data by bounding box, year, and layer(s)"
)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Spatial Data API is running"}


@app.post("/get_data", response_model=DataResponse, tags=["Data Query"])
def get_data(query: AreaQuery):
    year = query.year
    if year not in data_by_year:
        raise HTTPException(status_code=404, detail=f"No data found for year {year}")

    # Create bounding box from query
    bbox = box(query.min_lon, query.min_lat, query.max_lon, query.max_lat)

    # Retrieve the relevant GeoDataFrame for the specified year
    gdf = data_by_year[year]

    # Filter GeoDataFrame to those geometries intersecting the bounding box
    matching = gdf[gdf.intersects(bbox)]
    if matching.empty:
        raise HTTPException(status_code=404, detail="No data found for the specified bounding box")

    results = []

    # Decide on the return type based on the layer name.
    # For example, layers starting with "Layer" return pixel data,
    # and layers starting with "Analytics" return vector data.
    for layer in query.layers:
        if layer.startswith("Layer"):
            # Replace with actual logic to extract a 100x100 pixel grid from the raster
            dummy_grid = [[0.0 for _ in range(100)] for _ in range(100)]
            results.append(PixelData(layer=layer, data=dummy_grid))
        elif layer.startswith("Analytics"):
            # Replace with actual logic to extract vector data (e.g., clip geometries to bbox)
            dummy_geojson = {
                "type": "FeatureCollection",
                "features": []  # Populate with actual features clipped to the bounding box
            }
            results.append(VectorData(layer=layer, geometry=dummy_geojson))
        else:
            raise HTTPException(status_code=400, detail=f"Invalid layer type: {layer}")

    return DataResponse(result=results)
