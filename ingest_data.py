import pandas as pd
import sqlite3
import os

# --- Configuration ---
CSV_FILE_PATH = 'data/Mobile_Food_Facility_Permit_20250504.csv'
DATABASE_FILE_PATH = 'data/foodtrucks.db'
TABLE_NAME = 'food_facilities'

# --- Data Ingestion Script ---
def create_database_and_table(db_path: str):
    """Creates the SQLite database file and the food_facilities table."""
    conn = None
    try:
        # Ensure the directory for the database file exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            locationid INTEGER PRIMARY KEY,
            Applicant TEXT,
            FacilityType TEXT,
            cnn TEXT, -- Storing as TEXT to match potential string/int from CSV
            LocationDescription TEXT,
            Address TEXT,
            blocklot TEXT,
            block TEXT, 
            lot TEXT,
            permit TEXT,
            Status TEXT,
            FoodItems TEXT,
            X REAL,
            Y REAL,
            Latitude REAL, -- Storing as REAL for geospatial calculations
            Longitude REAL, -- Storing as REAL for geospatial calculations
            Schedule TEXT,
            dayshours TEXT,
            NOISent TEXT,
            Approved TEXT,
            Received TEXT, -- Storing as TEXT to match potential string/int/date from CSV
            PriorPermit INTEGER,
            ExpirationDate TEXT,
            Location TEXT, -- This might be the (lat, lon) string, store as TEXT
            Fire_Prevention_Districts INTEGER,
            Police_Districts INTEGER,
            Supervisor_Districts INTEGER,
            Zip_Codes INTEGER,
            Neighborhoods_old TEXT
        );
        """
        cursor.execute(create_table_sql) # Create the table if it doesn't exist
        conn.commit()
        print(f"Database '{db_path}' and table '{TABLE_NAME}' ensured to exist.")

    except sqlite3.Error as e:
        print(f"Database error during table creation: {e}")
    finally:
        if conn:
            conn.close()

def ingest_csv_data(csv_path: str, db_path: str, table_name: str):
    """Reads data from CSV and inserts it into the SQLite table."""
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        print("Please download the data from the SFGov link and place it in the 'data/' directory.")
        return

    print(f"Reading data from {csv_path}...")
    try:
        df = pd.read_csv(csv_path, low_memory=False) # low_memory=False to avoid dtype warning
        print(f"Successfully read {len(df)} rows from CSV.")

        # --- Data Cleaning and Preparation ---
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce') # Convert to numeric, coerce errors to NaN
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

        # Drop rows where Latitude or Longitude are NaN
        initial_rows = len(df)
        df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
        rows_dropped = initial_rows - len(df)
        if rows_dropped > 0:
            print(f"Dropped {rows_dropped} rows with missing Latitude or Longitude.")

        # Rename columns to be valid SQLite identifiers 
        df.columns = [c.strip().replace(' ', '_') for c in df.columns]

        # Based on previous errors, explicitly convert 'cnn' and 'Received' to string
        if 'cnn' in df.columns:
             df['cnn'] = df['cnn'].astype(str)
        if 'Received' in df.columns:
             df['Received'] = df['Received'].astype(str)


        print(f"Connecting to database '{db_path}'...")
        conn = sqlite3.connect(db_path)

        # Use pandas to_sql to insert data
        print(f"Inserting data into table '{table_name}'...")

        # if_exists='replace' will drop the table and recreate it each time, clean load for the assessment
        df.to_sql(table_name, conn, if_exists='replace', index=False) # index=False to avoid writing DataFrame index as a column

        conn.commit()
        print(f"Successfully inserted {len(df)} rows into '{table_name}'.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file is empty at {csv_path}")
    except Exception as e:
        print(f"An error occurred during data ingestion: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)

    # Create the database file and table structure
    create_database_and_table(DATABASE_FILE_PATH)

    # Ingest data from the CSV file into the database
    ingest_csv_data(CSV_FILE_PATH, DATABASE_FILE_PATH, TABLE_NAME)

    print("Data ingestion process finished.")
    print(f"Database file created/updated at: {DATABASE_FILE_PATH}")
