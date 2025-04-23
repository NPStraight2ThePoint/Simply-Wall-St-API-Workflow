import pandas as pd
from sqlalchemy import create_engine, text
from datetime import date
from config.env_utils import * # Assumes db_params1 is loaded properly

from config.settings import * # Assumes db_params1 is loaded properly
# Connection setup
conn_str = f"postgresql+psycopg2://{db_params1['user']}:{db_params1['password']}@{db_params1['host']}:{db_params1['port']}/{db_params1['database']}"
engine = create_engine(conn_str)


# Dictionary mapping table names to deletion SQLs
delete_queries = {
    "exchanges_counts": """
        DELETE FROM exchanges_counts a
        USING (
            SELECT MIN(ctid) as keep_ctid, index_date, exchange
            FROM exchanges_counts
            WHERE index_date = :TODAY
            GROUP BY index_date, exchange
            HAVING COUNT(*) > 1
        ) b
        WHERE a.index_date = b.index_date
          AND a.exchange = b.exchange
          AND a.ctid <> b.keep_ctid;
    """,
    "companies": """
        DELETE FROM companies a
        USING (
            SELECT MIN(ctid) as keep_ctid, index_date, id
            FROM companies
            WHERE index_date = :TODAY
            GROUP BY index_date, id
            HAVING COUNT(*) > 1
        ) b
        WHERE a.index_date = b.index_date
          AND a.id = b.id
          AND a.ctid <> b.keep_ctid;
    """,
    "listings": """
        DELETE FROM listings a
        USING (
            SELECT MIN(ctid) as keep_ctid, date, id
            FROM listings
            WHERE date = :TODAY
            GROUP BY date, id
            HAVING COUNT(*) > 1
        ) b
        WHERE a.date = b.date
          AND a.id = b.id
          AND a.ctid <> b.keep_ctid;
    """,
    "statements": """
        DELETE FROM statements a
        USING (
            SELECT MIN(ctid) as keep_ctid, ticker, exchange, date
            FROM statements
            WHERE date = :TODAY
            GROUP BY ticker, exchange, date
            HAVING COUNT(*) > 1
        ) b
        WHERE a.ticker = b.ticker
          AND a.exchange = b.exchange
          AND a.date = b.date
          AND a.ctid <> b.keep_ctid;
    """
}

def delete_duplicates(engine, TODAY):
    with engine.begin() as conn:
        for table, query in delete_queries.items():
            try:
                print(f"🧹 Removing duplicates from {table} for {TODAY}...")
                result = conn.execute(text(query), {"TODAY": TODAY})
                print(f"✅ {table}: Duplicates cleaned.")
            except Exception as e:
                print(f"❌ Error in {table}: {e}")

if __name__ == "__main__":
    delete_duplicates(engine, TODAY)
