import shutil
from pathlib import Path
from datetime import datetime

# Define the date variable
first_day_of_month = datetime.today().replace(day=1).strftime("%Y-%m-%d")

# Define base directories for the folders to be moved
data_folder = Path(r"C:/.../.venv/Data")
archive_folder = Path(r"C:/Users/.../.venv/Data Archive") / first_day_of_month

# Define the directories to delete and recreate
BASE_DIRECTORIES = [
    Path(r"C:/.../.venv/Data/Try 1"),
    Path(r"C:/.../.venv/Data/Try 2"),
    Path(r"C:/.../.venv/Data/Try 3"),
    Path(r"C:/.../.venv/Data/Try_id"),
    Path(r"C:/.../.venv/Data/Companies"),
    Path(r"C:/.../.venv/Data/Log"),
    Path("C:/.../.venv/Data/Joined Data/NEW_DATA"),
    Path("C:/.../.venv/Data/Joined Data/NEW_DATA_id"),
    Path("C:/.../.venv/Data/Joined Data/EXISTING_DATA"),
    Path("C:/.../.venv/Data/Joined Data/EXISTING_DATA_id"),
    Path("C:/.../.venv/Data/Rec File"),
    Path("C:/.../.venv/Data/Exchanges_Counts"),
]

# Function to move folders
def move_folders_to_archive():
    # Create the 'Today' folder path inside 'Data Archive' if it doesn't exist
    archive_folder.mkdir(parents=True, exist_ok=True)

    # Get the list of all subdirectories in the Data folder
    data_subfolders = [f for f in data_folder.iterdir() if f.is_dir()]

    for subfolder in data_subfolders:
        # Create a new name for the subfolder with the current date as a prefix
        new_folder_name = archive_folder / f"{first_day_of_month}_{subfolder.name}"

        # Move the subfolder to the Data Archive folder
        try:
            shutil.move(str(subfolder), str(new_folder_name))
            print(f"Moved {subfolder} to {new_folder_name}")
        except Exception as e:
            print(f"Error moving {subfolder}: {e}")

# Function to delete specific folders/files
def delete_specified_folders():
    for folder in BASE_DIRECTORIES:
        if folder.exists():
            try:
                # Delete the folder and its contents
                shutil.rmtree(folder)
                print(f"Deleted {folder}")
            except Exception as e:
                print(f"Error deleting {folder}: {e}")

# Function to recreate the deleted directories
def recreate_directories():
    for folder in BASE_DIRECTORIES:
        if not folder.exists():
            try:
                folder.mkdir(parents=True, exist_ok=True)
                print(f"Recreated {folder}")
            except Exception as e:
                print(f"Error recreating {folder}: {e}")

# Perform the actions
move_folders_to_archive()  # Move folders to archive
delete_specified_folders()  # Delete specific folders/files
recreate_directories()  # Recreate the deleted directories


