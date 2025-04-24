from utils.core_pipeline import run_pipeline, run_pipeline2
from datetime import datetime
import os
from utils.dir_utils import *
import pandas as pd

def file_exists(file_path):
    """Helper function to check if a file exists."""
    return os.path.exists(file_path)


def main():
    step1 = 30
    step2 = 1
    step3 = 1

    print(f"🚀 Starting Try 1 (step = {step1})")
    run_pipeline(LOG_PATH[0], EXCHANGES_CSV_PATH, step1, BASE_DIRECTORIES[0])
    print(f"✅ Try {1} completed.\n")

    if file_exists(LOG_PATH[0]):
        print(f"🚀 Starting Try 2 (step = {step2})")
        run_pipeline2(LOG_PATH[0], LOG_PATH[1], TODAY, BASE_DIRECTORIES[1])
        print(f"✅ Try {2} completed.\n")
    else:
        print(f"⚠️ File {LOG_PATH[0]} does not exist. Skipping Try 2.\n")

    if file_exists(LOG_PATH[1]):
        print(f"🚀 Starting Try 3 (step = {step3})")
        run_pipeline2(LOG_PATH[1], LOG_PATH[2], TODAY, BASE_DIRECTORIES[2])
        print(f"✅ Try {3} completed.\n")
    else:
        print(f"⚠️ File {LOG_PATH[1]} does not exist. Skipping Try 3.\n")

if __name__ == "__main__":
    main()
