# 📈 SWS API ETL Pipeline - Summary

## 🚀 Overview

The goal of this ETL Pipeline is to 
- Retreive all available data for all exchanges/companies from SWS API.
- Transform & extract all valuable info into readable form.
- Store the clean data into a PostgreSQL DB.

The project is built using:
- **Python**
    Libraries : pandas, regex
- **PostgreSQL**
- **Simply Wall St API**

## 🔹 

### 1. ETL Process

* **Extract**  
  - **SWS API** Connection & data fetch.
                1.Exchanges & Counts
                2.Listings, Statements, Members, Owners, Insider Transactions
                          🔹1st Try Pagination Step 30 (Initial Retreival with max step)
                          🔹2nd Try Pagination Step 1  (Second Retreival with step 1 to identify failed items)
                          🔹3rd Try Pagination Step 1  (Final Retreival with step 1 to eliminate the possibility of a HTTP error)

* **Transform**  
  - Transform data for SQL Import
               1. Convert json responses into flattened dataframes based on data category
               2. Save flattened dataframes in CSV's
               3. Merge CSV'S
               4. Special Handling :
                         🔹Statements : Transpose rows to columns (API default response had indicators in rows so a transpose is required to match the DB table schema)
                         🔹 Insider_Transactions : 2nd ETL (To identify new unique data due to API response structure and lack of unique identifiers)
    
* **Pre Load QA** 
 - Count received vs expected data points , Log errors and final data points to be imported into SQL DB
   
* **Load** 
 -  Import data into SQL DB
   
* **Post Load QA**    
-   Transform Tickers/Exchanges to Uppercase
-   Delete Duplicate rows
-   Drop Temporary tables
-   Compare data points in DB vs what was expected to be imported to ensure data consistency & integrity
-   Lock data
-   Backup DB



