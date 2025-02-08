# Simply-Wall-St-API-Workflow
This repository demonstrates the creation of a data pipeline that retrieves financial data from the Simply Wall St API, processes, cleans and stores the data in a PostgreSQL database . The pipeline showcases an end-to-end workflow that integrates data acquisition, transformation and application of stock attribution analysis.

The project is built using Python, PostgreSQL, Pandas, Excel and Simply Wall St API .

How It Works

1. Data Retreival / Cleansing / Storing
   
   3 Main Python scripts that extract all available API data via GraphQL queries for all or specific exchanges and all companies in each.
   Data is retreived in json files which is then flattened/cleansed and transformed into dataframes via a variety of methods.
   Once dataframes ready they are inserted into PostgreSQL DB taking into consideration DB/tables schemas ,unique constraints and conflict 
   handling. API and SQL DB column headers are being mapped accordingly within python scripts so that data is inserted approprietly. 
     
2. Data validity checks / SQL procedures
   
   ● Check dublicate or null rows exist.
   ● Check expected number of tickers retreived / reconciling CompanyCount vs actual total tickers retreived.
   ● Transpose company_statements table appropriately to implement 'Snowflake' attribution analysis.

3. 'Snowflake' attribution analysis.

   ● Query data from SQL and store it in a formulated excel spreadsheet.
   ● Display stock rankings based on Snowflake attributions.
   ● Filter / sort based on stock rankings and sectors.

Key Python Script Parts

1.Exchanges&Counts.py / Retreive list of all exchanges and number of tickers for each one .

# Libraries
import pandas as pd
from datetime import datetime
import requests
import os
import csv
from sqlalchemy import create_engine
from sqlalchemy import text

# PostgreSQL connection
  ...
  engine = create_engine(db_url)
  
# Simply API connection
  ... 
  # GraphQL
  query = """query { exchanges{symbol companiesCount}}"""

#Query Response
response = requests.post(url, headers=headers, json={"query": query})
data = response.json()
df = pd.DataFrame(data)

# Preparing json for data flattening
# Add date column at position 0 for all rows
# Create a DataFrame from the list of dictionaries
# Rename columns to match SQL table columns
# Reorder columns to match SQL table column order
# Insert or update in PostgreSQL
with engine.begin() as conn:
    for _, row in df.iterrows():
        conn.execute(
            text("""
                  INSERT INTO simply_api_raw_data.exchanges_counts (index_date, exchange, company_count)
                  VALUES (:index_date, :exchange, :company_count)
                  ON CONFLICT (index_date, exchange) DO UPDATE
                  SET company_count = EXCLUDED.company_count;
              """),
            {
                "index_date": row["index_date"],
                "exchange": row["exchange"],
                "company_count": row["company_count"]
            }
        )

# Final SQL table exported in CSV

index_date	exchange	  company_count
8/02/2025	  DB	        17469
8/02/2025	  OTCPK	      15599
8/02/2025	  LSE	        8725
8/02/2025	  BATS-CHIXE	6822
8/02/2025	  BSE	        4940
8/02/2025	  TSE	        4563
8/02/2025	  XTRA	      3677
8/02/2025	  SZSE	      3532
....        ...         ...

2.Get_Data.py / Get tickers & other info for selected exchanges

# Libraries
from Get_Tickers import fetch_data # ✅ Import the function
import pandas as pd
from sqlalchemy import create_engine
import time
import requests

# List of exchanges
Exchanges = ["TWSE", "NYSE", "NasdaqCM", "NasdaqGM", "NasdaqGS"]

for Exchange in Exchanges:
fetch_data(Exchange)  # ✅ Calls fetch_data
...
def fetch_data(Exchange):
    """Function to fetch data for a given exchange."""

    step = 100  # Pagination step
    offset = 0  # Initial offset
    all_results = []  # Store all fetched records

    while True:
        try:
            query = """query($exchange: String!, $limit: Int!, $offset: Int!) {companies(exchange: $exchange, limit: $limit, offset: $offset) {
                       id  name tickerSymbol classificationStatus marketCapUSD}}"""

            variables = {"exchange": Exchange, "limit": step, "offset": offset}

            # Send request
            response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
            data = response.json()

            # Check if 'data' and 'companies' exist in response
            # If no data returned, break the loop
            # Convert to DataFrame
            # Add missing 'exchange' column
            # Reorder and rename columns
            # Store results

            # Insert or update data in PostgreSQL
                with engine.begin() as conn:
                    for _, row in flattened_data.iterrows():
                        conn.execute(
                            text("""
                                   INSERT INTO simply_api_raw_data.exchanges_tickers (exchange, name, ticker, id, classification_status, market_cap_usd)
                                   VALUES (:exchange, :name, :ticker, :id, :classification_status, :market_cap_usd)
                                   ON CONFLICT (exchange, ticker, id) DO UPDATE
                                   SET exchange = EXCLUDED.exchange,
                                       name = EXCLUDED.name,
                                       ticker = EXCLUDED.ticker,
                                       market_cap_usd = EXCLUDED.market_cap_usd,
                                       classification_status = EXCLUDED.classification_status;
                                      .....

            # Check if we reached the last page
            # Increment offset
            # Optional delay to avoid rate limits
           
# Final SQL table exported in CSV

exchange	name	                ticker id	                                  classification_status	market_cap_usd
ASX	      Ansell	              ANN	   25ece3b4-dc77-4d46-980c-b3eda5233274	ACTIVE	              3174886131
ASX	      Advance ZincTek	      ANO	   5a642809-aaef-4911-831d-77c2e016c3b1	ACTIVE	              30014488.19
ASX	      Anatara Lifesciences	ANR	   9f371156-6513-4fec-a0d2-91aca59b1b29	ACTIVE	              7549833.144
ASX	      Anax Metals	          ANX	   06a27ec2-7736-4b1d-a698-f67583684514	ACTIVE	              6057025.543
ASX	      ANZ Group Holdings	  ANZ	   213a0983-44a8-497f-bda5-ea652181583b	ACTIVE	              57863985237
...       ...                   ...    ...                                  ...                   ...

3.Get_CompanyInfo.py / Retreive a variety of financial indicators & metrics for a list of tickers / exchanges.

# Libraries
import requests
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import csv
import os
import time

# Opt-in to the future behavior to silence warning(s)
# Set date variables
# PostgreSQL connection
# SQL Query to get all exchanges / Adjust below accordingly
query_exchanges = "SELECT exchange FROM simply_api_raw_data.exchanges_counts WHERE exchange = 'NYSE';"

# Loop through each exchange and fetch stock data for active stocks excluding ETFs

query_tickers = text("""
        SELECT * 
        FROM simply_api_raw_data.exchanges_tickers
        WHERE exchange = :exchange
        AND NOT (
    classification_status <> 'ACTIVE'
    OR name LIKE '%ETF%'
    OR name LIKE '%Exchange Traded Fund%'
    OR market_cap_usd = 0 )""")

    tickers_df = pd.read_sql(query_tickers, engine, params={"exchange": exchange})

    # Loop through each ticker and make API requests
    for _, ticker_row in tickers_df.iterrows():
        ticker = ticker_row['ticker']
        # Perform the API call or any other logic here
        query = """query($exchange: String!, $tickerSymbol: String!) {companyByExchangeAndTickerSymbol(exchange: $exchange, tickerSymbol: $tickerSymbol) {
                    id  exchangeSymbol tickerSymbol name marketCapUSD  primaryIndustry .....  }}"""

        variables = {"tickerSymbol": ticker, "exchange": exchange}
        # Send the API request
        try:
            # Make API request
            # Extract company information safely
            # Extract closing prices safely
            # Get the first closing price, default to 0 if missing
            # Prepare flattened data for SQL insertion
            # Create a DataFrame for inserting into SQL
            # Insert into SQL table, updating if ticker, exchange, and date are the same #--->CONFLICT
               query = text("""
                 INSERT INTO simply_api_raw_data.company_info (
                    id, date, exchange_symbol, ticker_symbol, name, 
                    market_cap_usd, primary_industry, secondary_industry, 
                    tertiary_industry, market, market_iso2, closing_prices ) VALUES (
                    :id, :date, :exchange_symbol, :ticker_symbol, :name, 
                    :market_cap_usd, :primary_industry, :secondary_industry, 
                    :tertiary_industry, :market, :market_iso2, :closing_prices )
                ON CONFLICT (date, ticker_symbol, exchange_symbol) 
                DO NOTHING;  """)

          # Use `engine.begin()` to handle transactions automatically
            with engine.begin() as conn:
                conn.execute(query, df.to_dict(orient="records")[0])

          # Assuming `data` is the response from the GraphQL query
          # Check if insider transactions are found
          # Add ticker and exchange to the flattened transactions before inserting
          # Convert to DataFrame
          # SQL Insert Query with ON CONFLICT Handling

          # Flatten the transactions into a list of dictionaries
          # Get all keys as header from the first transaction
          # Transpose the data dynamically, setting 'title' as the new column headers
            df_transposed = df.pivot_table(
                    index=["Ticker"],  # Group by Ticker
                    columns=["area", "name"],  # Use 'area' and 'name' as new column headers
                    values=["value", "description"],  # Include 'value' and 'description' columns
                    aggfunc="first",  # Handle duplicates by taking the first value
                    fill_value=""  # Fill NaNs with an empty string or any placeholder)

          # Flatten the multi-index columns with desired format
          # Reset index for cleaner output
          # Add 'Exchange' and 'Date' columns after 'Ticker'
          # Reorder columns to make sure 'Ticker', 'Exchange', 'Date' come first
          # Ensure column names are lowercase
          # Load mapping API2SQL
          # Rename DataFrame columns
          # Drop N/A columns
          # Explicitly call infer_objects to ensure correct data types are inferred
          # Insert into SQL
           
# Final SQL table exported in CSV

# Company Info
(https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-08%20215355.png?raw=true)

# Insider transactions
(https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot 2025-02-08 221649.png?raw=true)
# Company Statements
(https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot 2025-02-09 083838.png?raw=true)
# Company members
(https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot 2025-02-09 084252.png?raw=true)
# Company owners
(https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot 2025-02-09 084500.png?raw=true)

Snowflake Attribution Analysis

Calling below SQL queries via Python :

import psycopg2
import pandas as pd

# Define queries
queries = {
    "exchanges_counts": "SELECT * FROM simply_api_raw_data.exchanges_counts;",
    "exchanges_tickers": "SELECT * FROM simply_api_raw_data.exchanges_tickers;",
    "company_info": "SELECT * FROM simply_api_raw_data.company_info;",
    "insider_transactions": "SELECT * FROM simply_api_raw_data.insider_transactions;",
    "company_statements": "SELECT * FROM simply_api_raw_data.company_statements;",
    "company_members": "SELECT * FROM simply_api_raw_data.company_members;",
    "company_owners": "SELECT * FROM simply_api_raw_data.company_owners;"
}

EXCEL_FILE = "output_data.xlsx"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_PARAMS)

    with pd.ExcelWriter(EXCEL_FILE, engine="xlsxwriter") as writer:
        for sheet_name, query in queries.items():
            df = pd.read_sql_query(query, conn)
            df.to_excel(writer, sheet_name=sheet_name, index=False)  # Save each DataFrame to a separate sheet


Final results after the SQL DB retreivals and attribution analysis filtering :

[Snowflake](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Snowflake Attribution Analysis.xlsx)


**Created by:** Nicholas Papadimitris
**Timestamp:** 2025-02-09 10:26 (UTC)  
**Unique ID:** [Simply-Wall-St-API-Workflow-2025-02-09 10:26]  


## Future Updates & Feedback  
This project is continuously evolving, and I plan to add more features and updates in the future.  

If you have any questions, suggestions, or feedback, feel free to reach out!  

**Author:** Nicholas Papadimitris
📧 Email: nicholas.papadimitris@gmail.com  
💼 LinkedIn: [Nicholas Papadimitris](https://www.linkedin.com/in/nicholas-papadimitris-82b7221a2/)

## Similar Projects Coming Soon  
I'm working on additional projects related to financial data pipelines, analytics, and investing insights. Stay tuned for more releases! 🚀  















                
          
               
            

                    
       
   
        
       
            
           
       
        
        







                      
                        
                       
                        
                        
                        
                      
                   
                    
            





  


  

