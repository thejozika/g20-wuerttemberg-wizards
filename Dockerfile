FROM python:3.10

# Set a working directory
WORKDIR /app

# Install any system dependencies your geospatial libraries need
# (Even in a bigger image, you usually still need GDAL, PROJ, build tools, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Environment variables for Rasterio/pyproj to locate GDAL headers
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy your requirements file and install Python dependencies
COPY python_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Now copy in your actual application code
COPY python_app/. ./python_app/
COPY datasets/. ./datasets/

# Expose a port if you are running a server (FastAPI, etc.)
EXPOSE 8000

# Example: run a FastAPI app with Uvicorn
CMD ["uvicorn", "python_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
