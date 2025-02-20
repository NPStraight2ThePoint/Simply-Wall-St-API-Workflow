# Simply-Wall-St-API-Workflow

## Overview
This repository demonstrates the creation of a data pipeline that retrieves financial data from the **Simply Wall St API**, processes, cleans, and stores the data in a PostgreSQL database and applies financial analysis.

The project is built using:
- **Python**
- **PostgreSQL**
- **Pandas**
- **Excel**
- **Simply Wall St API**

## How It Works

# Python API Queries
   * All Exchanges & Company counts
   * All Tickers under all Exchanges
   * Company Info (Sector(s), Market, MarketCap, Status) for all Tickers/Exchanges
   * Insider Transactions for all Tickers/Exchanges
   * Financial Indicators for all Tickers/Exchanges (130+)
   * Members for all Tickers/Exchanges
   * Owners for all Tickers/Exchanges
  
   # General ETL Process

   * API->JSON->DataFrame->Flattening/Cleansing->CSV
   * Merge/Transform CSV's->Joined CSV (API2SQL ETL Column Mapping)
   * Create SQL Temp Table->Copy CSV to SQL Temp Table->INSERT to Clean SQL Table -> On Conflict/Constraint handling->DROP Temp Table

   # Data QA
   * Data Integrity Validation -> Retry Queries -> Expected State achieved

   # Financial Analysis   
   * Export clean data -> Stock Attribution Analysis -> Final Watchlist

   # Visualisation
   * Power BI Visualisation



## Final SQL Tables

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

| exchange | name                     | ticker | id                                     | classification_status | market_cap_usd   |
|----------|--------------------------|--------|----------------------------------------|-----------------------|------------------|
| ASX      | Ansell                   | ANN    | 25ece3b4-                              | ACTIVE                | 3174886131       |
| ASX      | Advance ZincTek          | ANO    | 5a642809-                              | ACTIVE                | 30014488.19      |
| ASX      | Anatara Lifesciences     | ANR    | 9f371156-                              | ACTIVE                | 7549833.144      |
| ASX      | Anax Metals              | ANX    | 06a27ec2-                              | ACTIVE                | 6057025.543      |
| ASX      | ANZ Group Holdings       | ANZ    | 213a0983-                              | ACTIVE                | 57863985237      |
| ...      | ...                      | ...    | ...                                    | ...                   | ...              |

| id        | date  | exchange_symbol | ticker_symbol | name | market_cap_usd | primary_industry | secondary_industry | tertiary_industry | market | market_iso2 |
|---------------------------------------|------------|-----------------|---------------|------------------------------------------------|----------------|--------------------------|------
| 70e51eb9 | 19/02/2025 | ASX             | 14D           | 1414 Degrees                                  | 4348117.515    | Capital Goods            | Electrical        | Electrical Components and Equipment    | Australia | AU          |
| 867e8678- | 19/02/2025 | ASX             | 1AD           | AdAlta                                       | 6416845.886    | Pharmaceuticals & Biotech | Biotechs          | Biotechnology                         | Australia | AU          |
| ab60d5fb- | 19/02/2025 | ASX             | 1AE           | Aurora Energy Metals                          | 6027547.856    | Materials                | Metals and Mining | Diversified Metals and Mining         | Australia | AU          |
| 1794b0ff- | 19/02/2025 | ASX             | 1AG           | Alterra                                       | 2799178.135    | Food, Beverage & Tobacco | Food              | Agricultural Products                 | Australia | AU          |
| c6c4adb8- | 19/02/2025 | ASX             | 1AI           | Algorae Pharmaceuticals                      | 6435929.121    | Pharmaceuticals & Biotech | Biotechs          | Biotechnology                         | Australia | AU          |
| ac5900dd- | 19/02/2025 | ASX             | 1CG           | One Click Group                               | 8985154.771    | Commercial Services      | Professional Services | Research and Consulting Services   | Australia | AU          |
| 24c54267- | 19/02/2025 | ASX             | 1GOV          | Vaneck 1-5 Year Australian Government Bond ETF | 0              | Diversified Financials    | Capital Markets   | Asset Management and Custody Banks    | Australia | AU          |


### 2. Data Validity Checks / SQL Procedures

This step ensures the quality of the data:
- **Check for duplicate or null rows.**
- **Verify the expected number of tickers** retrieved by reconciling `CompanyCount` vs actual total tickers.
- **Transpose `company_statements` table** appropriately to implement **'Stock' attribution analysis**.

### 3. 'Stock' Attribution Analysis

This step includes:
- Quering data from the PostgreSQL database and store it in a formulated Excel spreadsheet.
- Display stock rankings based on stock attributions.
- Filter and sort data based on stock rankings and sectors.

         
# Final SQL table(s) exported in CSV

[Company Info](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-08%20215355.png)

[Insider Transactions](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-08%20221649.png?raw=true)

[Company Statements](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-09%20083838.png?raw=true)

[Company Members](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-09%20084252.png?raw=true)

[Company Owners](https://github.com/NPStraight2ThePoint/Simply-Wall-St-API-Workflow/blob/Simply-Wall-St-API-Pipeline/Test/Screenshot%202025-02-09%20084500.png?raw=true)

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

## Project Information

**Created by:** Nicholas Papadimitris  
**Timestamp:** 2025-02-09 10:26 (UTC)  
**Unique ID:** [Simply-Wall-St-API-Workflow-2025-02-09 10:26]


## Future Updates & Feedback  
This project is continuously evolving, and I plan to add more features and updates in the future.  

By sharing this work, I aim to show how to streamline your data workflow(s) and tranform them into useful insights. I'm open to feedback on its value, and if you’re interested in optimizing your workflows or improving your data processing, feel free to reach out. I'm more than happy to elaborate on any aspect of the project if you need more details!

**Author:** Nicholas Papadimitris  
📧 **Email:** nicholas.papadimitris@gmail.com  
💼 **LinkedIn:** [Nicholas Papadimitris](https://www.linkedin.com/in/nicholas-papadimitris/)

## Similar Projects Coming Soon  
I'm working on additional projects related to financial data pipelines, analytics, and investing insights. Stay tuned for more releases! 🚀  

## Disclaimer
API is still in beta, which means things are subject to change. Specs could be updated, limits might be introduced, paywalls added, or even certain features removed .
