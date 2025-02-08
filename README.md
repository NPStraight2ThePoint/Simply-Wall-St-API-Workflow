# Simply-Wall-St-API-Workflow
This repository demonstrates the creation of a data pipeline that retrieves financial data from the Simply Wall St API, processes cleans and stores the data in a PostgreSQL database . The pipeline showcases an end-to-end workflow that integrates data acquisition, transformation, with end goal being to generate actionable financial insights.

The project is built using Python, PostgreSQL, Pandas and Simply Wall St API .

Key Features

●Retrieve financial data from the Simply Wall St API.
●Cleanse and process the raw financial data (e.g., handling missing values, data flattening).
●Store structured data in a PostgreSQL database.
●Query structured data & apply financial analysis.
●Demonstrate end-to-end data pipeline construction.

How It Works
1. Data Retrieval
The pipeline starts by fetching financial data from the Simply Wall St API. This data includes information about stocks, financial metrics, and other relevant data points.

2. Data Cleansing
Once the data is retrieved, it is cleansed to handle issues like missing values, incorrect data formats, and outliers. This step ensures that the data is in a usable format for further analysis.

3. Storing Data in PostgreSQL
After cleansing, the data is stored in a PostgreSQL database. This allows for efficient querying and further data analysis in future steps.

4. Financial analysis
Finally data is queried and stored in excel , conducting attribution analysis based on the snowflake components for a universe of stocks,
and creating a ranking system to filter stocks.

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

![Pipeline Overview](images/Screenshot 2025-02-08 215355.png)

                
          
               
            

                    
       
   
        
       
            
           
       
        
        







                      
                        
                       
                        
                        
                        
                      
                   
                    
            





  


  

