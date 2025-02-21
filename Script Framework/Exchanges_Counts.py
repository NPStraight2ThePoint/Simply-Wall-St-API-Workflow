# Framework for retreiving All exchanges & their Company_Count

import requests
import pandas as pd
import csv
import os
from datetime import datetime
import psycopg2

# Set date variables
today = datetime.now()
today = today.strftime("%Y-%m-%d")

# SQL DB connection
# Simply API connection
# GraphQL Query
query = """
query {
 exchanges
    {symbol
    companiesCount}
}
"""
#Query Response
response = requests.post(url, headers=headers, json={"query": query})
print(f"🚀 Starting data fetch for Exchanges / Company_Counts...")

# Preparing the json for data flattening
# Add the date column at position 0 for all rows
# Define the CSV file
# Check if statements is not empty

    # Rename headers before writing
    header_mapping = {
        "date": "index_date",
        "symbol": "exchange",
        "companiesCount": "company_count"
    }

    # Define correct header order
    # Write to CSV

        # Write fixed headers
        # Write rows ensuring values are in the correct order
        for statement in statements:
            row = [
                statement.get("date", ""),
                statement.get("symbol", ""),
                statement.get("companiesCount", "")
            ]
            writer.writerow(row)

    print(f"CSV file '{csv_file}' created successfully with ordered headers!")
else:
    print("No data available to write.")

# Step 1: Create a temporary table (if not already created)
# Step 2: Copy data from CSV into the temporary table
# Step 3: Insert into the main table, ignoring conflicts
# Commit changes

print(f'Exchanges_Companies {today}.csv imported successfully into simply_api_raw_data.exchanges_counts!')




