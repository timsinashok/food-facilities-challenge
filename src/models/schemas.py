from pydantic import BaseModel
from typing import Optional, List, Union # union is used for type hinting multiple types

class FoodFacilityBase(BaseModel):
    """Base schema for a food facility."""
    locationid: int
    Applicant: str
    FacilityType: Optional[str] = None

    # allowing cnn to be str or int based on potential data variations
    cnn: Optional[Union[str, int]] = None
    LocationDescription: Optional[str] = None
    Address: Optional[str] = None
    blocklot: Optional[str] = None
    block: Optional[str] = None
    lot: Optional[str] = None
    permit: Optional[str] = None
    Status: Optional[str] = None
    FoodItems: Optional[str] = None
    X: Optional[float] = None
    Y: Optional[float] = None

    # Latitude and Longitude are crucial for nearest search, but handle potential None
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None
    Schedule: Optional[str] = None
    dayshours: Optional[str] = None
    NOISent: Optional[str] = None
    Approved: Optional[str] = None

    # Allow Received to be str or int based on potential data variations (dates might be numbers)
    Received: Optional[Union[str, int]] = None
    PriorPermit: Optional[int] = None
    ExpirationDate: Optional[str] = None
    Location: Optional[str] = None 
    Fire_Prevention_Districts: Optional[int] = None
    Police_Districts: Optional[int] = None
    Supervisor_Districts: Optional[int] = None
    Zip_Codes: Optional[int] = None
    Neighborhoods_old: Optional[str] = None


class FoodFacility(FoodFacilityBase):
    """Schema for a food facility, extending the base."""
    pass

class FoodFacilityWithDistance(FoodFacility):
    """Schema for a food facility including calculated distance."""
    distance_km: float 

