import uvicorn
from fastapi.responses import Response
from fastapi import FastAPI, Query, HTTPException

from python_app.visualizer import visualize_land_cutout, visualize_gpp_cutout, visualize_glw_cattle_cutout , visualize_precipitation_cutout, visualize_glw_goat_cutout ,visualize_glw_sheep_cutout ,visualize_population_density_cutout

app = FastAPI(
    title="Spatial Data API",
    description="API to query spatial data by bounding box, year, and layer(s)"
)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Spatial Data API is running"}


@app.get("/cutout/land", response_class=Response)
def get_cutout(lon1: float, lat1: float, lon2: float, lat2: float,year: int = Query(..., ge=2010, le=2023, description="Year between 2010 and 2023")):
    """
    Example endpoint:
    GET /cutout?lon1=-11.2843&lat1=16.9779&lon2=-12.3143&lat2=16.4229&year=2010
    """
    try:
        png_bytes_io = visualize_land_cutout(lon1, lat1, lon2, lat2, year=year-2010)  # update your function to handle year
        png_bytes = png_bytes_io.getvalue()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(content=png_bytes, media_type="image/png")

@app.get("/cutout/gpp", response_class=Response)
def get_cutout(lon1: float, lat1: float, lon2: float, lat2: float,year: int = Query(..., ge=2010, le=2023, description="Year between 2010 and 2023")):
    """
    Example endpoint:
    GET /cutout?lon1=-11.2843&lat1=16.9779&lon2=-12.3143&lat2=16.4229&year=2010
    """
    try:
        png_bytes_io = visualize_gpp_cutout(lon1, lat1, lon2, lat2, year=year-2010)  # update your function to handle year
        png_bytes = png_bytes_io.getvalue()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(content=png_bytes, media_type="image/png")

@app.get("/cutout/population", response_class=Response)
def get_cutout(lon1: float, lat1: float, lon2: float, lat2: float,year: int = Query(..., ge=2010, le=2023, description="Year between 2010 and 2023")):
    """
    Example endpoint:
    GET /cutout?lon1=-11.2843&lat1=16.9779&lon2=-12.3143&lat2=16.4229&year=2010
    """
    try:
        png_bytes_io = visualize_population_density_cutout(lon1, lat1, lon2, lat2, year=year-2010)  # update your function to handle year
        png_bytes = png_bytes_io.getvalue()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(content=png_bytes, media_type="image/png")

@app.get("/cutout/precipitation", response_class=Response)
def get_cutout(lon1: float, lat1: float, lon2: float, lat2: float,year: int = Query(..., ge=2010, le=2023, description="Year between 2010 and 2023")):
    """
    Example endpoint:
    GET /cutout?lon1=-11.2843&lat1=16.9779&lon2=-12.3143&lat2=16.4229&year=2010
    """
    try:
        png_bytes_io = visualize_precipitation_cutout(lon1, lat1, lon2, lat2, year=year-2010)  # update your function to handle year
        png_bytes = png_bytes_io.getvalue()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(content=png_bytes, media_type="image/png")

@app.get("/cutout/goat", response_class=Response)
def get_cutout(lon1: float, lat1: float, lon2: float, lat2: float,year: int = Query(..., ge=2010, le=2023, description="Year between 2010 and 2023")):
    """
    Example endpoint:
    GET /cutout?lon1=-11.2843&lat1=16.9779&lon2=-12.3143&lat2=16.4229&year=2010
    """
    try:
        png_bytes_io = visualize_glw_goat_cutout(lon1, lat1, lon2, lat2, year=year-2010)  # update your function to handle year
        png_bytes = png_bytes_io.getvalue()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(content=png_bytes, media_type="image/png")

@app.get("/cutout/cattle", response_class=Response)
def get_cutout(lon1: float, lat1: float, lon2: float, lat2: float,year: int = Query(..., ge=2010, le=2023, description="Year between 2010 and 2023")):
    """
    Example endpoint:
    GET /cutout?lon1=-11.2843&lat1=16.9779&lon2=-12.3143&lat2=16.4229&year=2010
    """
    try:
        png_bytes_io = visualize_glw_cattle_cutout(lon1, lat1, lon2, lat2, year=year-2010)  # update your function to handle year
        png_bytes = png_bytes_io.getvalue()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(content=png_bytes, media_type="image/png")

@app.get("/cutout/sheep", response_class=Response)
def get_cutout(lon1: float, lat1: float, lon2: float, lat2: float,year: int = Query(..., ge=2010, le=2023, description="Year between 2010 and 2023")):
    """
    Example endpoint:
    GET /cutout?lon1=-11.2843&lat1=16.9779&lon2=-12.3143&lat2=16.4229&year=2010
    """
    try:
        png_bytes_io = visualize_glw_sheep_cutout(lon1, lat1, lon2, lat2, year=year-2010)  # update your function to handle year
        png_bytes = png_bytes_io.getvalue()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(content=png_bytes, media_type="image/png")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
