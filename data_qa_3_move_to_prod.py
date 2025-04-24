from sqlalchemy import create_engine, MetaData, Table, select, text
import pandas as pd
# Replace with your real credentials
SRC_DB = "postgresql+psycopg2://postgres:Arxidolemios39@localhost/Simply_API"
DEST_DB = "postgresql+psycopg2://postgres:Arxidolemios39@localhost/Simply_API_Prod"

# ─────────────────────────────────────────────────────────────
# Core Function: Copy and Delete Table Data
# ─────────────────────────────────────────────────────────────
def copy_and_delete_table_data(table_name, src_engine, dest_engine, src_metadata):
    try:
        src_table = Table(table_name, src_metadata, autoload_with=src_engine)

        with src_engine.connect() as src_conn, dest_engine.begin() as dest_conn:
            result = src_conn.execute(select(src_table))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

            if df.empty:
                print(f"⚠️  Skipping {table_name}: No data.")
                return

            df.to_sql(table_name, dest_engine, if_exists='append', index=False)
            print(f"✅ Copied {len(df)} rows to {table_name}.")

            delete_query = text(f"DELETE FROM {table_name};")
            src_conn.execute(delete_query)
            src_conn.commit()

            print(f"🧹 Deleted all data from {table_name} in Simply_API.")

    except Exception as e:
        print(f"❌ Error copying/deleting {table_name}: {e}")

# ─────────────────────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────────────────────
def main():
    print("🚀 Starting table migration...")

    src_engine = create_engine(SRC_DB)
    dest_engine = create_engine(DEST_DB)

    src_metadata = MetaData()
    src_metadata.reflect(bind=src_engine)

    for table_name in src_metadata.tables:
        copy_and_delete_table_data(table_name, src_engine, dest_engine, src_metadata)

    print("\n✅ All tables processed.")

if __name__ == "__main__":
    main()
