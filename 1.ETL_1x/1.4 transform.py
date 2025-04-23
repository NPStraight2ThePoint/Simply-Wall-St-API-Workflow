import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from config.env_utils import *
from config.settings import *
from utils.dir_utils import *
from utils.transform_utils import *

exchanges_df = pd.read_csv(EXCHANGES_CSV_PATH)
EXCHANGES = exchanges_df["exchange"].unique().tolist()

def main():
    # Step 1: Process Data
    transpose_csv(BASE_DIRECTORIES)
    merge_insider_transactions(BASE_DIRECTORIES, NEW_DATA)
    load_temp_SQL(NEW_DATA, FILE_RULES, DB_CONNECTION)

    # Step 2: Ensure Upper Case
    update_columns_to_uppercase(db_params, "insider_transactions_uat")

    # Step 3: Fetch and Save Data
    fetch_and_save_data(db_params, EXCHANGES, TABLE_MAPPINGS, NEW_DATA, EXISTING_DATA)

    # Step 4: Find Unique Transactions
    find_unique_transactions(EXCHANGES_CSV_PATH, NEW_DATA, EXISTING_DATA)

# 📌
if __name__ == "__main__":
    main()

