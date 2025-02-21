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

parent_folder = 'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Statements'  # Replace with your folder path

# Loop through all items in the parent folder
for item in os.listdir(parent_folder):
    item_path = os.path.join(parent_folder, item)

    # Check if the item is a directory (folder) and remove it
    if os.path.isdir(item_path):
        shutil.rmtree(item_path)  # Deletes the folder and all its contents
        print(f"Deleted folder: {item_path}")

csv_file_clear = f"C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Joined Data/merged_output_Statements_{today}.csv"
# Check if the file exists, then delete it
if os.path.exists(csv_file_clear):
    os.remove(csv_file_clear)

print("All folders deleted successfully.")

# Database connection
conn = psycopg2.connect(
    dbname="Simply_API",
    user="postgres",
    password="Arxidolemios39",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Simply API setup
url = "https://api.simplywall.st/graphql"
headers = {
    "Authorization": "Bearer sws:Y2VkM2QxYTEtOTA1Mi00ODY2LWIyY2MtNTgyMGFjOWZjMGQ3OmEyYWI1NGU5MDY3MzMyOTE=",
    "Content-Type": "application/json"
}



# Read the CSV file
df1 = pd.read_csv(f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Exchanges & Counts/Exchanges_Companies {today}.csv')  # Replace with your actual file path

#for Exchange in df1["exchange"]:
for Exchange in df1["exchange"].dropna().unique():  # Exclude NaN values
    # Filter matching rows
    filtered_values = df1.loc[df1["exchange"] == Exchange, "company_count"].values

    # Ensure there's at least one match before accessing index 0
    if len(filtered_values) > 0:
        companies_count = int(filtered_values[0])
    else:
        companies_count = 0  # Default value if no match

    #companies_count = df1.loc[df1["exchange"] == Exchange, "company_count"].values[0]
    #companies_count = int(companies_count)
    print(f"🚀 Starting data fetch for {Exchange}...")
    print(f"Companies count: {companies_count}")

    Company_Statements_path = f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Statements/{Exchange}'

    # Check and create directories if they don't exist
    os.makedirs(Company_Statements_path, exist_ok=True)

    # Check if the folder exists
    if not os.path.exists(Company_Statements_path):
        # Create the folder
        os.makedirs(Company_Statements_path)

    # Configuration
    max_retries = 3  # Max API retry attempts
    base_step = 50  # Normal batch step size
    offset = 0  # Start fetching from the first company
    csv_file = os.path.join(Company_Statements_path,f"{Exchange}_Statements_{today}.csv")  # Ensure correct file path
    write_headers = not os.path.exists(csv_file)  # Write headers only if the file does not exist

    while offset < companies_count:
        remaining_items = companies_count - offset
        fetch_step = min(base_step, remaining_items)  # Adjust step size
        retries = 0  # Reset retry counter
        success = False  # Track batch success
        failed_offset = None  # Track offsets that need incremental retries

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
                #print(response.json())
                # Parse response
                data = response.json().get('data', {})
                companies = data.get('companies', [])

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
                if flattened_data:
                    # Check if the file exists for the first time
                    write_headers = not os.path.exists(csv_file)

                    # Open the file in append mode for subsequent batches
                    mode = "w" if write_headers else "a"

                    with open(csv_file, mode=mode, newline="", encoding="utf-8") as file:
                        writer = csv.DictWriter(file, fieldnames=flattened_data[0].keys())

                        # Write headers only if the file is being created (i.e., it's the first batch)
                        if write_headers:
                            writer.writeheader()
                            write_headers = False  # Set to False to prevent future header writes

                        # Write the batch data
                        writer.writerows(flattened_data)
                else:
                    print("No statements to save.")

                # Load data into DataFrame and rename columns
                df = pd.read_csv(csv_file)
                print(df)
                df.rename(columns={'outcomeName': 'outcomename'}, inplace=True)

                print(f"✅ Company statements successfully saved for {Exchange}.")

                # Move to next batch
                offset += fetch_step
                success = True

            except requests.exceptions.RequestException as e:
                print(f"⚠️ API Request failed: {e}")
                retries += 1
                if retries == max_retries:
                    print(f"❌ Max retries reached. Storing failed offset: {offset}")
                    failed_offset = offset  # Track failed batch

        # Handle failed offsets with incremental retries
        if failed_offset is not None:
            print(f"🔄 Retrying failed batch incrementally from offset {failed_offset}...")
            for retry_offset in range(failed_offset, failed_offset + fetch_step):
                try:
                    variables = {"exchange": Exchange, "limit": 1, "offset": retry_offset}
                    response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
                    response.raise_for_status()
                    data = response.json().get('data', {})
                    companies = data.get('companies', [])

                    if not companies:
                        continue

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
                                "outcomename": statement.get('outcomeName')
                            })

                    if flattened_data:
                        # Check if the file exists for the first time
                        write_headers = not os.path.exists(csv_file)

                        # Open the file in append mode for subsequent batches
                        mode = "w" if write_headers else "a"

                        with open(csv_file, mode=mode, newline="", encoding="utf-8") as file:
                            writer = csv.DictWriter(file, fieldnames=flattened_data[0].keys())

                            # Write headers only if the file is being created (i.e., it's the first batch)
                            if write_headers:
                                writer.writeheader()
                                write_headers = False  # Set to False to prevent future header writes

                            # Write the batch data
                            writer.writerows(flattened_data)

                except requests.exceptions.RequestException as e:
                    print(f"⚠️ Failed incremental retry at offset {retry_offset}: {e}")


import runpy
from Statements_Columns import COPY_COLUMNS, COPY_COLUMNS2

# Ensure columns are properly formatted in the query
columns_str = ",\n    ".join(COPY_COLUMNS)
all_columns = ",\n        ".join(COPY_COLUMNS2)

runpy.run_path("Statements_Transpose.py")  # Runs the script in the current directory

# Change the current working directory
os.chdir('C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Joined Data')

csv_file = f"merged_output_Statements_{today}.csv"

# Create table query
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS temp_statements (
        {all_columns}
    );
"""

# Execute the query to create the table
cursor.execute(create_table_query)
conn.commit() # Commit the changes to the database


# Import CSV into the correct schema and table
copy_query = f"""
    COPY temp_statements (
        {columns_str}
    ) FROM STDIN WITH CSV HEADER
"""

with open(csv_file, "r") as file:
    next(file)  # Skip header row
    cursor.copy_expert(copy_query, file)

query = f"""
    INSERT INTO simply_api_raw_data.company_statements (
        {columns_str}
    )
    SELECT 
        {columns_str}
    FROM temp_statements
    ON CONFLICT ON CONSTRAINT unique_exchange_ticker_date
    DO NOTHING;
"""

cursor.execute(query)

conn.commit()

# SQL query to drop the temporary table
drop_table_query = "DROP TABLE IF EXISTS temp_statements;"
cursor.execute(drop_table_query) # Execute the query to drop the table

# Commit the changes to the database
conn.commit()
cursor.close()
conn.close()


print(f"Transposed_merged_output_Statements_{today}.csv imported successfully into simply_api_raw_data.company_statements!")