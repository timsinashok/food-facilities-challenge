import pytest

from src.utils.geo import calculate_distance


# --- Utility Function Tests ---
def test_calculate_distance_same_point():
    """Test distance calculation for the same point."""
    lat, lon = 37.7749, -122.4194 # San Francisco coordinates
    distance = calculate_distance(lat, lon, lat, lon)
    
    # Distance should be 0 for the same point, allowing small tolerance
    assert distance == pytest.approx(0.0, abs=1e-9)

def test_calculate_distance_known_points():
    """Test distance calculation for known points with expected distance."""

    # Example 1: Distance between San Francisco City Hall and Golden Gate Bridge
    sf_city_hall = (37.7790, -122.4199)
    golden_gate_bridge = (37.8199, -122.4783)

    # geodesic distance in km calculated using https://www.fai.org/page/world-distance-calculator
    expected_distance_km = 6.860178748724984 

    distance = calculate_distance(
        sf_city_hall[0], sf_city_hall[1],
        golden_gate_bridge[0], golden_gate_bridge[1]
    )
    
    assert distance == pytest.approx(expected_distance_km, abs=0.05) # Allow +/- 0.05 km tolerance


    # Example 2: Distance between two points on the equator (simple case)
    distance_equator = calculate_distance(0, 0, 0, 1)
    assert distance_equator == pytest.approx(111.32, rel=0.01) # Allow 1% relative tolerance

def test_calculate_distance_with_none_coordinates():
    """Test distance calculation when one or more coordinates are None."""
    
    # The calculate_distance function includes a safeguard for None values
    distance = calculate_distance(37.7, -122.4, None, -122.5)
    assert distance == float('inf')

    distance = calculate_distance(None, None, 37.8, -122.5)
    assert distance == float('inf')

    distance = calculate_distance(37.7, -122.4, 37.8, None)
    assert distance == float('inf')
