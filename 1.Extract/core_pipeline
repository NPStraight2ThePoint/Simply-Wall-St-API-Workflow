import logging
import pandas as pd
from csv_utils import *
from dir_utils import TODAY
from data_flattening_utils import *
import os
import requests
from env_utils import url,headers,query

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

def run_pipeline(Log_File, exchanges_file, fetch_step, base_path):
    print(f"📂 Running pipeline with log file: {Log_File}")
    print(f"📂 Using base path: {base_path}")
    print(f"🔄 Step size: {fetch_step}")

    os.makedirs(base_path, exist_ok=True)

    df = pd.read_csv(exchanges_file)
    step_counter = 0

    for Exchange in df["exchange"].dropna().unique():  # Exclude NaN values
        companies_count = int(df.loc[df["exchange"] == Exchange, "company_count"].values[0])
        logging.info(f"🚀 Starting data fetch for {Exchange}... Companies count: {companies_count}")

        for offset in range(0, companies_count, fetch_step):
            step_counter += 1
            logging.info(f"{Exchange}: Fetching companies {offset + 1} to {min(offset + fetch_step, companies_count)}...")
            process_and_save_data(Log_File, Exchange, offset, fetch_step, TODAY, base_path)

        logging.info(f"✅ Fetching complete for {Exchange}.")

    clean_log_file(Log_File, exchanges_file)

def run_pipeline2(log_file_1, log_file_2, TODAY, base_path):
    if not os.path.exists(log_file_1):
        print(f"❌ Log file not found: {log_file_1}")
        return
    log_df = pd.read_csv(log_file_1, header=None, names=["exchange", "start", "end"])

    for index, row in log_df.iterrows():
        exchange = row["exchange"]
        start_offset = row["start"]
        end_offset = row["end"]
        print(f"🚀 Processing {exchange}, batch {start_offset} to {end_offset}...")

        for offset in range(start_offset, end_offset, 1):  # Step size is 1
            print(f"{exchange}: Fetching company {offset + 1}...")
            process_and_save_data(log_file_2, exchange, offset, 1, TODAY, base_path)
        print(f"✅ Fetching complete for {exchange}, batch {start_offset} to {end_offset}.")

    df = pd.read_csv(log_file_2)
    df_cleaned = df.drop_duplicates()
    df_cleaned.to_csv(log_file_2, index=False)

    print("Duplicate rows removed and saved to 'Retry Log.csv'")

# Main function to process data and save it to CSV
def process_and_save_data(Log_File, exchange, offset, fetch_step, today, base_path):
    companies = fetch_data(exchange, offset, fetch_step, Log_File)

    start = offset
    end = (offset + fetch_step)

    if not companies:
        print(f"❌ {exchange},{start},{end} No companies found, moving to next batch...")
        # !!!!Log Tracking Here!!!!
        append_to_csv(Log_File, exchange, start, end)
        return offset + fetch_step

    statements_data = []
    listings_data = []
    owners_data = []
    insider_transactions_data = []
    members_data = []

    # Loop through each company and extract data using modularized functions
    for company in companies:
        ticker = safe_get(company, "tickerSymbol", "")

        statements_data.extend(flatten_statements(company, ticker, exchange, today))
        listings_data.extend(flatten_listings(company, ticker, exchange, today))
        owners_data.extend(flatten_owners(company, ticker, exchange, today))
        insider_transactions_data.extend(flatten_insider_transactions(company, ticker, exchange, today))
        members_data.extend(flatten_members(company, ticker, exchange, today))

    # Create a folder for the exchange if it doesn't exist
    exchange_folder = os.path.join(base_path, exchange)
    create_directory(exchange_folder)

    # Save the processed data to CSV files
    save_to_csv(listings_data, os.path.join(exchange_folder, f"{exchange}_Listings_{today}.csv"))
    save_to_csv(owners_data, os.path.join(exchange_folder, f"{exchange}_Owners_{today}.csv"))
    save_to_csv(insider_transactions_data, os.path.join(exchange_folder, f"{exchange}_Insider_Transactions_{today}.csv"))
    save_to_csv(members_data, os.path.join(exchange_folder, f"{exchange}_Members_{today}.csv"))
    save_to_csv(statements_data, os.path.join(exchange_folder, f"{exchange}_Statements_{today}.csv"))

    return offset + fetch_step

def fetch_data(exchange, offset, limit, log_file_path):

    variables = {"exchange": exchange, "limit": limit, "offset": offset}

    start = offset
    end = (offset + 30)

    try:
        response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
        response.raise_for_status()
        data = response.json().get('data', {})
        if not data:
            logging.error(f"❌ {exchange},{start},{end} Received None as response data.")
            return []
        return data.get('companies', [])
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ {exchange},{start},{end} Request failed: {e}")
        # !!!!Log Tracking Here!!!!
        append_to_csv(
            log_file_path,
            exchange, start, end)
        return []

def clean_log_file(log_file_path, exchanges_file_path):
    try:
        # Read the log file and exchanges file
        df = pd.read_csv(log_file_path, header=None, names=['exchange', 'column2', 'column3'])
        exchanges_df = pd.read_csv(exchanges_file_path, names=['index_date', 'exchange', 'company_count'])

        # Remove duplicates
        df_cleaned = df.drop_duplicates()
        df_cleaned.to_csv(log_file_path, index=False)
        logging.info("Duplicate rows removed and saved to 'Log.csv'")

        # Adjust batch ranges
        df['column3'] = pd.to_numeric(df['column3'], errors='coerce')
        exchanges_df['company_count'] = pd.to_numeric(exchanges_df['company_count'], errors='coerce')

        for i, row in df.iterrows():
            exchange = row['exchange']
            matching_row = exchanges_df[exchanges_df['exchange'] == exchange]
            if not matching_row.empty:
                company_count = matching_row['company_count'].values[0]
                if row['column3'] > company_count:
                    df.at[i, 'column3'] = company_count

        # Save the updated log file
        df.to_csv(log_file_path, index=False, header=False)
        logging.info("Batch ranges have been adjusted in Log_File.")

    except Exception as e:
        logging.error(f"Error cleaning log file: {str(e)}")
