# Simply-Wall-St-API-Workflow

This repository demonstrates the creation of a data pipeline that retrieves financial data from the **Simply Wall St API**, processes, cleans and stores the data in a PostgreSQL database. The pipeline showcases an end-to-end workflow that integrates data acquisition, transformation, and application of stock attribution analysis.

The project is built using:
- **Python**
- **PostgreSQL**
- **Pandas**
- **Excel**
- **Simply Wall St API**

## How It Works

### 1. Data Retrieval / Cleansing / Storing

Three main Python scripts :
- Extract all available API data via GraphQL queries for all or specific exchanges and companies.
- Data is retrieved in JSON format, which is then flattened, cleansed, and transformed into dataframes using various methods.
- Once the dataframes are ready, they are inserted into the PostgreSQL database, considering table schemas, unique constraints, and conflict handling.
- API and SQL DB column headers are mapped within Python scripts to ensure proper data insertion.

### 2. Data Validity Checks / SQL Procedures

This step ensures the quality of the data:
- **Check for duplicate or null rows.**
- **Verify the expected number of tickers** retrieved by reconciling `CompanyCount` vs actual total tickers.
- **Transpose `company_statements` table** appropriately to implement **'Snowflake' attribution analysis**.

### 3. 'Snowflake' Attribution Analysis

In this step:
- Query data from the PostgreSQL database and store it in a formulated Excel spreadsheet.
- Display stock rankings based on **Snowflake** attributions.
- Filter and sort data based on stock rankings and sectors.

## Key Python Script Parts

### 1. Exchanges&Counts.py
This script retrieves a list of all exchanges and the number of tickers for each one.

### Libraries Used
```python
import pandas as pd
from datetime import datetime
import requests
import os
import csv
from sqlalchemy import create_engine, text

# Example of PostgreSQL connection
engine = create_engine(db_url)
  
# Example of GraphQL query to Simply Wall St API
query = """query { exchanges{symbol companiesCount}}"""
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
```

## Final SQL Table Exported to CSV

| index_date | exchange  | company_count |
|------------|-----------|---------------|
| 8/02/2025  | DB        | 17469         |
| 8/02/2025  | OTCPK     | 15599         |
| 8/02/2025  | LSE       | 8725          |
| 8/02/2025  | BATS-CHIXE| 6822          |
| 8/02/2025  | BSE       | 4940          |
| 8/02/2025  | TSE       | 4563          |
| 8/02/2025  | XTRA      | 3677          |
| 8/02/2025  | SZSE      | 3532          |

## 2. Get_Data.py - Get Tickers & Other Info for Selected Exchanges

This script fetches tickers and other information for selected exchanges using the `fetch_data` function.

### Libraries Used
```python
from Get_Tickers import fetch_data  # ✅ Import the function
import pandas as pd
from sqlalchemy import create_engine
import time
import requests

List of Exchanges
Exchanges = ["TWSE", "NYSE", "NasdaqCM", "NasdaqGM", "NasdaqGS"]

for Exchange in Exchanges:
    fetch_data(Exchange)  # ✅ Calls fetch_data for each exchange
...
Fetch Data Function
def fetch_data(Exchange):
    """Function to fetch data for a given exchange."""

    step = 100  # Pagination step
    offset = 0  # Initial offset
    all_results = []  # Store all fetched records

    while True:
        try:
            query = """query($exchange: String!, $limit: Int!, $offset: Int!) {
                           companies(exchange: $exchange, limit: $limit, offset: $offset) {
                               id
                               name
                               tickerSymbol
                               classificationStatus
                               marketCapUSD
                           }
                       }"""

            variables = {"exchange": Exchange, "limit": step, "offset": offset}

            # Send request to the API
            response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
            data = response.json()

            # Check if data and companies exist in response
            # Convert data to DataFrame and flatten if needed
            # Add 'exchange' column and reorder/rename columns
            # Insert or update data into PostgreSQL
            # Check if we reached the last page and increment offset
            # Optional delay to avoid rate limits
            # Error handling
```
                   
## Final SQL Table Exported to CSV

| exchange | name                     | ticker | id                                     | classification_status | market_cap_usd   |
|----------|--------------------------|--------|----------------------------------------|-----------------------|------------------|
| ASX      | Ansell                   | ANN    | 25ece3b4-                              | ACTIVE                | 3174886131       |
| ASX      | Advance ZincTek          | ANO    | 5a642809-                              | ACTIVE                | 30014488.19      |
| ASX      | Anatara Lifesciences     | ANR    | 9f371156-                              | ACTIVE                | 7549833.144      |
| ASX      | Anax Metals              | ANX    | 06a27ec2-                              | ACTIVE                | 6057025.543      |
| ASX      | ANZ Group Holdings       | ANZ    | 213a0983-                              | ACTIVE                | 57863985237      |
| ...      | ...                      | ...    | ...                                    | ...                   | ...              |

## 3.Get_CompanyInfo.py / Retreive a variety of financial indicators & metrics for a list of tickers / exchanges.

### Libraries Used
```python
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
```
          
# Final SQL table(s) exported in CSV

[Company Info](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-08%20215355.png)

[Insider Transactions](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-08%20221649.png?raw=true)

[Company Statements](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-09%083838.png)

[Company Members](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-09%084252.png)

[Company Owners](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-09%084500.png)

## Snowflake Attribution Analysis

Calling below SQL queries via Python:

```python
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
```

# Final results after the SQL DB retreivals and attribution analysis filtering :

[Snowflake Attribution Analysis](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Snowflake%20Attribution%20Analysis.xlsx)


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















                
          
               
            

                    
       
   
        
       
            
           
       
        
        







                      
                        
                       
                        
                        
                        
                      
                   
                    
            





  


  

