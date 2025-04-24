import shutil
from pathlib import Path
from datetime import datetime
import pandas as pd

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────
TODAY = datetime.today().replace(day=1).strftime("%Y-%m-%d")
first_day_of_month = datetime.today().replace(day=1).strftime("%Y-%m-%d")

data_folder = Path(
    r"C:/.../.venv/Data"
)

# Get exchange name from the CSV
exchange_csv = data_folder / f"Exchanges_Counts/Exchanges_{TODAY}.csv"
try:
    exchange = pd.read_csv(exchange_csv).iloc[0]["exchange"]
except Exception as e:
    exchange = "Unknown_Exchange"
    print(f"⚠️ Could not read exchange from {exchange_csv}: {e}")

# Create archive path using exchange
archive_folder = (
    Path(
        r"C:/.../.venv/Data Archive"
    )
    / first_day_of_month
    / exchange
)

BASE_DIRECTORIES = [
    data_folder / "Try 1",
    data_folder / "Try 2",
    data_folder / "Try 3",
    data_folder / "Try_id",
    data_folder / "Companies",
    data_folder / "Log",
    data_folder / "Joined Data/NEW_DATA",
    data_folder / "Joined Data/NEW_DATA_id",
    data_folder / "Joined Data/EXISTING_DATA",
    data_folder / "Joined Data/EXISTING_DATA_id",
    data_folder / "Rec File",
    data_folder / "Exchanges_Counts",
]

# ─────────────────────────────────────────────────────────────
# Core Functions
# ─────────────────────────────────────────────────────────────
def move_folders_to_archive():
    archive_folder.mkdir(parents=True, exist_ok=True)
    data_subfolders = [f for f in data_folder.iterdir() if f.is_dir()]

    for subfolder in data_subfolders:
        new_folder_name = archive_folder / f"{first_day_of_month}_{subfolder.name}"
        try:
            shutil.move(str(subfolder), str(new_folder_name))
            print(f"📦 Moved {subfolder} to {new_folder_name}")
        except Exception as e:
            print(f"❌ Error moving {subfolder}: {e}")

def delete_specified_folders():
    for folder in BASE_DIRECTORIES:
        if folder.exists():
            try:
                shutil.rmtree(folder)
                print(f"🗑️  Deleted {folder}")
            except Exception as e:
                print(f"❌ Error deleting {folder}: {e}")

def recreate_directories():
    for folder in BASE_DIRECTORIES:
        try:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"📁 Recreated {folder}")
        except Exception as e:
            print(f"❌ Error recreating {folder}: {e}")

# ─────────────────────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────────────────────
def main():
    print(f"🚀 Starting archive and cleanup process for exchange: {exchange}\n")
    move_folders_to_archive()
    delete_specified_folders()
    recreate_directories()
    print("\n✅ All operations completed.")

if __name__ == "__main__":
    main()

