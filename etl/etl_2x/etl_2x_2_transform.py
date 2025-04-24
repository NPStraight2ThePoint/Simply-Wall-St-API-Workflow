from pathlib import Path
import os
import shutil
import pandas as pd
from datetime import datetime
from config.env_utils import *
from config.settings import *
from utils.dir_utils import *
from utils.transform_utils import *

EXCHANGES_CSV_PATH = "C:/.../.venv/Data/Log/Listings_failed_id.csv"

NEW_DATA = Path(
    "C:/.../.venv/Data/Joined Data/NEW_DATA_id")
EXISTING_DATA = Path(
    "C:/.../.venv/Data/Joined Data/EXISTING_DATA_id")

exchanges_df = pd.read_csv(EXCHANGES_CSV_PATH)
EXCHANGES = exchanges_df["exchangeSymbol"].unique().tolist()
TODAY = datetime.now().replace(day=1).strftime("%Y-%m-%d")

BASE_DIR = [
    Path(r"C:/.../.venv/Data/Try_id/All_Exchanges"),
]

def main():
    # Step 1: Process Data
    transpose_csv(BASE_DIR)

    source_file = Path(f"C:/.../.venv/Data/Try_id/All_Exchanges/Insider_Transactions_{TODAY}.csv")
    destination_file = Path(f"C:/.../.venv/Data/Joined Data/NEW_DATA_id/Insider_Transactions.csv")

    if source_file.exists():
        shutil.copy(source_file, destination_file)
        print(f"✅ Copied: {source_file.name}")
    else:
        print(f"⚠️ File not found: {source_file.name} — skipping copy step.")

    load_temp_SQL(NEW_DATA, FILE_RULES, DB_CONNECTION)

    # Step 2: Ensure Upper Case
    update_columns_to_uppercase(db_params, "insider_transactions_uat")

    # Step 3: Fetch and Save Data
    fetch_and_save_data(db_params, EXCHANGES, TABLE_MAPPINGS, NEW_DATA, EXISTING_DATA)

    # Step 4: Find Unique Transactions
    find_unique_transactions_id(EXCHANGES_CSV_PATH, NEW_DATA, EXISTING_DATA)

if __name__ == "__main__":
    main()

