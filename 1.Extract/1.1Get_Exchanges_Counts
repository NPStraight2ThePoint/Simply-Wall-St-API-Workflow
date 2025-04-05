import os
from pathlib import Path
import requests
from env_utils import *
from data_flattening_utils import *
from dir_utils import *

# Fetch the data
response = requests.post(url, headers=headers, json={"query": query_exchanges})
data = response.json()

# Get the exchange data
statements = data.get('data', {}).get('exchanges', [])

# Main function to flatten and save the CSV
flatten_and_save_csv_exchanges(statements, EXCHANGES_CSV_PATH, TODAY)

