# ============================================================
# 📝 SCRIPT FUNCTION:
# ============================================================
# 🔄 Loops through all exchanges listed in:
#    📄  Exchanges_Companies {1st Day of Month}.csv'
#        
# 🔍 Queries available data for all companies/exchanges
#    ➝ Uses pagination step = 30.
#
# 📊 Flattens JSON responses into DataFrames
#    ➝ Saves as CSV per category type with the following structure:
#
# 📁 Data Storage Path:
#    'C:/.../Data/1.Try'
#
# 📌 CSV Naming Convention:
#    ├── * Exchange_Insider_Transactions_{1st Day of Month}.csv
#    ├── * Exchange_Listings_{1st Day of Month}.csv
#    ├── * Exchange_Members_{1st Day of Month}.csv
#    ├── * Exchange_Owners_{1st Day of Month}.csv
#    ├── * Exchange_Statements_{1st Day of Month}.csv
#
# 📜 Logs failed batches in:
#    🗂 'C:/.../Log.csv'
# ============================================================

# 📌 Import necessary modules
import os
from datetime import datetime
import csv
import pandas as pd
import logging
import requests

# Function to append csv
def append_to_csv(filename, exchange, start, end):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Append the data without writing headers
        writer.writerow([exchange, start, end])
    print(f"Appended to CSV: {exchange}, {start}, {end}")

# Function to create directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to save csv
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

# Function to create directory if not exists
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

query = """
            query Companies(
              $exchange: String!,
              $offset: Int!,
              $limit: Int!
            ) {
              companies(
                exchange: $exchange,
                offset: $offset,
                limit: $limit
              ) {
                id
                exchangeSymbol
                tickerSymbol
                name
                marketCapUSD
                primaryIndustry { name }
                secondaryIndustry { name }
                tertiaryIndustry { name }
                market { name iso2 }
                active
                classificationStatus
                insiderTransactions {
                      type
                      ownerName
                      ownerType
                      description
                      tradeDateMin
                      tradeDateMax
                      shares
                      priceMin
                      priceMax
                      transactionValue
                      percentageSharesTraded
                      percentageChangeTransShares
                      isManagementInsider
                      filingDate}
                statements {name
                            title
                            area
                            type
                            value
                            outcome
                            description
                            state
                            severity
                            outcomeName}
                members {age
                        name
                        title
                        tenure
                        compensation}
                owners {name
                        type
                        sharesHeld
                        holdingDate
                        periodStartDate
                        periodEndDate
                        rankSharesHeld
                        rankSharesSold}
                   }
            }
            """

# Function to fetch data from SWS API
def fetch_data(exchange, offset, limit, max_retries=3, backoff_factor=1):
    # Simply API setup
    .............
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
            '....../Log.csv',
            exchange, start, end)
        return []

# Function to safely get values with default fallback
def safe_get(data, key, default=None):
    try:
        if data is None:
            return default
        return data.get(key, default)
    except Exception as e:
        logging.error(f"Error accessing {key} in data: {data}. Error: {str(e)}")
        return default

# Main function to process data and save it to CSV
def process_and_save_data(exchange, offset, fetch_step, today):
    companies = fetch_data(exchange, offset, fetch_step)

    start = offset
    end = (offset + fetch_step)

    if not companies:
        print(f"❌ {exchange},{start},{end} No companies found, moving to next batch...")
        # !!!!Log Tracking Here!!!!
        append_to_csv('C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Data/7.Log/Log.csv', exchange, start, end)
        return offset + fetch_step

    listings_data = []
    owners_data = []
    insider_transactions_data = []
    members_data = []
    statements_data = []

    # Loop through each company and extract data
    for company in companies:
        ticker = safe_get(company, "tickerSymbol", "")

        for statement in company.get("statements", []):
            try:
                statements_data.append({
                    "ticker": ticker,
                    "exchange": exchange,
                    "date": today,
                    "name": safe_get(statement, 'name'),
                    "title": safe_get(statement, 'title'),
                    "area": safe_get(statement, 'area'),
                    "type": safe_get(statement, 'type'),
                    "value": safe_get(statement, 'value'),
                    "description": safe_get(statement, 'description'),
                    "state": safe_get(statement, 'state'),
                    "severity": safe_get(statement, 'severity'),
                    "outcomeName": safe_get(statement, 'outcomeName'),
                })
            except Exception as e:
                logging.error(f"Error processing statement for {ticker}: {str(e)}")

        try:
            listings_data.append({
                'id': safe_get(company, "id", ""),
                'date': pd.Timestamp.today().strftime('%Y-%m-%d'),
                'exchange_symbol': safe_get(company, "exchangeSymbol", ""),
                'ticker_symbol': safe_get(company, "tickerSymbol", ""),
                'name': safe_get(company, "name", ""),
                'market_cap_usd': safe_get(company, "marketCapUSD", 0),
                'primary_industry': safe_get(company.get("primaryIndustry", {}), "name", ""),
                'secondary_industry': safe_get(company.get("secondaryIndustry", {}), "name", ""),
                'tertiary_industry': safe_get(company.get("tertiaryIndustry", {}), "name", ""),
                'market': safe_get(company.get("market", {}), "name", ""),
                'market_iso2': safe_get(company.get("market", {}), "iso2", ""),
                'active': safe_get(company, "active", ""),
                'classification_status': safe_get(company, "classificationStatus", ""),
            })
        except Exception as e:
            logging.error(f"Error processing listings for {ticker}: {str(e)}")

        for owner in company.get("owners", []):
            try:
                owners_data.append({
                    "ticker": safe_get(company, "tickerSymbol", ""),
                    "exchange": safe_get(company, "exchangeSymbol", ""),
                    "date": today,
                    "owner_name": safe_get(owner, "name"),
                    "owner_type": safe_get(owner, "type"),
                    "sharesHeld": safe_get(owner, "sharesHeld"),
                    "holdingDate": safe_get(owner, "holdingDate"),
                    "periodStartDate": safe_get(owner, "periodStartDate"),
                    "periodEndDate": safe_get(owner, "periodEndDate"),
                    "rankSharesHeld": safe_get(owner, "rankSharesHeld"),
                    "rankSharesSold": safe_get(owner, "rankSharesSold")
                })
            except Exception as e:
                logging.error(f"Error processing owner data for {ticker}: {str(e)}")

        for transaction in company.get("insiderTransactions", []):
            try:
                insider_transactions_data.append({
                    "ticker": safe_get(company, "tickerSymbol", ""),
                    "exchange": safe_get(company, "exchangeSymbol", ""),
                    "date": today,
                    "owner_name": safe_get(transaction, "ownerName"),
                    "owner_type": safe_get(transaction, "ownerType"),
                    "type": safe_get(transaction, "type"),
                    "description": safe_get(transaction, "description"),
                    "tradeDateMin": safe_get(transaction, "tradeDateMin"),
                    "tradeDateMax": safe_get(transaction, "tradeDateMax"),
                    "shares": safe_get(transaction, "shares"),
                    "priceMin": safe_get(transaction, "priceMin"),
                    "priceMax": safe_get(transaction, "priceMax"),
                    "transactionValue": safe_get(transaction, "transactionValue"),
                    "percentageSharesTraded": safe_get(transaction, "percentageSharesTraded"),
                    "percentageChangeTransShares": safe_get(transaction, "percentageChangeTransShares"),
                    "isManagementInsider": safe_get(transaction, "isManagementInsider"),
                    "filingDate": safe_get(transaction, "filingDate")
                })
            except Exception as e:
                logging.error(f"Error processing insider transaction for {ticker}: {str(e)}")

        for member in company.get("members", []):
            try:
                members_data.append({
                    "ticker": safe_get(company, "tickerSymbol", ""),
                    "exchange": safe_get(company, "exchangeSymbol", ""),
                    "date": today,
                    "age": safe_get(member, "age"),
                    "name": safe_get(member, "name"),
                    "title": safe_get(member, "title"),
                    "tenure": safe_get(member, "tenure"),
                    "compensation": safe_get(member, "compensation")
                })
            except Exception as e:
                logging.error(f"Error processing member data for {ticker}: {str(e)}")

    base_path = f"C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Data/1.Try"
    # Create a folder for the exchange if it doesn't exist
    exchange_folder = os.path.join(base_path, exchange)
    create_directory(exchange_folder)

    save_to_csv(listings_data, os.path.join(exchange_folder, f"{exchange}_Listings_{today}.csv"))
    save_to_csv(owners_data, os.path.join(exchange_folder, f"{exchange}_Owners_{today}.csv"))
    save_to_csv(insider_transactions_data,os.path.join(exchange_folder, f"{exchange}_Insider_Transactions_{today}.csv"))
    save_to_csv(members_data, os.path.join(exchange_folder, f"{exchange}_Members_{today}.csv"))
    save_to_csv(statements_data, os.path.join(exchange_folder, f"{exchange}_Statements_{today}.csv"))

    return offset + fetch_step

# Main loop to process all exchanges in steps of 30
def main_loop():
    today = datetime.now().replace(day=1)
    today = today.strftime("%Y-%m-%d")

    df = pd.read_csv(f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Data/4.Exchanges_Counts/Exchanges_Companies {today}.csv')

    step_counter = 0

    for Exchange in df["exchange"].dropna().unique():  # Exclude NaN values
        companies_count = df.loc[df["exchange"] == Exchange, "company_count"].values[0]
        companies_count = int(companies_count)  # Ensure integer count
        print(f"🚀 Starting data fetch for {Exchange}...")
        print(f"Companies count: {companies_count}")

        # Loop for processing data in steps of 30
        for offset in range(0, companies_count, 30):
            step_counter += 1
            print(f"{Exchange}: Fetching companies {offset + 1} to {min(offset + 30, companies_count)}...")
            process_and_save_data(Exchange, offset, 30, today)
        print(f"✅ Fetching complete for {Exchange}.")

main_loop()

df = pd.read_csv('C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Data/7.Log/Log.csv')
df_cleaned = df.drop_duplicates()
df_cleaned.to_csv('C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Data/7.Log/Log.csv', index=False)

print("Duplicate rows removed and saved to 'Log.csv'")

today = datetime.now().replace(day=1)
today = today.strftime("%Y-%m-%d")

csv_file = 'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Data/7.Log/Log.csv'
exchanges_file = f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Data/4.Exchanges_Counts/Exchanges_Companies {today}.csv'

df = pd.read_csv(csv_file, header=None, names=['exchange', 'column2', 'column3'])
exchanges_df = pd.read_csv(exchanges_file, names=['index_date', 'exchange', 'company_count'])

# Reduce batch if it exceeds maximum count
df['column3'] = pd.to_numeric(df['column3'], errors='coerce')
exchanges_df['company_count'] = pd.to_numeric(exchanges_df['company_count'], errors='coerce')

for i, row in df.iterrows():
    exchange = row['exchange']
    matching_row = exchanges_df[exchanges_df['exchange'] == exchange]
    if not matching_row.empty:
        company_count = matching_row['company_count'].values[0]
        # Check if the third column exceeds the company_count, and if so, update it
        if row['column3'] > company_count:
            df.at[i, 'column3'] = company_count

df.to_csv('C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Data/7.Log/Log.csv', index=False, header=False)

print("CSV file updated successfully.")
