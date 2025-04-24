# Script Descriptions

## ETL Steps

### `etl_1x_1_get_exchanges_counts.py`
- **Purpose:** Retrieve all exchanges and the number of companies trading in each.
- **Reasoning:** This is the main point of the project for determining the exchanges to query (paginated) and estimating the expected number of tickers.

### `etl_1x_2_get_companies.py`
- **Purpose:** Retrieve all companies' core data (e.g., Ticker, exchange, ID, active status, market cap, etc.).
- **Reasoning:** This step ensures the fastest possible way to gather a list of all companies expected to have data, minimizing failure risk.

### `etl_1x_3_get_all_data_3x.py`
- **Purpose:** Retrieve all available data for all companies using the maximum possible API limit (30).
- **Reasoning:** This step accounts for potential batch failures and logs failed batches to retry with a step-wise approach to isolate the failures.

### `etl_1x_4_transform.py`
- **Purpose:** Perform data transformations for"statements" data & identify new insider transactions to load into the database              
- **Reasoning:** Statements are vertically oriented by default so we need to transpose to match DB schema.
                 Insider transactions do not have unique identifiers so we need to perform a cross check process to ensure only new data are being processed.

### `etl_1x_5_load.py`
- **Purpose:** Loads the cleaned and transformed data into temporary SQL tables in the database.
- **Reasoning:** This step prepares the data for final quality checks and ensures we do not interfere with production database.

### `etl_2x_1_get_all_data_id.py`
- **Purpose:** Check if tickers are missing from table (comparing vs companies table) and retrieve missing data for those tickers using their IDs.
- **Reasoning:** Sometimes responses give non expected values which cause batch to fail thus queries need to be adjusted to bypass this.

### `etl_2x_2_transform.py`
- **Purpose:** Perform similar transformations as the initial process (e.g., transpose, identify insider transactions).
- **Reasoning:** Ensures consistency and integrity when handling additional data that might have failed during earlier attempts.

### `etl_2x_3_load.py`
- **Purpose:** Loads the second batch of data into the database after transformation.
- **Reasoning:** This step ensures that any missing data retrieved in the second attempt is loaded correctly into the database.

---

## Data Quality Assurance (QA)

### `data_qa_1_qa_1.py`
- **Purpose:** Queries the temporary database to check for duplicate rows and compares table counts with the main exchange counts table.
- **Reasoning:** Ensures data accuracy and consistency across all tables, ensuring completeness and no missing tickers.

### `data_qa_2_qa_2.py`
- **Purpose:** Tracks the number of insider transactions, owners, and members per ticker to monitor unusual movement.
- **Reasoning:** Helps track data changes over time and ensures consistency in the data.

### `data_qa_3_move_to_prod.py`
- **Purpose:** Moves clean data from the temporary database to the production database once QA passes.
- **Reasoning:** This step ensures that the final clean data is properly migrated into the production environment for further use.

### `data_qa_4_db_backup.py`
- **Purpose:** Backs up the production database and clears the temporary database to prepare for the next pipeline run.
- **Reasoning:** Ensures data safety and ensures that the pipeline can be restarted cleanly without conflicts.

### `data_qa_5_clean_dir.py`
- **Purpose:** Archives all files related to the pipeline run and prepares new files for the next run.
- **Reasoning:** Keeps the working directory clean and organized, ensuring the pipeline is ready for the next execution.
