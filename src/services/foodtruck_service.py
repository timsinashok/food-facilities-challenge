
from typing import List, Optional

from src.models.schemas import FoodFacility, FoodFacilityWithDistance
from src.utils.geo import calculate_distance
from src.data_access.foodtruck_repository import FoodFacilityRepository

class FoodFacilityService:
    """Handles business logic for Food Facilities.
    Uses a FoodFacilityRepository to access data.
    """

    def __init__(self, repository: FoodFacilityRepository):
        """
        Initializes the service with a repository instance.
        Args:
            repository: An instance of FoodFacilityRepository.
        """
        self.repository = repository

    def search_by_name(self, applicant_name: str, status: Optional[str] = None) -> List[FoodFacility]:
        """
        Search food facilities by applicant name with an optional status filter.
        Args:  
            applicant_name: Partial or full applicant name.
            status: Optional status to filter by.
        Returns:
            A list of FoodFacility objects.
        """
        facilities_base = self.repository.search_by_applicant_name(applicant_name, status)

        # Convert to FoodFacility schema, we have the same structure
        return [FoodFacility(**f.model_dump()) for f in facilities_base] 

    def search_by_street(self, street_name: str) -> List[FoodFacility]:
        """
        Search food facilities by street name.
        Args:
            street_name: Partial or full street name.
        Returns:
            A list of FoodFacility objects.
        """
        facilities_base = self.repository.search_by_street_name(street_name)
        return [FoodFacility(**f.model_dump()) for f in facilities_base] # Convert to FoodFacility schema

    def find_nearest(
        self, lat: float, lon: float, status: Optional[str] = "APPROVED", limit: int = 5
    ) -> List[FoodFacilityWithDistance]:
        """
        Find the nearest food facilities to a given location, optionally filtering by status.
        Args:
            lat: Latitude of the reference location.
            lon: Longitude of the reference location.
            status: Optional status to filter by. Defaults to 'APPROVED'.
            limit: Maximum number of nearest facilities to return.
        Returns:
            A list of FoodFacilityWithDistance objects, sorted by distance, up to the specified limit.
        """

        if status is not None:
            facilities_base = self.repository.get_facilities_by_status(status)
        else:
            # state is None (meaning all statuses), get all facilities with location
            facilities_base = self.repository.get_all_facilities_with_location()

        # Calculate distance for each facility and store with the facility data
        facilities_with_distance = []
        for facility_base in facilities_base:
            # Ensure Latitude and Longitude are not None before calculating
            if facility_base.Latitude is not None and facility_base.Longitude is not None:
                 distance_km = calculate_distance(lat, lon, facility_base.Latitude, facility_base.Longitude)

                 # Create a FoodFacilityWithDistance object including the calculated distance
                 facilities_with_distance.append(FoodFacilityWithDistance(**facility_base.model_dump(), distance_km=distance_km))

        # Sort by distance and return the top results based on the limit
        facilities_with_distance.sort(key=lambda x: x.distance_km)
        return facilities_with_distance[:limit]
