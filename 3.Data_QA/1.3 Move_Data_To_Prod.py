from sqlalchemy import create_engine, MetaData, Table, select, text
import pandas as pd
# Replace with your real credentials
SRC_DB = Source_DB
DEST_DB = Dest_DB

# Create engines
src_engine = create_engine(SRC_DB)
dest_engine = create_engine(DEST_DB)

# Reflect source metadata
src_metadata = MetaData()
src_metadata.reflect(bind=src_engine)

def copy_and_delete_table_data(table_name):
    try:
        # Reflect source table
        src_table = Table(table_name, src_metadata, autoload_with=src_engine)

        with src_engine.connect() as src_conn, dest_engine.begin() as dest_conn:
            # Read from source
            result = src_conn.execute(select(src_table))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

            if df.empty:
                print(f"⚠️  Skipping {table_name}: No data.")
                return

            # Write to target
            df.to_sql(table_name, dest_engine, if_exists='append', index=False)
            print(f"✅ Copied {len(df)} rows to {table_name}.")

            # Delete from source
            delete_query = text(f"DELETE FROM {table_name};")
            src_conn.execute(delete_query)  # Execute DELETE
            src_conn.commit()  # Explicit commit to ensure data is deleted

            print(f"🧹 Deleted all data from {table_name} in Simply_API.")

    except Exception as e:
        print(f"❌ Error copying/deleting {table_name}: {e}")

# Loop through all tables
for table_name in src_metadata.tables:
    copy_and_delete_table_data(table_name)
