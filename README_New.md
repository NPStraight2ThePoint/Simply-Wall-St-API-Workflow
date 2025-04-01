# 📈 SWS API ETL Pipeline

## 🚀 Overview

The goal of this ETL Pipeline is to:
- Retrieve all available data for all exchanges/companies from the **SWS API**.
- Transform and extract valuable information into a readable format.
- Store the clean data into a **PostgreSQL** database.

### Tools and Technologies
- **Python**  
  Libraries: `pandas`, `regex`
- **PostgreSQL**
- **Simply Wall St API**

---

## 🔹 ETL Process

### 1. **Extract**
- **SWS API Connection & Data Fetch**  
  The extraction process involves connecting to the **SWS API** and retrieving data for the following:
  - Exchanges & Counts
  - Listings, Statements, Members, Owners, Insider Transactions

**Pagination Strategy:**
  - **1st Try**: Use **Pagination Step 30** for the initial retrieval with the maximum step size.
  - **2nd Try**: Use **Pagination Step 1** for the second retrieval to identify any failed items.
  - **3rd Try**: Use **Pagination Step 1** for the final retrieval to eliminate potential HTTP errors.

---

### 2. **Transform**
- **Transform Data for SQL Import**
  1. Convert **JSON responses** into flattened dataframes based on the data category.
  2. Save flattened dataframes as **CSV files**.
  3. Merge the **CSV files** into a single dataset for easy import.
  4. **Special Handling**:
     - **Statements**: Transpose rows to columns (API's default response has indicators in rows, so a transpose is required to match the DB table schema).
     - **Insider Transactions**: Conduct a second ETL to identify new, unique data due to API response structure and lack of unique identifiers.

---

### 3. **Pre-Load QA**
- Count **received** vs **expected** data points.
- Log **errors** and ensure all data points are ready to be imported into the SQL database.

---

### 4. **Load**
- Import data into the **PostgreSQL database**.

---

### 5. **Post-Load QA**
- **Data Cleanup and Integrity Check**:
  - Transform **tickers** and **exchanges** to uppercase for consistency.
  - Delete **duplicate rows** to maintain data quality.
  - Drop **temporary tables** used for intermediate processing.
  - Compare **data points in the DB** against the expected imported data to ensure consistency and integrity.
- **Lock Data**: Finalize the data to prevent further changes.
- **Backup DB**: Ensure a backup of the database is made after the load process.

---

## ⚙️ Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SWS-API-ETL-Pipeline.git



