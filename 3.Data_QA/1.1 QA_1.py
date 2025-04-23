import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

# Custom imports
from config.env_utils import *               # For loading environment variables
from config.settings import *               # For db_params1
from utils.sql_utils import load_sql_queries  # For loading .sql files

# Load env variables (API keys, DB creds, etc.)
load_env()

# Set current month start for parameterized SQL queries
TODAY = datetime.now().replace(day=1).strftime("%Y-%m-%d")

# ─────────────────────────────────────────────────────────────
# Database Connection
# ─────────────────────────────────────────────────────────────
conn_str = f"postgresql+psycopg2://{db_params1['user']}:{db_params1['password']}@{db_params1['host']}:{db_params1['port']}/{db_params1['database']}"
engine = create_engine(conn_str)

# ─────────────────────────────────────────────────────────────
# Load SQL Files
# ─────────────────────────────────────────────────────────────
SQL_QUERIES_PATH = "C:/.../.venv/SQL Queries"
SQL_QUERIES = load_sql_queries(SQL_QUERIES_PATH)

# ─────────────────────────────────────────────────────────────
# Output Path
# ─────────────────────────────────────────────────────────────
output_file = "C:/.../.venv/Data/Log/QA_1_Results.xlsx"

# ─────────────────────────────────────────────────────────────
# Run each query and export results to Excel
# ─────────────────────────────────────────────────────────────
try:
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for query_name, sql in SQL_QUERIES.items():
            print(f"Running {query_name}...")

            # Handle parameterized queries
            num_params = sql.count('%s')
            params = tuple([TODAY] * num_params) if num_params > 0 else None

            try:
                df = pd.read_sql_query(sql, engine, params=params)
                df.to_excel(writer, sheet_name=query_name[:31], index=False)
            except Exception as query_error:
                print(f"❌ Failed on {query_name}: {query_error}")

    print(f"\n✅ Done: All results saved to {output_file}")

except Exception as e:
    print(f"🔥 Error in main execution: {e}")
