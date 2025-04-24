import logging
import pandas as pd
from utils.dir_utils import *
from utils.flatten_utils import *
import os
import requests
from config.env_utils import *
from config.settings import *
from config.api_queries import *
import csv
import psycopg2
from datetime import datetime

# Define the query to include only differences ≠ 0
query = """
SELECT t.*
FROM companies t
WHERE NOT EXISTS (
    SELECT 1
    FROM listings l
    WHERE t."tickerSymbol" = l.ticker_symbol
);
"""

# Connect and fetch
conn = psycopg2.connect(**db_params1)
df = pd.read_sql(query, conn, params=(TODAY))
conn.close()

# Save to CSV
df.to_csv(f"C:/.../.venv/Data/Log/Listings_failed_id.csv", index=False)
print(f"✅ Saved CSV for Listings id missing on {TODAY}")

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_to_csv(data, file_path):
    if not data:
        logging.warning(f"No data to save for {file_path}")
        return
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        logging.error(f"Error saving CSV {file_path}: {e}")

# === File Paths ===
exchanges_file = "C:/.../.venv/Data/Log/Listings_failed_id.csv"
base_path = "C:/.../.venv/Data/Try_id"

def safe_get(data, key, default=None):
    try:
        if data is None:
            return default
        return data.get(key, default)
    except Exception as e:
        logging.error(f"Error accessing {key} in data: {data}. Error: {str(e)}")
        return default


def flatten_statements(company, ticker, exchange, today):
    return [{
        "ticker": ticker,
        "exchange": exchange,
        "date": today,
        "name": safe_get(s, 'name'),
        "title": safe_get(s, 'title'),
        "area": safe_get(s, 'area'),
        "type": safe_get(s, 'type'),
        "value": safe_get(s, 'value'),
        "description": safe_get(s, 'description'),
        "state": safe_get(s, 'state'),
        "severity": safe_get(s, 'severity'),
        "outcomeName": safe_get(s, 'outcomeName')
    } for s in company.get("statements", [])]


def flatten_listings(company, ticker, exchange, today):
    return [{
        'id': safe_get(company, "id", ""),
        'date': today,
        'exchange_symbol': exchange,
        'ticker_symbol': ticker,
        'name': safe_get(company, "name", ""),
        'market_cap_usd': safe_get(company, "marketCapUSD", 0),
        'primary_industry': safe_get(company.get("primaryIndustry", {}), "name", ""),
        'secondary_industry': safe_get(company.get("secondaryIndustry", {}), "name", ""),
        'tertiary_industry': safe_get(company.get("tertiaryIndustry", {}), "name", ""),
        'market': safe_get(company.get("market", {}), "name", ""),
        'market_iso2': safe_get(company.get("market", {}), "iso2", ""),
        'active': safe_get(company, "active", ""),
        'classification_status': safe_get(company, "classificationStatus", ""),
    }]


def flatten_owners(company, ticker, exchange, today):
    return [{
        "ticker": ticker,
        "exchange": exchange,
        "date": today,
        "owner_name": safe_get(o, "name"),
        "owner_type": safe_get(o, "type"),
        "sharesHeld": safe_get(o, "sharesHeld"),
        "holdingDate": safe_get(o, "holdingDate"),
        "periodStartDate": safe_get(o, "periodStartDate"),
        "periodEndDate": safe_get(o, "periodEndDate"),
        "rankSharesHeld": safe_get(o, "rankSharesHeld"),
        "rankSharesSold": safe_get(o, "rankSharesSold")
    } for o in company.get("owners", [])]


def flatten_insider_transactions(company, ticker, exchange, today):
    return [{
        "ticker": ticker,
        "exchange": exchange,
        "date": today,
        "owner_name": safe_get(t, "ownerName"),
        "owner_type": safe_get(t, "ownerType"),
        "type": safe_get(t, "type"),
        "description": safe_get(t, "description"),
        "tradeDateMin": safe_get(t, "tradeDateMin"),
        "tradeDateMax": safe_get(t, "tradeDateMax"),
        "shares": safe_get(t, "shares"),
        "priceMin": safe_get(t, "priceMin"),
        "priceMax": safe_get(t, "priceMax"),
        "transactionValue": safe_get(t, "transactionValue"),
        "percentageSharesTraded": safe_get(t, "percentageSharesTraded"),
        "percentageChangeTransShares": safe_get(t, "percentageChangeTransShares"),
        "isManagementInsider": safe_get(t, "isManagementInsider"),
        "filingDate": safe_get(t, "filingDate")
    } for t in company.get("insiderTransactions", [])]


def flatten_members(company, ticker, exchange, today):
    return [{
        "ticker": ticker,
        "exchange": exchange,
        "date": today,
        "age": safe_get(m, "age"),
        "name": safe_get(m, "name"),
        "title": safe_get(m, "title"),
        "tenure": safe_get(m, "tenure"),
        "compensation": safe_get(m, "compensation")
    } for m in company.get("members", [])]

def process_companies_to_csv(df, today, base_path, QUERY_COMPANY_BY_ID, url, headers):
    companies = []

    for company_id in df["id"]:
        variables = {"id": company_id}
        response = requests.post(url, headers=HEADERS, json={"query": QUERY_COMPANY_BY_ID, "variables": variables})
        data = response.json()

        if response.status_code == 200 and data.get("data") and data["data"].get("company"):
            companies.append(data["data"]["company"])
        else:
            logging.warning(f"⚠️ Skipped ID {company_id} due to error: {data.get('errors') or response.status_code}")

    # Flattening and saving
    statements_data, listings_data, owners_data, insider_transactions_data, members_data = [], [], [], [], []

    for company in companies:
        ticker = safe_get(company, "tickerSymbol", "")
        exchange = safe_get(company, "exchangeSymbol", "")

        statements_data.extend(flatten_statements(company, ticker, exchange, today))
        listings_data.extend(flatten_listings(company, ticker, exchange, today))
        owners_data.extend(flatten_owners(company, ticker, exchange, today))
        insider_transactions_data.extend(flatten_insider_transactions(company, ticker, exchange, today))
        members_data.extend(flatten_members(company, ticker, exchange, today))

        print(f"✅ Processed and saved data for {company_id} .")
    # Save all to CSV in a folder named 'All_Exchanges' (or change logic if needed)
    exchange_folder = os.path.join(base_path, "All_Exchanges")
    create_directory(exchange_folder)

    save_to_csv(listings_data, os.path.join(exchange_folder, f"Listings_{today}.csv"))
    save_to_csv(owners_data, os.path.join(exchange_folder, f"Owners_{today}.csv"))
    save_to_csv(insider_transactions_data, os.path.join(exchange_folder, f"Insider_Transactions_{today}.csv"))
    save_to_csv(members_data, os.path.join(exchange_folder, f"Members_{today}.csv"))
    save_to_csv(statements_data, os.path.join(exchange_folder, f"Statements_{today}.csv"))

    print(f"✅ Processed and saved data for {len(companies)} companies.")

def main():
    df = pd.read_csv(exchanges_file)
    process_companies_to_csv(df, TODAY, base_path, QUERY_COMPANY_BY_ID, BASE_URL, HEADERS)

if __name__ == "__main__":
    main()
