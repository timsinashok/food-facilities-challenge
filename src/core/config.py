from pathlib import Path

# Go two levels up from config.py → from core → src → your-project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Path to the SQLite database file
DATABASE_PATH = BASE_DIR / 'data' / 'foodtrucks.db'
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
