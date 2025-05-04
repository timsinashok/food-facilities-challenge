from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import sqlite3

from src.core.database import get_db
from src.services.foodtruck_service import FoodFacilityService
from src.data_access.foodtruck_repository import FoodFacilityRepository
from src.models.schemas import FoodFacility, FoodFacilityWithDistance

# These functions are used to provide dependencies to the FastAPI routes.
def get_food_facility_repository(db: sqlite3.Connection = Depends(get_db)) -> FoodFacilityRepository:
    """Provides a FoodFacilityRepository instance with a database connection."""
    return FoodFacilityRepository(db=db)

def get_food_facility_service(
    repository: FoodFacilityRepository = Depends(get_food_facility_repository)) -> FoodFacilityService:
    """Provides a FoodFacilityService instance with a repository."""
    return FoodFacilityService(repository=repository)


# --- API Router ---
router = APIRouter(
    prefix="/foodtrucks",
    tags=["foodtrucks"], # Tags for (Swagger UI)
)

# --- API Endpoints ---
@router.get("/search/name", response_model=List[FoodFacility])
def search_by_name(
    q: str = Query(..., description="Partial or full applicant name to search for."),
    status: Optional[str] = Query(None, description="Optional status to filter by (e.g., 'APPROVED')."),
    service: FoodFacilityService = Depends(get_food_facility_service)
):
    """
    Search food facilities by applicant name with an optional status filter.
    Returns a list of matching food facilities.
    """
    results = service.search_by_name(applicant_name=q, status=status) # status is optional
    return results # returns [] if no results found

@router.get("/search/street", response_model=List[FoodFacility])
def search_by_street(
    q: str = Query(..., description="Partial or full street name to search for."),
    service: FoodFacilityService = Depends(get_food_facility_service)
):
    """
    Search food facilities by street name.
    Returns a list of matching food facilities.
    """
    results = service.search_by_street(street_name=q)
    return results # returns [] if no results found

@router.get("/nearest", response_model=List[FoodFacilityWithDistance])
def find_nearest(
    lat: float = Query(..., description="Latitude of the reference location."),
    lon: float = Query(..., description="Longitude of the reference location."),
    status: Optional[str] = Query("APPROVED", description="Optional status to filter by. Defaults to 'APPROVED'. Use 'all' to include all statuses."),
    limit: int = Query(5, description="Maximum number of nearest facilities to return.", ge=1),
    service: FoodFacilityService = Depends(get_food_facility_service)
):
    """
    Find the nearest food facilities to a given location, optionally filtering by status.
    Default is 'APPROVED' status.
    Returns a list of FoodFacility objects including distance, sorted by distance.
    """
    # Interpret 'all' as no status filter
    search_status = status if status and status.lower() != 'all' else None
    results = service.find_nearest(lat, lon, status=search_status, limit=limit)
    return results # returns [] if no results found
