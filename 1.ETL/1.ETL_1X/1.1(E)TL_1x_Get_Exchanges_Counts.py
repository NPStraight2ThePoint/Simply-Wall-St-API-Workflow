import requests
from env_utils import *
from dir_utils import *
import pandas as pd
from sqlalchemy import create_engine
import csv

def flatten_and_save_csv_exchanges(statements, file_path, today):
    if not statements:
        print("No data available to write.")
        return
    for statement in statements:
        statement["date"] = today
    header_mapping = {
        "date": "index_date",
        "symbol": "exchange",
        "companiesCount": "company_count",
    }
    final_headers = ["index_date", "exchange", "company_count"]

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(final_headers)  # Write headers
        for statement in statements:
            row = [
                statement.get("date", ""),
                statement.get("symbol", ""),
                statement.get("companiesCount", "")
            ]
            writer.writerow(row)

    print(f"✅ CSV file '{file_path}' created successfully with ordered headers!")

response = requests.post(url, headers=headers, json={"query": query_exchanges})
data = response.json()
statements = data.get('data', {}).get('exchanges', [])

flatten_and_save_csv_exchanges(statements, EXCHANGES_CSV_PATH, TODAY)

df = pd.read_csv(EXCHANGES_CSV_PATH)
engine = create_engine(db_connection)
df.to_sql("exchanges_counts", engine, if_exists="append", index=False)


