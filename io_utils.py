# io_utils.py
import csv
import pandas as pd
from sqlalchemy import create_engine
import os
from config.settings import EXCHANGES_CSV_PATH
from utils.dir_utils import failed_log_path

def init_failed_log():
    if not os.path.isfile(failed_log_path):
        with open(failed_log_path, mode='w', newline='', encoding='utf-8') as log_file:
            writer = csv.writer(log_file)
            writer.writerow(["Exchange", "Offset"])


def load_exchanges():
    df = pd.read_csv(EXCHANGES_CSV_PATH)
    exchange_list = df['exchange'].dropna().unique()
    company_counts = df.set_index('exchange')['company_count'].to_dict()
    return exchange_list, company_counts


def write_csv_header_if_needed(csv_filename):
    if not os.path.isfile(csv_filename):
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                "index_date", "id", "name", "tickerSymbol",
                "exchangeSymbol", "active", "marketCapUSD"
            ])

def flatten_and_save_csv_exchanges(statements, file_path, today):
    """Flatten and save exchange data to CSV."""
    if not statements:
        print("No data available to write.")
        return
    for statement in statements:
        statement["date"] = today

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

    print(f"✅ CSV file '{file_path}' created successfully!")


def csv_to_sql_table(csv_path, table_name, db_connection):
    """Reads CSV file and saves it to the SQL table."""
    df = pd.read_csv(csv_path)
    engine = create_engine(db_connection)
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"✅ Data saved to '{table_name}' table in database.")


def append_to_csv(file_path, exchange, start, end):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([exchange, start, end])
    print(f"Appended to CSV: {exchange}, {start}, {end}")

def save_to_csv(data, csv_file):
    if not data:
        print(f"No data to save for {csv_file}.")
        return

    write_headers = not os.path.exists(csv_file)
    mode = "w" if write_headers else "a"
    with open(csv_file, mode=mode, newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if write_headers:
            writer.writeheader()
        writer.writerows(data)



