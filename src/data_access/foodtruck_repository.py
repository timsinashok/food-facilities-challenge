import sqlite3
from typing import List, Optional, Tuple

from src.models.schemas import FoodFacilityBase 

class FoodFacilityRepository:
    """
    Repository class for accessing Food Facility data from the SQLite database.
    Handles direct database interactions and returns raw data (or Pydantic models
    representing the raw data structure).
    """
    def __init__(self, db: sqlite3.Connection):
        """
        Initializes the repository with a database connection.

        Args:
            db: The active SQLite database connection.
        """
        self.db = db

    def _execute_query(self, query: str, params: Optional[list] = None) -> List[sqlite3.Row]:
        """Helper method to execute a read query and fetch all results."""
        cursor = self.db.cursor()
        try:
            db_path = self.db.execute("PRAGMA database_list;").fetchone()[2]

            cursor.execute(query, params or [])
            rows = cursor.fetchall()
            return rows
        
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return [] # Return empty list on query error

    def get_all_facilities(self) -> List[FoodFacilityBase]:
        """Fetches all food facilities from the database."""
        query = "SELECT * FROM food_facilities WHERE Latitude IS NOT NULL AND Longitude IS NOT NULL"
        rows = self._execute_query(query)
        # Convert raw rows to Pydantic models representing the data structure
        return [FoodFacilityBase(**row) for row in rows]

    def search_by_applicant_name(self, name_query: str, status: Optional[str] = None) -> List[FoodFacilityBase]:
        """Searches facilities by applicant name (partial, case-insensitive)."""
        query = "SELECT * FROM food_facilities WHERE LOWER(Applicant) LIKE ?"
        params = [f"%{name_query.lower()}%"]

        if status:
            query += " AND LOWER(Status) = ?"
            params.append(status.lower())

        rows = self._execute_query(query, params)
        return [FoodFacilityBase(**row) for row in rows]

    def search_by_street_name(self, street_query: str) -> List[FoodFacilityBase]:
        """Searches facilities by street name (partial, case-insensitive)."""
        query = "SELECT * FROM food_facilities WHERE LOWER(Address) LIKE ?"
        params = [f"%{street_query.lower()}%"]

        rows = self._execute_query(query, params)
        return [FoodFacilityBase(**row) for row in rows]

    def get_facilities_by_status(self, status: str) -> List[FoodFacilityBase]:
        """Fetches facilities filtered by a specific status (case-insensitive)."""
        query = "SELECT * FROM food_facilities WHERE LOWER(Status) = ? AND Latitude IS NOT NULL AND Longitude IS NOT NULL"
        params = [status.lower()]
        rows = self._execute_query(query, params)
        return [FoodFacilityBase(**row) for row in rows]

    def get_all_facilities_with_location(self) -> List[FoodFacilityBase]:
        """Fetches all facilities that have valid Latitude and Longitude."""
        query = "SELECT * FROM food_facilities WHERE Latitude IS NOT NULL AND Longitude IS NOT NULL"
        rows = self._execute_query(query)
        return [FoodFacilityBase(**row) for row in rows]
