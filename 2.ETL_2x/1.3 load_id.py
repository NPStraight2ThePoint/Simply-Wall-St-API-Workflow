import pandas as pd
from sqlalchemy import create_engine
import os
from utils.dir_utils import *
from utils.load_utils import *
from config.env_utils import *
from datetime import datetime
from utils.sql_utils import *
from config.settings import *
unique_directories = {
    "insider_transactions": "C:/.../.venv/Data/Joined Data/NEW_DATA_id"
}
BASE_DIR = [
    Path(r"C:/.../.venv/Data/Try_id/All_Exchanges"),
]

engine = create_engine(f"postgresql+psycopg2://{db_params['username']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}")
update_multiple_tables_to_uppercase(db_params)
delete_data_from_table(db_params)

# Process files for each base directory (excluding Unique directories)
for base_directory in BASE_DIR:
    process_csv_files(base_directory)

# Process Unique files separately
for special_type, special_directory in unique_directories.items():
    process_csv_files(special_directory, only_special=special_type)





