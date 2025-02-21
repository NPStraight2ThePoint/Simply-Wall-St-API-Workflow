import pandas as pd
import time
import requests
from datetime import datetime
import psycopg2
import csv
import os
import shutil

# Set date variables
today = datetime.now()
today = today.strftime("%Y-%m-%d")

# SQL DB connection
# Simply API connection

# Define function to fetch & save data
def fetch_data(Exchange):
        """Function to fetch paginated data for a given exchange and save to CSV."""
        
        folder_path = '...'

        # Check if the folder exists
        if not 
            # Create the folder
            
        # Define the CSV file
       
        # Set Loop parameters
        # Max API retry attempts
        # Normal step size
        # Start fetching from the first company
        # Write headers only on first write

        # Loop until page exceeds number of companies within the exchange
        while offset < companies_count:
            # Track Page - Companies ( to identify if it's the last page)
            # Normal batch size
            #Track failed offset
            # Track success

            while not success:
                try:
                    print(f"🔍 Fetching Tickers offset {offset} with {fetch_step} items for {Exchange}...")

                    query = """
                               query($exchange: String!, $limit: Int!, $offset: Int!) {
                                 companies(exchange: $exchange, limit: $limit, offset: $offset) {
                                   id
                                   name
                                   tickerSymbol
                                   classificationStatus
                                   marketCapUSD
                                 }
                               }
                               """
                    variables = {"exchange": Exchange, "limit": fetch_step, "offset": offset}
                    response = requests.post(url, headers=headers, json={"query": query, "variables": variables})

                    response.raise_for_status()  # Check HTTP status
                    data = response.json()

                        if not companies:  # No more data
                            print(f"✅ No more Tickers to fetch for {Exchange}.")
                            break

                        updated_companies = []
                        error_occurred = False

                        for company in companies:
                            try:
                                if company.get("classificationStatus") is None:
                                    company["classificationStatus"] = "Non Active"
                                company["exchange"] = Exchange
                                updated_companies.append(company)

                            except Exception as e:
                                print(f"⚠ Error in company {company.get('name', 'Unknown')}, retrying page: {e}")
                                error_occurred = True
                                break

                        if not error_occurred:
                            success = True
                            # ✅ Update last successful batch

                            # Write data to CSV
                              ....
                            print(
                                f"✅ Tickers for offset {offset}, limit {fetch_step} written to '{csv_file}' successfully.")

                   else:
                        print(f"⚠ No data received from API at offset {offset}. Marking for retry.")
                        failed_offset = offset
                        break  # Exit loop to retry with step 1

                except requests.exceptions.RequestException as e:
                    for attempt in range(1, max_retries + 1):
                        print(f"⚠ API error at offset {offset}, attempt {attempt}/{max_retries}: {e}")
                        time.sleep(2 ** attempt)
                        continue
                    print(f"❌ Persistent API error after {max_retries} attempts. Marking for retry.")
                    failed_offset = offset
                    break  # Exit loop to retry

            if failed_offset is not None:
                # ** Incrementally retry from the failed offset **
                print(f"🔄 Incrementally retrying from offset {failed_offset} with step 1...")

                for retry_offset in range(failed_offset, failed_offset + base_step):
                    try:
                        print(f"🔍 Fetching single item at offset {retry_offset}...")

                        #!!!!Retry Loop!!!!

                            print(f"✅ Successfully recovered item at offset {retry_offset}.")

                    except Exception as e:
                        print(f"⚠ Skipping item at offset {retry_offset} due to persistent error: {e}")
                        continue

                print(f"🔄 Recovery complete. Resuming normal batch processing at offset {failed_offset + base_step}.")
                # ✅ Move to next batch after retry

            else:
                # Move to next batch
                print(f"✅ Moving to next offset {offset}.")

#Exchanges = ["TWSE", "NYSE", "NasdaqCM", "NasdaqGM", "NasdaqGS"]  # List of exchanges
#Exchanges = ["DB"]

# Read the CSV file
....

for Exchange in df["exchange"].dropna().unique():  # Exclude NaN values
    # Retrieve the company count for the current exchange
    ....   
    print(f"🚀 Starting data fetch for {Exchange}...")
    print(f"Companies count: {companies_count}")

    fetch_data(Exchange)  # ✅ Calls fetch_data without triggering input()

    print(f"✅ Fetching complete for {Exchange}.")
    time.sleep(1)  # Sleep for 1 second to throttle requests

# Define the base path where Exchange folders are located

# List to store all DataFrames

# Loop through each exchange in the CSV
for exchange in df["exchange"].dropna().unique():  # Exclude NaN values
    # Exchange folder path
    # Full file path

    print(f"Checking: {ticker_path}")

    df_list = []
    # Flag to track if it's the first file

    # Ensure the directory exists
    if os.path.isdir(ticker_dir):
        # Ensure the file exists before trying to read
        if os.path.isfile(ticker_path):
            if is_first_file:
                # Read with headers on the first file
                
            else:
                # Read without headers on subsequent files
                # Optionally, you can set the column names manually if needed

            df_list.append(temp_df)
        else:
            print(f"File not found: {ticker_path}")  # Debugging message
    else:
        print(f"Directory not found: {ticker_dir}")  # Debugging message

# Merge all DataFrames
if df_list:
    ...
    print(f"Merging complete! Output saved as merged_output_Exchanges_Tickers_{today}.csv")
else:
    print("No files found for merging.")

# SQL query to create the temporary table

# Execute the query to create the table
# Import CSV to temporary table
# Insert INTO Formal From temporary
# ON CONFLICT ON CONSTRAINT -> DO 
# SQL query to drop the temporary table
# Commit the changes to the database

print("CSV imported successfully into simply_api_raw_data.exchanges_exchanges_tickers!")
