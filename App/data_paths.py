# Centralized data path configuration
# Provides robust, portable access to data files regardless of current working directory.

from pathlib import Path

# Project root assumed to be two levels up from this file (App/ is under root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = (PROJECT_ROOT / 'Data').resolve()

# Individual data files (add more as needed)
PRIMARY_DATA_FILE = DATA_DIR / 'Chennai_FlightData_Processed.xlsx'
CASCADING_DELAYS_FILE = DATA_DIR / 'cascading_delays.xlsx'
WEATHER_CASCADING_DELAYS_FILE = DATA_DIR / 'weather_cascading_delays.xlsx'
FLIGHT_SUMMARY_BY_HOUR_FILE = DATA_DIR / 'Flight_Summary_By_Hour.xlsx'
SUMMARY_TABLE_FILE = DATA_DIR / 'summary_table.xlsx'

# Helper loader functions

def get_data_path(filename: str):
    """Return a Path to a file inside the Data directory."""
    return DATA_DIR / filename

__all__ = [
    'PROJECT_ROOT', 'DATA_DIR', 'PRIMARY_DATA_FILE', 'CASCADING_DELAYS_FILE',
    'WEATHER_CASCADING_DELAYS_FILE', 'FLIGHT_SUMMARY_BY_HOUR_FILE', 'SUMMARY_TABLE_FILE',
    'get_data_path'
]
