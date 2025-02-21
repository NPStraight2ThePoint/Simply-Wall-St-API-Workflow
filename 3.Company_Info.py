import requests
import pandas as pd
from datetime import datetime
import csv
import os
import time
import psycopg2
import shutil

# Set date variables
today = datetime.now()
today = today.strftime("%Y-%m-%d")

# Check if the file exists, then delete it
if os.path.exists(csv_file_clear):
    os.remove(csv_file_clear)

print("All folders deleted successfully.")

# Database connection
# Simply API setup

# Opt-in to the future behavior to silence the warning
# Read the CSV file
# Replace with your actual file path

for Exchange in df1["exchange"].dropna().unique():  # Exclude NaN values

    print(f"🚀 Starting Company_Info Data fetch for {Exchange}...")
    print(f"Companies count: {companies_count}")

    # Check and create directories if they don't exist
    os.makedirs(Company_info_path, exist_ok=True)

    csv_file = os.path.join(Company_info_path, f'{Exchange}_Tickers_{today}.csv')
    write_headers = not os.path.exists(csv_file)

    # Max API retry attempts
    # Normal step size
    # Start fetching from the first company
    # Track the last successful batch

    #csv_file = f"{Exchange}_Company_Info_data.csv"

    while offset < companies_count:
        remaining_items = companies_count - offset
         # Normal batch size
         # Track failed offset
         # Track success

        while not success:
            try:
                print(f"🔍 Fetching Company_Info offset {offset} with {fetch_step} items for {Exchange}...")

                query = """
                    query ($exchange: String!, $limit: Int!, $offset: Int!) {
                        companies(exchange: $exchange, limit: $limit, offset: $offset) {
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
                        }
                    }
                """
                variables = {"exchange": Exchange, "limit": fetch_step, "offset": offset}
                response = requests.post(url, headers=headers, json={"query": query, "variables": variables})

                response.raise_for_status()  # Raise error if status is not 200
                data = response.json()

                # Extract company information
                companies = data.get("data", {}).get("companies", [])

                flattened_data = []
                for company in companies:
                    try:
                        flattened_data.append({
                            'id': company.get("id", ""),
                            'date': pd.Timestamp.today().strftime('%Y-%m-%d'),
                            'exchange_symbol': company.get("exchangeSymbol", ""),
                            'ticker_symbol': company.get("tickerSymbol", ""),
                            'name': company.get("name", ""),
                            'market_cap_usd': company.get("marketCapUSD", 0),
                            'primary_industry': company.get("primaryIndustry", {}).get("name", ""),
                            'secondary_industry': company.get("secondaryIndustry", {}).get("name", ""),
                            'tertiary_industry': company.get("tertiaryIndustry", {}).get("name", ""),
                            'market': company.get("market", {}).get("name", ""),
                            'market_iso2': company.get("market", {}).get("iso2", ""),
                        })
                    except AttributeError as e:
                        print(f"⚠ Data parsing error at offset {offset}: {e}")
                        failed_offset = offset
                        break  # Exit processing this batch

                if failed_offset is not None:
                    break  # Trigger incremental retry

                # Convert to DataFrame and append to CSV
            
                # Ensure headers are written only once
                print(f"✅ Company_Info Data for offset {offset}, limit {fetch_step} written to '{csv_file}' successfully.")

                # Update offset tracking
                success = True
                last_successful_offset = offset
                offset += fetch_step  # Move to the next batch

            except (requests.exceptions.RequestException, AttributeError) as e:
                print(f"⚠ API or parsing error at offset {offset}: {e}")
                failed_offset = offset
                break  # Exit loop to retry with smaller steps

        if failed_offset is not None:
            print(f"🔄 Incrementally retrying from offset {failed_offset} with step 1...")

            for retry_offset in range(failed_offset, failed_offset + base_step):
                try:
                    print(f"🔍 Fetching single item at offset {retry_offset}...")

                    variables = {"exchange": Exchange, "limit": 1, "offset": retry_offset}
                    response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
                    response.raise_for_status()
                    data = response.json()

                    companies = data.get("data", {}).get("companies", [])
                    if not companies:
                        print(f"✅ No more Company_Info Data to fetch for {Exchange}.")
                        break

                    flattened_data = []
                    for company in companies:
                        flattened_data.append({
                            'id': company.get("id", ""),
                            'date': pd.Timestamp.today().strftime('%Y-%m-%d'),
                            'exchange_symbol': company.get("exchangeSymbol", ""),
                            'ticker_symbol': company.get("tickerSymbol", ""),
                            'name': company.get("name", ""),
                            'market_cap_usd': company.get("marketCapUSD", 0),
                            'primary_industry': company.get("primaryIndustry", {}).get("name", ""),
                            'secondary_industry': company.get("secondaryIndustry", {}).get("name", ""),
                            'tertiary_industry': company.get("tertiaryIndustry", {}).get("name", ""),
                            'market': company.get("market", {}).get("name", ""),
                            'market_iso2': company.get("market", {}).get("iso2", ""),
                        })

                    df = pd.DataFrame(flattened_data)
                    df.to_csv(csv_file, mode='a', index=False, header=False)

                    print(f"✅ Successfully recovered item at offset {retry_offset}.")

                except Exception as e:
                    print(f"⚠ Skipping item at offset {retry_offset} due to persistent error: {e}")
                    continue

            print(f"🔄 Recovery complete. Resuming normal batch processing at offset {failed_offset + base_step}.")
            offset = failed_offset + base_step

# Define the base path where Exchange folders are located
# List to store all DataFrames

# Loop through each exchange in the CSV
for exchange in df["exchange"].dropna().unique():  # Exclude NaN values
    
    # Exchange folder path
    # Full file path

    print(f"Checking: {ticker_path}")
    # Ensure the directory exists
     # Ensure the file exists before trying to read
       # Ensures ticker_symbol is read as a string
         # Prevents "NA" from being treated as NaN
          # Add exchange column for reference     
        else:
            print(f"File not found: {ticker_path}")  # Debugging message
    else:
        print(f"Directory not found: {ticker_dir}")  # Debugging message
# Merge all DataFrames
    print(f"Merging complete! Output saved as merged_output_Company_Info_{today}.csv")
else:
    print("No files found for merging.")

# SQL query to create the temporary table
# Execute the query to create the table
# Convert the file to UTF-8 and override the original file
# Import CSV into PostgreSQL
# SQL query to drop the temporary table
# Commit the changes to the database

print("CSV imported successfully into simply_api_raw_data.company_info!")
