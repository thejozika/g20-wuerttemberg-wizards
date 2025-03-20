# Use a base Python image
FROM python:3.10-slim

# Create a directory inside the container; we'll call it /app
WORKDIR /app

# Copy requirements first and install (to leverage build cache)
COPY python_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Now copy both folders into /app
COPY python_app/ python_app/
COPY datasets/ datasets/

# We will run the application from within python_app
WORKDIR /app/python_app

# Expose the port (if you're running a web server inside, e.g. FastAPI)
EXPOSE 8000

# Example: run FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
