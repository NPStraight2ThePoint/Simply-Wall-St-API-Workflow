# ETL Pipeline 

## Overview
This ETL (Extract, Transform, Load) pipeline automates the process of retrieving, transforming, and loading financial data from API into a PostgreSQL database. The pipeline is designed to make financial data processing and analysis easier by automating data flow, allowing for efficient querying, manipulation, and further analysis.

- **Extract**: Retrieves raw financial data from API using via Python.
- **Transform**: Cleanses and transforms the data, including flattening nested JSON structures, handling missing data and aligning data formats to the database schema.
- **Load**: Loads the transformed data into a PostgreSQL database, making it ready for analysis, querying and reporting.

## 🧰 Tech Stack

- **Language**: Python 🐍  
- **Database**: PostgreSQL 🐘  
- **Libraries Used**:
  - `pandas` — Data manipulation and Excel/csv operations
  - `requests` — API communication  
  - `sqlalchemy` — Database connection and ORM support  
  - `psycopg2` — PostgreSQL driver for Python  
  - `openpyxl` — Excel writing engine for `.xlsx` output  

# 📜 Script Descriptions

| Script                             | Purpose                                                                 | Reasoning                                                                         |
|----------------------------------- |-------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| `etl_1x_1_get_exchanges_counts.py` | Retrieve all exchanges and the number of companies in each.             | Determines exchanges to query and estimate expected number of tickers.            |
| `etl_1x_2_get_companies.py`        | Retrieve core company data (Ticker, exchange, ID, market cap, etc.).    | Fastest method to gather all expected tickers, reducing failure risk.             |
| `etl_1x_3_get_all_data_3x.py`      | Retrieve full data for all companies using max API batch limit.         | Handles batch failures and logs them for retry with step-wise isolation.          |
| `etl_1x_4_transform.py`            | Transform statements and identify new insider transactions.             | Transpose vertical data for DB compatibility; identify only new insider events.   |
| `etl_1x_5_load.py`                 | Load transformed data into temp SQL tables.                             | Keeps production DB safe during validation and transformation.                    |
| `etl_2x_1_get_all_data_id.py`      | Requery missing tickers using their unique IDs.                         | Fixes issues from failed responses by bypassing problematic records.              |
| `etl_2x_2_transform.py`            | Apply same transformations to second-pass data.                         | Maintains consistency in DB formatting and logic.                                 |
| `etl_2x_3_load.py`                 | Load newly retrieved data into DB.                                      | Ensures completeness by capturing what was missed in round 1.                     |
| `data_qa_1_qa_1.py`                | Check for duplicates and compare row counts across tables.              | Validates consistency and completeness of ingested data.                          |
| `data_qa_2_qa_2.py`                | Track insider activity (transactions, owners, members) per ticker.      | Detects unusual behavior and ensures tracking over time.                          |
| `data_qa_3_move_to_prod.py`        | Move validated data from temp to production DB.                         | Ensures only QA-passed data enters the production pipeline.                       |
| `data_qa_4_db_backup.py`           | Backup production DB and reset temp DB.                                 | Prepares environment for the next run and protects final dataset.                 |


### 🆔 Project Info

**Author:** *Nicholas Papadimitris*  
**Created on:** *05/04/2025 6:58 PM* (UTC)  
**Last modified:** *24/04/2025 9:20 PM* (UTC)   
**Project ID:** `SWS_ETL_05_Apr2025`  
**GitHub:** [My GitHub](https://github.com/NPStraight2ThePoint)

📧 **Email:** nicholas.papadimitris@gmail.com  
💼 **LinkedIn:** [Nicholas Papadimitris](https://www.linkedin.com/in/nicholas-papadimitris/)

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.






