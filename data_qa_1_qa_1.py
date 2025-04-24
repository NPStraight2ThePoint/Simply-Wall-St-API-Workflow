import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

# Custom imports
from config.env_utils import load_env
from config.settings import db_params1
from utils.sql_utils import load_sql_queries

def main():
    print("🚀 Starting SQL QA Run...\n")

    # Load env vars (DB creds, API keys, etc.)
    load_env()

    # Set current month for parameter substitution
    TODAY = datetime.now().replace(day=1).strftime("%Y-%m-%d")

    # Database connection
    conn_str = (
        f"postgresql+psycopg2://{db_params1['user']}:{db_params1['password']}"
        f"@{db_params1['host']}:{db_params1['port']}/{db_params1['database']}"
    )
    engine = create_engine(conn_str)

    # Load SQL queries
    SQL_QUERIES_PATH = "C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production/.venv/SQL Queries"
    SQL_QUERIES = load_sql_queries(SQL_QUERIES_PATH)

    # Output file location
    output_file = (
        "C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production/"
        ".venv/Data/Log/QA_1_Results.xlsx"
    )

    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for query_name, sql in SQL_QUERIES.items():
                print(f"📄 Running query: {query_name}...")

                num_params = sql.count('%s')
                params = tuple([TODAY] * num_params) if num_params > 0 else None

                try:
                    df = pd.read_sql_query(sql, engine, params=params)
                    df.to_excel(writer, sheet_name=query_name[:31], index=False)
                except Exception as query_error:
                    print(f"❌ Failed on {query_name}: {query_error}")

        print(f"\n✅ All results saved to: {output_file}")

    except Exception as e:
        print(f"🔥 Error in main execution: {e}")

if __name__ == "__main__":
    main()
