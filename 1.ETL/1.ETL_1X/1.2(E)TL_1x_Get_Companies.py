import csv
import pandas as pd
import os
from pathlib import Path
import requests
from datetime import datetime
from sqlalchemy import create_engine
import time
from env_utils import *
from dir_utils import *

# Create failed_batches CSV with headers if it doesn't exist
if not os.path.isfile(failed_log_path):
    with open(failed_log_path, mode='w', newline='', encoding='utf-8') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(["Exchange", "Offset"])

engine = create_engine(db_connection)
df = pd.read_csv(EXCHANGES_CSV_PATH)
exchange_list = df['exchange'].dropna().unique()
company_counts = df.set_index('exchange')['company_count'].to_dict()
limit = 100

for exchange in exchange_list:
    company_count = company_counts.get(exchange, 0)
    if company_count == 0:
        print(f"⚠️ Skipping {exchange} — no company count recorded.")
        continue

    offset = 0
    csv_filename = f"C:/.../Data/Companies/{exchange}.csv"

    print(f"\n🚀 Fetching data for {exchange}...")

    # Write headers if file doesn't exist
    if not os.path.isfile(csv_filename):
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["index_date", "id", "name", "tickerSymbol", "exchangeSymbol", "active", "marketCapUSD"])

    while offset < company_count:
        print(f"📚 Fetching page: {offset // limit + 1} of {company_count // limit + 1} for {exchange}...")

        payload = {
            "query": """
                query ($exchange: String!, $limit: Int!, $offset: Int!) {
                    companies(exchange: $exchange, limit: $limit, offset: $offset) {
                        id
                        name
                        tickerSymbol
                        exchangeSymbol
                        active
                        marketCapUSD
                    }
                }
            """,
            "variables": {
                "exchange": exchange,
                "limit": limit,
                "offset": offset
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                print(f"❌ API error for {exchange} @ offset {offset}: {response.status_code}")
                print(response.text)
                time.sleep(1)
                offset += limit
                continue

            data = response.json()
            companies = data.get("data", {}).get("companies", [])

            try:
                companies = response.json()["data"]["companies"]
            except (KeyError, TypeError) as parse_error:
                print(f"⚠️ JSON parsing error for {exchange} @ offset {offset}: {parse_error}")
                print("Raw response:", response.text)
                time.sleep(1)
                offset += limit
                continue

            if offset >= company_count:
                print(f"✅ Finished {exchange}: fetched {offset}/{company_count}")
                break

            with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for company in companies:
                    writer.writerow([
                        TODAY,
                        company.get("id"),
                        company.get("name"),
                        company.get("tickerSymbol"),
                        company.get("exchangeSymbol"),
                        company.get("active"),
                        company.get("marketCapUSD")
                    ])

            offset += limit
            time.sleep(0.3)

        except Exception as e:
            print(f"❌ Exception for {exchange} @ offset {offset}: {e}")
            # Log to CSV
            with open(failed_log_path, mode='a', newline='', encoding='utf-8') as log_file:
                writer = csv.writer(log_file)
                writer.writerow([exchange, offset])
            break

    print(f"✅ Finished {exchange}: saved data to {csv_filename}")


for filename in os.listdir(companies_path ):
    if filename.endswith(".csv"):
        csv_path = os.path.join(companies_path , filename)
        print(f"✅ Processing: {filename}")

        df = pd.read_csv(csv_path)
        df.columns = [col.strip() for col in df.columns]
        df.to_sql("companies", con=engine, if_exists='append', index=False)

print("✅ All CSVs loaded into SQL.")
