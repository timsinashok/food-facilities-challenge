from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import os

# Import the API router for food trucks
from src.api import foodtrucks

# --- FastAPI Application Instance ---
app = FastAPI(
    title="SF Mobile Food Facilities API", # Updated title
    description="API for searching and finding nearest mobile food facilities in San Francisco",
    version="1.0.0", # Version for the API docs
    docs_url="/docs", # Explicitly set docs URL
    redoc_url="/redoc" # Explicitly set redoc URL
)

# --- Include API Routers ---
# Include the foodtrucks router in the main application
app.include_router(foodtrucks.router)


# --- Serve Static Files (Simple UI) ---
# Mount the 'ui' directory to serve static files (HTML, CSS, JS)
app.mount("/", StaticFiles(directory="ui", html=True), name="static")




