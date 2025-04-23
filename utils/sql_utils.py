import os
import pandas as pd
from pathlib import Path
from config.env_utils import *
from sqlalchemy import create_engine, text
from datetime import datetime
import psycopg2
from config.settings import *
def load_sql_queries(directory_path):

    sql_queries = {}

    # Loop through all .sql files in the given directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".sql"):
            query_name = filename.split('.')[0]  # Strip the file extension
            with open(os.path.join(directory_path, filename), 'r') as file:
                sql_queries[query_name] = file.read()

    return sql_queries

def update_multiple_tables_to_uppercase(db_params):
    try:
        # Get today's date (1st of the month)
        today = datetime.now().replace(day=1).strftime("%Y-%m-%d")

        # Create the SQLAlchemy engine
        connection_string = f"postgresql://{db_params['username']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
        engine = create_engine(connection_string)

        # Define the queries with placeholders for today
        queries = [
            f"UPDATE exchanges_counts SET exchange = UPPER(exchange) WHERE index_date = '{today}';",
            f"UPDATE listings SET exchange_symbol = UPPER(exchange_symbol), ticker_symbol = UPPER(ticker_symbol) WHERE date = '{today}';",
            f"UPDATE insider_transactions SET exchange = UPPER(exchange), ticker = UPPER(ticker) WHERE date = '{today}';",
            f"UPDATE members SET exchange = UPPER(exchange), ticker = UPPER(ticker) WHERE date = '{today}';",
            f"UPDATE owners SET exchange = UPPER(exchange), ticker = UPPER(ticker) WHERE date = '{today}';",
            f"UPDATE statements SET exchange = UPPER(exchange), ticker = UPPER(ticker) WHERE date = '{today}';"
        ]

        with engine.connect() as conn:
            for query in queries:
                print(f"Running: {query.strip()}")
                result = conn.execute(text(query))
                print(f"✅ {result.rowcount} rows updated.")
            conn.commit()

        print("🎉 All updates completed successfully.")

    except Exception as e:
        print(f"❌ Error executing queries: {e}")

def delete_data_from_table(db_params):
    try:
        # Connect to the database using psycopg2
        conn = psycopg2.connect(
            dbname=db_params['database'],
            user=db_params['username'],
            password=db_params['password'],
            host=db_params['host'],
            port=db_params['port']
        )

        # Create a cursor and execute the query
        with conn.cursor() as cur:
            cur.execute("DELETE FROM public.insider_transactions_uat;")
            conn.commit()  # Commit the transaction
            print("✅ Deleted all records from public.insider_transactions_uat")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

    finally:
        if conn:
            conn.close()

import os
from sqlalchemy import create_engine
from config.settings import DB_CONNECTION
from utils.dir_utils import companies_path
engine = create_engine(DB_CONNECTION)

def load_csvs_to_sql():
    for filename in os.listdir(companies_path):
        if filename.endswith(".csv"):
            csv_path = os.path.join(companies_path, filename)
            print(f"✅ Processing: {filename}")

            df = pd.read_csv(csv_path)
            df.columns = [col.strip() for col in df.columns]
            df.to_sql("companies", con=engine, if_exists='append', index=False)

    print("✅ All CSVs loaded into SQL.")


import psycopg2
import logging
from config.settings import * # Assuming DB_PARAMS are stored in settings


def execute_query(query, params=None):
    """
    Executes a given SQL query with optional parameters.

    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): The parameters for the query.

    Returns:
        result (list): The query results if SELECT query, else None.
    """
    result = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        cursor.execute(query, params)

        # If SELECT query, fetch results
        if query.strip().lower().startswith("select"):
            result = cursor.fetchall()

        # Commit changes if it's an INSERT/UPDATE/DELETE query
        else:
            conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f"Error executing query: {e}")

    return result
