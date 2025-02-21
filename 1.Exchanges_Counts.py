import requests
import pandas as pd
import csv
import os
from datetime import datetime
import psycopg2

# Set date variables
today = datetime.now()
today = today.strftime("%Y-%m-%d")

csv_file_clear = f'C:/
# Check if the file exists, then delete it
if os.path.exists(csv_file_clear):
    os.remove(csv_file_clear)

# Database connection
conn = psycopg2.connect(
    dbname="Simply_API",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

#Simply API setup
url = "https://api.simplywall.st/graphql"
headers = {
    "Authorization": "Bearer,
    "Content-Type": "application/json"
}
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
data = response.json()
df = pd.DataFrame(data)

# Preparing the json for data flattening
statements = data['data']['exchanges']

# Add the date column at position 0 for all rows
for statement in statements:
    statement["date"] = today  # Add the date key

# Change the current working directory
os.chdir('C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Exchanges & Counts')

# Define the CSV file
csv_file = f'Exchanges_Companies {today}.csv'

# Check if statements is not empty
if statements:
    # Rename headers before writing
    header_mapping = {
        "date": "index_date",
        "symbol": "exchange",
        "companiesCount": "company_count"
    }

    # Define correct header order
    final_headers = ["index_date", "exchange", "company_count"]

    # Write to CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write fixed headers
        writer.writerow(final_headers)

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
cursor.execute("""
    CREATE TEMP TABLE temp_exchanges_counts AS 
    TABLE simply_api_raw_data.exchanges_counts WITH NO DATA;
""")

# Step 2: Copy data from CSV into the temporary table
with open(csv_file, "r") as file:
    next(file)  # Skip header row
    cursor.copy_expert(
        "COPY temp_exchanges_counts (index_date, exchange, company_count) FROM STDIN WITH CSV",
        file
    )

# Step 3: Insert into the main table, ignoring conflicts
cursor.execute("""
    INSERT INTO simply_api_raw_data.exchanges_counts (index_date, exchange, company_count)
    SELECT index_date, exchange, company_count FROM temp_exchanges_counts
    ON CONFLICT ON CONSTRAINT unique_index_exchange
    DO NOTHING;
""")

# Commit changes
conn.commit()
cursor.close()
conn.close()

print(f'Exchanges_Companies {today}.csv imported successfully into simply_api_raw_data.exchanges_counts!')




