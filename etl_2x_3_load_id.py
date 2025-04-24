from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from utils.dir_utils import *
from utils.load_utils import *
from config.env_utils import *
from datetime import datetime
from utils.sql_utils import *
from config.settings import *

# Define your base and unique directories
BASE_DIR = [
    Path(r"C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production/.venv/Data/Try_id/All_Exchanges"),
]
unique_directories = {
    "insider_transactions": r"C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production/.venv/Data/Joined Data/NEW_DATA_id"
}

def main():
    print("🚀 Starting ETL process...")

    # Step 1: Create DB engine
    engine = create_engine(
        f"postgresql+psycopg2://{db_params['username']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
    )

    # Step 2: Setup database (if needed)
    update_multiple_tables_to_uppercase(db_params)
    delete_data_from_table(db_params)

    # Step 3: Process base directories
    for base_directory in BASE_DIR:
        if Path(base_directory).exists():
            process_csv_files(base_directory)
        else:
            print(f"⚠️ Directory not found: {base_directory}, skipping...")

    # Step 4: Process unique/special directories
    for special_type, special_directory in unique_directories.items():
        if Path(special_directory).exists():
            process_csv_files(special_directory, only_special=special_type)
        else:
            print(f"⚠️ Special directory not found: {special_directory}, skipping...")

    print("✅ ETL process complete.")

if __name__ == "__main__":
    main()







