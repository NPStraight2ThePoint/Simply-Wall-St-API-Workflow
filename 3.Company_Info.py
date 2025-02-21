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

parent_folder = 'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Company_Info'  # Replace with your folder path

# Loop through all items in the parent folder
for item in os.listdir(parent_folder):
    item_path = os.path.join(parent_folder, item)

    # Check if the item is a directory (folder) and remove it
    if os.path.isdir(item_path):
        shutil.rmtree(item_path)  # Deletes the folder and all its contents
        print(f"Deleted folder: {item_path}")


csv_file_clear = f"C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Joined Data/merged_output_Company_Info_{today}.csv"
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

# Opt-in to the future behavior to silence the warning
pd.set_option('future.no_silent_downcasting', True)

# Read the CSV file
df1 = pd.read_csv(f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Exchanges & Counts/Exchanges_Companies {today}.csv')  # Replace with your actual file path

#for Exchange in df1["exchange"]:
for Exchange in df1["exchange"].dropna().unique():  # Exclude NaN values
    companies_count = df1.loc[df1["exchange"] == Exchange, "company_count"].values[0]
    companies_count = int(companies_count)
    print(f"🚀 Starting Company_Info Data fetch for {Exchange}...")
    print(f"Companies count: {companies_count}")

    Company_info_path = f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Company_Info/{Exchange}'

    # Check and create directories if they don't exist
    os.makedirs(Company_info_path, exist_ok=True)

    csv_file = os.path.join(Company_info_path, f'{Exchange}_Tickers_{today}.csv')
    write_headers = not os.path.exists(csv_file)

    max_retries = 3  # Max API retry attempts
    base_step = 100  # Normal step size
    offset = 0  # Start fetching from the first company
    last_successful_offset = -1  # Track the last successful batch

    #csv_file = f"{Exchange}_Company_Info_data.csv"

    while offset < companies_count:
        remaining_items = companies_count - offset
        fetch_step = min(base_step, remaining_items)  # Normal batch size
        failed_offset = None  # Track failed offset
        success = False  # Track success

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
                df = pd.DataFrame(flattened_data)
                df.to_csv(csv_file, mode='a', index=False, header=write_headers)

                # Ensure headers are written only once
                write_headers = False

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


#df = pd.read_csv(f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Exchanges & Counts/Exchanges_Companies {today}.csv')
df = pd.read_csv(
    f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Exchanges & Counts/Exchanges_Companies {today}.csv',
    dtype={"ticker_symbol": str},  # Ensures ticker_symbol is read as a string
    keep_default_na=False  # Prevents "NA" from being treated as NaN
)
# Define the base path where Exchange folders are located
base_path = f"C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Company_Info"  # Update this with your actual base directory

# List to store all DataFrames
df_list = []

# Loop through each exchange in the CSV
#for exchange in df["exchange"]:
for exchange in df["exchange"].dropna().unique():  # Exclude NaN values

    ticker_dir = os.path.join(base_path, exchange)  # Exchange folder path
    file_name = f"{exchange}_Tickers_{today}.csv"
    ticker_path = os.path.join(ticker_dir, file_name)  # Full file path

    print(f"Checking: {ticker_path}")

    # Ensure the directory exists
    if os.path.isdir(ticker_dir):
        # Ensure the file exists before trying to read
        if os.path.isfile(ticker_path):
            temp_df = pd.read_csv(ticker_path,dtype={"ticker_symbol": str},  # Ensures ticker_symbol is read as a string
            keep_default_na=False)  # Prevents "NA" from being treated as NaN

            #temp_df["Exchange"] = exchange  # Add exchange column for reference
            df_list.append(temp_df)
        else:
            print(f"File not found: {ticker_path}")  # Debugging message
    else:
        print(f"Directory not found: {ticker_dir}")  # Debugging message

# Change the current working directory
os.chdir('C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/1.2 SimplyAPI_SQL_Pipeline/Joined Data')

csv_file = f"merged_output_Company_Info_{today}.csv"
# Merge all DataFrames
if df_list:
    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df.to_csv(csv_file, index=False)
    print(f"Merging complete! Output saved as merged_output_Company_Info_{today}.csv")
else:
    print("No files found for merging.")

# SQL query to create the temporary table
create_table_query = """
    CREATE TABLE IF NOT EXISTS temp_company_info (
        id UUID,
        date DATE,
        exchange_symbol TEXT,
        ticker_symbol TEXT,
        name TEXT,
        market_cap_usd NUMERIC,
        primary_industry TEXT,
        secondary_industry TEXT,
        tertiary_industry TEXT,
        market TEXT,
        market_iso2 TEXT   
    );
"""

# Execute the query to create the table
cursor.execute(create_table_query)
conn.commit() # Commit the changes to the database


# Convert the file to UTF-8 and override the original file
with open(csv_file, "r", encoding="ISO-8859-1") as f:
    content = f.read()

with open(csv_file, "w", encoding="utf-8") as f:
    f.write(content)

# Import CSV into PostgreSQL
with open(csv_file, "r", encoding="utf-8") as file:  # Now open in UTF-8
    next(file)  # Skip header row
    cursor.copy_expert(
        "COPY temp_company_info (id, date, exchange_symbol, ticker_symbol, name, market_cap_usd, primary_industry, secondary_industry, tertiary_industry, market, market_iso2) FROM STDIN WITH CSV",
        file
    )

cursor.execute("""
    INSERT INTO simply_api_raw_data.company_info (id, date, exchange_symbol, ticker_symbol, name, market_cap_usd, primary_industry, secondary_industry, tertiary_industry, market, market_iso2)
    SELECT id, date, exchange_symbol, ticker_symbol, name, market_cap_usd, primary_industry, secondary_industry, tertiary_industry, market, market_iso2
    FROM temp_company_info
    ON CONFLICT (ticker_symbol, exchange_symbol, date)
    DO NOTHING; 
""")

conn.commit()

# SQL query to drop the temporary table
drop_table_query = "DROP TABLE IF EXISTS temp_company_info;"
cursor.execute(drop_table_query) # Execute the query to drop the table

# Commit the changes to the database
conn.commit()
cursor.close()
conn.close()

print("CSV imported successfully into simply_api_raw_data.company_info!")
