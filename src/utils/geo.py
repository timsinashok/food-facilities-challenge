from geopy.distance import geodesic
from typing import Tuple


# --- Geospatial Utility Functions ---
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the geodesic distance between two points on the Earth.

    Args:
        lat1: Latitude of the first point.
        lon1: Longitude of the first point.
        lat2: Latitude of the second point.
        lon2: Longitude of the second point.

    Returns:
        The distance between the two points in kilometers.
        Returns float('inf') if any coordinate is None, though data ingestion
        should handle this by dropping rows. Added as a safeguard.
    """
    # Add a check for None coordinates as a safeguard, though data ingestion
    # should ensure Latitude/Longitude are present for rows used in nearest search.
    if any(coord is None for coord in [lat1, lon1, lat2, lon2]):
        return float('inf') # Return infinity if coordinates are missing

    point1 = (lat1, lon1)
    point2 = (lat2, lon2)

    try:
        distance = geodesic(point1, point2).km
        return distance
    except ValueError as e:
        # Handle potential errors from geopy (e.g., invalid coordinates)
        print(f"Error calculating distance between {point1} and {point2}: {e}")
        return float('inf') # Return infinity on calculation error
