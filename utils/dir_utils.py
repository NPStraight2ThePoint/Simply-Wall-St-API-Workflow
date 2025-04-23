import os
from datetime import datetime
from pathlib import Path

def get_today_date():
    """Returns today's date in YYYY-MM-DD format."""
    return datetime.now().replace(day=1).strftime("%Y-%m-%d")

def get_exchanges_csv_path(TODAY):
    """Returns the file path for the exchanges CSV."""
    return f"C:/.../.venv/Data/Exchanges_Counts/Exchanges_{TODAY}.csv"

# Set paths based on the current date
TODAY = get_today_date()
EXCHANGES_CSV_PATH = get_exchanges_csv_path(TODAY)

failed_log_path = f"C:/.../.venv/Data/Log/Log_companies_{TODAY}.csv"
companies_path = f"C:/.../.venv/Data/Companies"

BASE_DIRECTORIES = [
    Path(r"C:/.../.venv/Data/Try 1"),
    Path(r"C:/.../.venv/Data/Try 2"),
    Path(r"C:/.../.venv/Data//Try 3"),
    Path(r"C:/.../.venv/Data//Try_id/All_Exchanges"),
]

LOG_PATH = [
    Path(r"C:/.../.venv/Data/Log/Log 1.csv"),
    Path(r"C:/.../.venv/Data/Log/Log 2.csv"),
    Path(r"C:/.../.venv/Data/Log/Log 3.csv"),
]

NEW_DATA = Path(
    "C:/Users/.../.venv/Data/Joined Data/NEW_DATA")
EXISTING_DATA = Path(
    "C:/Users/.../.venv/Data/Joined Data/EXISTING_DATA")

FILE_RULES = [
    {"keyword": "insider_transactions", "table": "insider_transactions_uat", "columns": ["exchange", "ticker"]}]

BASE_FOLDER = Path(
    "C:/Users/.../.venv/Data/Joined Data")

TABLE_MAPPINGS = [
    ("insider_transactions_uat", "New_Insider_Transactions"),
    ("insider_transactions", "Existing_Insider_Transactions"),
]

unique_directories = {
    "insider_transactions": "C:/.../.venv/Data/Joined Data/NEW_DATA",
    "exchanges_counts": "C:/.../.venv/Data/Exchanges_Counts"
}
BASE_PATH = r"C:/.../.venv/Log/Listings_failed_id.csv"
