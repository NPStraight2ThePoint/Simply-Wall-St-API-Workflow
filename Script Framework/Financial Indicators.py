# Framework for retreiving all Financial Indicators

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

# Database connection
# Simply API setup

# Read the CSV file

for Exchange in df1["exchange"].dropna().unique():  # Exclude NaN values
    # Filter matching rows
    # Ensure there's at least one match before accessing index 0
 
    print(f"🚀 Starting data fetch for {Exchange}...")
    print(f"Companies count: {companies_count}")

    # Check and create directories if they don't exist
    # Check if the folder exists
    if not os.path.exists(Company_Statements_path):
        # Create the folder
        
    # Configuration
    # Max API retry attempts
    # Normal batch step size
    # Start fetching from the first company
    # Ensure correct file path
    # Write headers only if the file does not exist

    while offset < companies_count:
        # Remaining_items
        # Adjust step size
        # Reset retry counter
        # Track batch success
        # Track offsets that need incremental retries

        while not success and retries < max_retries:
            try:
                print(f"🔍 Fetching Statements offset {offset} with {fetch_step} items for {Exchange}...")

                # Define GraphQL query
                query = """
                    query ($exchange: String!, $limit: Int!, $offset: Int!) {
                        companies(exchange: $exchange, limit: $limit, offset: $offset) {
                            id
                            exchangeSymbol
                            tickerSymbol
                            statements {
                                name
                                title
                                area
                                type
                                value
                                outcome
                                description
                                state
                                severity
                                outcomeName
                            }
                        }
                    }
                """

                # Send API request
                variables = {"exchange": Exchange, "limit": fetch_step, "offset": offset}
                response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
                response.raise_for_status()  # Handle HTTP errors
    
                # Parse response
               
                if not companies:
                    print("❌ No companies found, moving to next batch...")
                    offset += fetch_step
                    break  # Skip to next batch

                flattened_data = []
                for company in companies:
                    ticker = company.get("tickerSymbol", "")
                    for statement in company.get("statements", []):
                        flattened_data.append({
                            "ticker": ticker,
                            "exchange": Exchange,
                            "date": today,
                            "name": statement.get('name'),
                            "title": statement.get('title'),
                            "area": statement.get('area'),
                            "type": statement.get('type'),
                            "value": statement.get('value'),
                            "description": statement.get('description'),
                            "state": statement.get('state'),
                            "severity": statement.get('severity'),
                            "outcomename": statement.get('outcomeName')  # Fixed column name here
                        })

                # Save to CSV
                    # Check if the file exists for the first time
                    # Open the file in append mode for subsequent batches
                        # Write headers only if the file is being created (i.e., it's the first batch)
                             # Set to False to prevent future header writes
                        # Write the batch data
                else:
                    print("No statements to save.")

                # Load data into DataFrame and rename columns
        
                print(f"✅ Company statements successfully saved for {Exchange}.")

                # Move to next batch
                offset += fetch_step
                success = True

            except requests.exceptions.RequestException as e:
                print(f"⚠️ API Request failed: {e}")
                retries += 1
                if retries == max_retries:
                    print(f"❌ Max retries reached. Storing failed offset: {offset}")
                    # Track failed batch

        # Handle failed offsets with incremental retries
        if failed_offset is not None:
            print(f"🔄 Retrying failed batch incrementally from offset {failed_offset}...")
            for retry_offset in range(failed_offset, failed_offset + fetch_step):
                try:
                    #Retry Batch ....

                except requests.exceptions.RequestException as e:
                    print(f"⚠️ Failed incremental retry at offset {retry_offset}: {e}")


import runpy
from Statements_Columns import COPY_COLUMNS, COPY_COLUMNS2

# Ensure columns are properly formatted in the query
columns_str = ",\n    ".join(COPY_COLUMNS)
all_columns = ",\n        ".join(COPY_COLUMNS2)

#Merge and Transpose to final Joined CSV
runpy.run_path("Statements_Transpose.py")  # Runs the script in the current directory

# SQL Load

# Create table query
# Execute the query to create the table
# Import CSV into the correct schema and table
# SQL query to drop the temporary table
# Commit the changes to the database

print(f"Transposed_merged_output_Statements_{today}.csv imported successfully into simply_api_raw_data.company_statements!")
