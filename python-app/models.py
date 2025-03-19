from pydantic import BaseModel, Field
from typing import List, Literal, Union

# Define allowed layer names
AllowedLayer = Literal["Layer1", "Layer2", "Layer3", "Layer4", "Analytics1", "Analytics2", "Analytics3"]


class AreaQuery(BaseModel):
    year: int = Field(..., description="Year of the dataset")
    min_lat: float = Field(..., description="Minimum latitude of the bounding box")
    max_lat: float = Field(..., description="Maximum latitude of the bounding box")
    min_lon: float = Field(..., description="Minimum longitude of the bounding box")
    max_lon: float = Field(..., description="Maximum longitude of the bounding box")
    layers: List[AllowedLayer] = Field(...,
                                       description="List of layers to query. Allowed values: Layer1, Layer2, Layer3, Layer4, Analytics1, Analytics2, Analytics3")


class PixelData(BaseModel):
    layer: AllowedLayer = Field(..., description="Layer name")
    # A 100x100 grid of pixel values (e.g., float numbers)
    data: List[List[float]] = Field(..., description="Pixel data as a 100x100 grid")


class VectorData(BaseModel):
    layer: AllowedLayer = Field(..., description="Layer name")
    # GeoJSON-like object representing vector data. A GeoJSON object is a JSON format
    # for encoding a variety of geographic data structures (like Point, LineString, Polygon, etc.)
    geometry: dict = Field(..., description="A valid GeoJSON object for the requested area")


# The response will be a list of results, one per layer.
class DataResponse(BaseModel):
    result: List[Union[PixelData, VectorData]] = Field(..., description="List of results, one per requested layer")
