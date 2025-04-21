import os
from pathlib import Path
import requests
from env_utils import *
from data_flattening_utils import *
from dir_utils import *
import pandas as pd
from sqlalchemy import create_engine

# Fetch the data
response = requests.post(url, headers=headers, json={"query": query_exchanges})
data = response.json()

# Get the exchange data
statements = data.get('data', {}).get('exchanges', [])

# Main function to flatten and save the CSV
flatten_and_save_csv_exchanges(statements, EXCHANGES_CSV_PATH, TODAY)

# Load your CSV
df = pd.read_csv(EXCHANGES_CSV_PATH)

# Connect to PostgreSQL
engine = create_engine("....")

# Load into SQL
df.to_sql("exchanges_counts", engine, if_exists="append", index=False)
