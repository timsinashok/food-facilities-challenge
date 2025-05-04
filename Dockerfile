# Use a base image that includes lightweight Python
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install uv - this requires pip initially
RUN pip install uv

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies using uv into the system environment(not venv) inside the container
RUN uv pip install --system -r requirements.txt

# Copy the rest of the application code 
COPY . .

# Ensure the data directory exists inside the container
RUN mkdir -p data

# --- Data Ingestion Step ---
# this step is essential to ensure that the data is available in the container
RUN python ingest_data.py  

# Expose the port that your FastAPI application will run on (default is 8000)
EXPOSE 8000

# Command to run your application using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
