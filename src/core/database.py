import sqlite3
from typing import Generator
from fastapi import HTTPException 

from src.core.config import DATABASE_URL

# --- Database Connection Setup ---
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Dependency that yields a SQLite database connection.
    The connection will be automatically closed after the request is finished.
    Handles potential database connection errors.
    """
    conn = None
    try:
        db_path = DATABASE_URL.replace("sqlite:///", "")
        print(f"Attempting to connect to database at: {db_path}")

        # check_same_thread=False is needed for SQLite with FastAPI/Uvicorn as requests might be handled by different threads.
        conn = sqlite3.connect(db_path, check_same_thread=False)

        # Set the row_factory to sqlite3.Row to access columns by name
        conn.row_factory = sqlite3.Row

        # Yield the connection to the endpoint function that uses this dependency
        yield conn

    except sqlite3.Error as e:
        # Catch specific SQLite errors (e.g., unable to open database)
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
    
    except Exception as e:
        # Catch any other unexpected errors during connection setup
        print(f"An unexpected error occurred in get_db: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {e}")
    finally:
        # Ensure the connection is closed even if errors occur or exceptions are raised
        if conn:
            conn.close()

