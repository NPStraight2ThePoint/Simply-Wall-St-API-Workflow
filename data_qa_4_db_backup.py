import subprocess
import os
from datetime import datetime
from config.env_utils import *

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────
BACKUP_DIR = r"C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production/.venv/Backup"
DATE = datetime.now().strftime("%Y%m%d_%H%M%S")  # Create unique backup file names
BACKUP_FILE = os.path.join(BACKUP_DIR, f"{DB_NAME2}_backup_{DATE}.sql")

# Ensure the backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)

# Path to pg_dump executable
pg_dump_path = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"

# Backup command
pg_dump_command = [
    pg_dump_path,
    "-U", DB_USER,
    "-h", DB_HOST,
    "-p", str(DB_PORT),
    "-F", "c",
    "-f", BACKUP_FILE,
    DB_NAME2
]

# ─────────────────────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────────────────────
def create_backup():
    # Set environment variable for password authentication
    os.environ["PGPASSWORD"] = DB_PASSWORD

    try:
        # Run the pg_dump command
        print(f"🧳 Creating backup of {DB_NAME2}...")
        subprocess.run(pg_dump_command, check=True)
        print(f"✅ Backup saved to {BACKUP_FILE}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during backup: {e}")
    finally:
        del os.environ["PGPASSWORD"]  # Clean up the environment variable after use

# ─────────────────────────────────────────────────────────────
# Main Function
# ─────────────────────────────────────────────────────────────
def main():
    print("🚀 Starting database backup process...")
    create_backup()
    print("\n✅ Backup process completed.")

if __name__ == "__main__":
    main()
