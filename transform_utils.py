import pandas as pd
from pathlib import Path
from config.env_utils import *
from sqlalchemy import create_engine, text
import os
from datetime import datetime
import re

def transpose_csv(base_directories):
    for base_directory in base_directories:
        print(f"\U0001F50D Processing directory: {base_directory}")

        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if "statements" in file.lower() and file.endswith(".csv"):  # Filter statements CSV files
                    file_path = os.path.join(root, file)
                    print(f"\U0001F4C4 Processing: {file_path}")

                    try:
                        df = pd.read_csv(file_path)
                        required_columns = {'ticker', 'exchange', 'date', 'area', 'name', 'value', 'description'}
                        if not required_columns.issubset(df.columns):
                            print(f"⚠️ Missing required columns in {file_path}. Skipping transformation.")
                            continue  # Skip files that don't have the required columns

                        # Aggregate duplicate (ticker, exchange, date, area, name) before pivoting
                        df = df.groupby(['ticker', 'exchange', 'date', 'area', 'name'], as_index=False).agg({
                            'value': 'first',  # Adjust aggregation method if needed
                            'description': 'first'})

                        # Create new column names for pivoting
                        df['name_value'] = df['area'] + "_" + df['name'] + "_Value"
                        df['name_desc'] = df['area'] + "_" + df['name'] + "_Desc"

                        # Pivot tables for values and descriptions
                        df_value = df.pivot(index=['ticker', 'exchange', 'date'], columns='name_value', values='value')
                        df_desc = df.pivot(index=['ticker', 'exchange', 'date'], columns='name_desc',
                                           values='description')

                        # Merge both pivot tables
                        df_pivot = pd.concat([df_value, df_desc], axis=1).reset_index()

                        # Rename specific columns
                        df_pivot.columns = df_pivot.columns.str.replace(
                            "VALUE_IsGoodValueComparingPreferredMultipleToPeersAverageValue_Value",
                            "VALUE_IsGoodValueComparingPreferredMultipleToPeersAvgVal_Value")
                        df_pivot.columns = df_pivot.columns.str.replace(
                            "VALUE_IsGoodValueComparingPreferredMultipleToPeersAverageValue_Desc",
                            "VALUE_IsGoodValueComparingPreferredMultipleToPeersAvgVal_Desc")

                        today = datetime.now().replace(day=1).strftime("%Y-%m-%d")
                        output_csv = os.path.join(root, f"Transposed_{file.replace('.csv', '')}.csv")
                        df_pivot.to_csv(output_csv, index=False)

                        print(f"✅ Successfully transposed and saved: {output_csv}")
                    except Exception as e:
                        print(f"❌ Error processing {file}: {e}")

def merge_insider_transactions(base_directories, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for base_dir in base_directories:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                # Match any file that contains "_Insider_Transactions" (wildcard for exchange)
                if "_Insider_Transactions" in file and file.endswith(".csv"):
                    # Construct full file path
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")

                    df = pd.read_csv(file_path)

                    # Extract the exchange from the file name using regex (assuming exchange is the part before '_Insider_Transactions')
                    match = re.match(r"([A-Za-z0-9]+)_Insider_Transactions", file)
                    if match:
                        exchange = match.group(1)  # Get the exchange code (e.g., ASX, NASDAQ, etc.)
                    else:
                        continue  # Skip the file if the exchange part cannot be found

                    # Create the exchange folder if it doesn't exist
                    exchange_output_folder = os.path.join(output_dir, exchange)
                    os.makedirs(exchange_output_folder, exist_ok=True)

                    # Check if a merged file already exists for this exchange
                    merged_file_path = os.path.join(exchange_output_folder, f"Insider_Transactions_{exchange}.csv")

                    if os.path.exists(merged_file_path):
                        # If merged file exists, append the current file to it
                        merged_df = pd.read_csv(merged_file_path)
                        merged_df = pd.concat([merged_df, df], ignore_index=True)
                        merged_df.to_csv(merged_file_path, index=False)
                    else:
                        # If merged file doesn't exist, save the current file as the merged file
                        df.to_csv(merged_file_path, index=False)

    print("Merging complete.")

def fetch_and_save_data(db_params, exchanges, table_mappings, NEW_DATA, EXISTING_DATA):

    try:
        # Create SQLAlchemy engine
        connection_string = f"postgresql://{db_params['username']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
        engine = create_engine(connection_string)

        for exchange in exchanges:
            if exchange == 'NaN' or pd.isna(exchange):  # Skip NaN or 'NaN' exchanges
                print(f"❌ Skipping invalid exchange value: {exchange}")
                continue

            for table_name, file_name in table_mappings:
                # Update query to fetch all data where exchange matches
                query = f"SELECT * FROM {table_name} WHERE exchange = %s"
                print(f"Running query: {query}")  # Debugging print to check the query

                # Fetch data filtered by exchange
                exchange_data = pd.read_sql(query, engine, params=(exchange,))

                # Determine appropriate folder based on the table
                output_folder = Path(NEW_DATA if table_name == "insider_transactions_uat" else EXISTING_DATA) / exchange
                output_folder.mkdir(parents=True, exist_ok=True)

                # Save data to CSV
                file_path = output_folder / f"{file_name}_{exchange}.csv"
                exchange_data.to_csv(file_path, index=False)
                print(f"✅ Saved {file_path}")
    except Exception as e:
        print(f"❌ Error fetching and saving data: {e}")

def load_temp_SQL(directory, file_rules, db_connection):
    """
    Processes CSV files in the specified directory based on the provided rules.
    :param directory: The base directory containing subdirectories with CSV files.
    :param file_rules: A list of dictionaries defining rules for processing files.
    :param db_connection: The SQLAlchemy engine or connection string for SQL insertion.
    """
    for root, dirs, files in os.walk(directory):
        if root == directory:
            continue
        for file in files:
            for rule in file_rules:
                if rule["keyword"] in file.lower() and file.lower().endswith(".csv"):
                    file_path = os.path.join(root, file)
                    print(f"Processing: {file_path}")
                    try:
                        df = pd.read_csv(file_path, parse_dates=["date"], dayfirst=False)
                        for column in rule["columns"]:
                            if column in df.columns:
                                df[column] = df[column].astype(str).str.upper()
                            else:
                                print(f"⚠️ Column '{column}' not found in {file}. Skipping uppercase conversion.")
                        for col in df.select_dtypes(include=['object']).columns:
                            df[col] = df[col].astype(str).str.lower()

                        # Use SQLAlchemy engine for insertion
                        df.to_sql(rule["table"], db_connection, if_exists="append", index=False)
                        print(f"✅ Successfully inserted: {file} into {rule['table']}")
                    except Exception as e:
                        print(f"❌ Error processing {file}: {e}")

def update_columns_to_uppercase(db_params, table_name):
    try:
        # Get today's date in 'YYYY-MM-DD' format
        today = datetime.now().replace(day=1).strftime("%Y-%m-%d")

        # Create the SQLAlchemy engine with provided database parameters
        connection_string = f"postgresql://{db_params['username']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
        engine = create_engine(connection_string)

        # Define the query to update the 'exchange' and 'ticker' columns to uppercase
        query = f"""
            UPDATE {table_name} 
            SET exchange = UPPER(exchange), 
                ticker = UPPER(ticker)
            WHERE exchange IS NOT NULL 
                AND ticker IS NOT NULL
                AND date = '{today}';
        """

        # Execute the query
        with engine.connect() as conn:
            result = conn.execute(text(query))

            # Commit the transaction (SQLAlchemy will auto-commit for DML queries, but you can call commit explicitly if needed)
            conn.commit()

            # Print the number of rows updated
            print(f"✅ {result.rowcount} rows updated to uppercase in {table_name} where date = {today}.")

    except Exception as e:
        print(f"❌ Error executing query: {e}")

def find_unique_transactions(exchanges_csv, insider_folder, sql_folder):
    # Read exchanges from CSV, ensuring 'exchange' column is string and handling NaNs
    exchanges_df = pd.read_csv(exchanges_csv)
    exchanges_df['exchange'] = exchanges_df['exchange'].astype(str).str.strip()
    exchanges_df = exchanges_df.dropna(subset=['exchange'])
    exchanges = exchanges_df['exchange'].unique()

    for exchange in exchanges:
        new_file = os.path.join(insider_folder, exchange, f"New_Insider_Transactions_{exchange}.csv")
        existing_file = os.path.join(sql_folder, exchange, f"Existing_Insider_Transactions_{exchange}.csv")
        output_file = os.path.join(insider_folder, exchange, f"Unique_Insider_Transactions_{exchange}.csv")

        if not os.path.exists(new_file) or not os.path.exists(existing_file):
            print(f"Skipping {exchange}: One or both files missing")
            continue

        new_df = pd.read_csv(new_file)
        existing_df = pd.read_csv(existing_file)

        # Convert all values to string for consistent comparison
        new_df_str = new_df.astype(str)
        existing_df_str = existing_df.astype(str)

        # Drop 'date' only for comparison, keep full original new_df
        comparison_cols = [col for col in new_df_str.columns if col != 'date']
        new_subset = new_df_str[comparison_cols].copy()
        existing_subset = existing_df_str[comparison_cols].copy()

        # Add index to trace back to original new_df
        new_subset['__original_index__'] = new_subset.index

        # Merge to find rows only in new_subset
        merged = new_subset.merge(existing_subset, how='left', indicator=True)
        unique_indices = merged[merged['_merge'] == 'left_only']['__original_index__']

        # Get the full rows from original new_df
        final_unique = new_df.loc[unique_indices]

        if not final_unique.empty:
            final_unique.to_csv(output_file, index=False)
            print(f"Saved unique transactions for {exchange} in {output_file}")
        else:
            print(f"No unique transactions found for {exchange}")

def find_unique_transactions_id(exchanges_csv, insider_folder, sql_folder):
    # Read exchanges from CSV, ensuring 'exchange' column is string and handling NaNs
    exchanges_df = pd.read_csv(exchanges_csv)
    exchanges_df['exchangeSymbol'] = exchanges_df['exchangeSymbol'].astype(str).str.strip()
    exchanges_df = exchanges_df.dropna(subset=['exchangeSymbol'])
    exchanges = exchanges_df['exchangeSymbol'].unique()

    for exchange in exchanges:
        new_file = os.path.join(insider_folder, exchange, f"New_Insider_Transactions_{exchange}.csv")
        existing_file = os.path.join(sql_folder, exchange, f"Existing_Insider_Transactions_{exchange}.csv")
        output_file = os.path.join(insider_folder, exchange, f"Unique_Insider_Transactions_{exchange}.csv")

        if not os.path.exists(new_file) or not os.path.exists(existing_file):
            print(f"Skipping {exchange}: One or both files missing")
            continue

        new_df = pd.read_csv(new_file)
        existing_df = pd.read_csv(existing_file)

        # Convert all values to string for consistent comparison
        new_df_str = new_df.astype(str)
        existing_df_str = existing_df.astype(str)

        # Drop 'date' only for comparison, keep full original new_df
        comparison_cols = [col for col in new_df_str.columns if col != 'date']
        new_subset = new_df_str[comparison_cols].copy()
        existing_subset = existing_df_str[comparison_cols].copy()

        # Add index to trace back to original new_df
        new_subset['__original_index__'] = new_subset.index

        # Merge to find rows only in new_subset
        merged = new_subset.merge(existing_subset, how='left', indicator=True)
        unique_indices = merged[merged['_merge'] == 'left_only']['__original_index__']

        # Get the full rows from original new_df
        final_unique = new_df.loc[unique_indices]

        if not final_unique.empty:
            final_unique.to_csv(output_file, index=False)
            print(f"Saved unique transactions for {exchange} in {output_file}")
        else:
            print(f"No unique transactions found for {exchange}")





