import pandas as pd
from sqlalchemy import create_engine
import os
from utils.dir_utils import *
from config.env_utils import *
from config.settings import *
engine = create_engine(DB_CONNECTION)

# Define file processing rules
file_rules = [
    {"keyword": "listings", "table": "listings", "columns": ["exchange_symbol", "ticker_symbol"]},
    {"keyword": "members", "table": "members", "columns": ["exchange", "ticker"]},
    {"keyword": "owners", "table": "owners", "columns": ["exchange", "ticker"]},
    {"keyword": "transposed", "table": "statements", "columns": ["exchange", "ticker"]},
    {"keyword": "unique", "table": "insider_transactions", "columns": ["exchange", "ticker"], "special_dir": "insider_transactions"}
    #{"keyword": "Exchanges_Companies", "table": "exchanges_counts", "columns": ["exchange"], "special_dir": "exchanges_counts"}
]

def process_csv_files(directory, only_special=None):
    for root, dirs, files in os.walk(directory):
        for file in files:
            for rule in file_rules:
                if rule["keyword"] in file.lower() and file.endswith(".csv"):
                    if only_special and rule.get("special_dir") != only_special:
                        continue  # Skip files that don't belong to the current special category

                    file_path = os.path.join(root, file)
                    print(f"Processing: {file_path}")

                    try:
                        # Read CSV into DataFrame
                        df = pd.read_csv(file_path, parse_dates=["date"], dayfirst=False)

                        # Convert specified columns to uppercase
                        for column in rule["columns"]:
                            if column in df.columns:
                                df[column] = df[column].astype(str).str.upper()
                            else:
                                print(f"⚠️ Column '{column}' not found in {file}. Skipping uppercase conversion.")

                        # Ensure only string columns are processed with .str
                        for col in df.select_dtypes(include=['object']).columns:
                            df[col] = df[col].astype(str).str.lower()

                        # Insert into SQL table
                        df.to_sql(rule["table"], engine, if_exists="append", index=False)
                        print(f"✅ Successfully inserted: {file} into {rule['table']}")
                    except Exception as e:
                        print(f"❌ Error processing {file}: {e}")



