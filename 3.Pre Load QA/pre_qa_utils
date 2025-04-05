import pandas as pd
import os
import glob
from dir_utils import TODAY

def process_directories(BASE_DIRECTORIES, keywords):

    for base_dir in BASE_DIRECTORIES:
        if not os.path.exists(base_dir):
            print(f"⚠️ Skipping missing directory: {base_dir}")
            continue
        print(f"\n📂 Processing directory: {base_dir}")
        # Loop through each subfolder in base_dir
        for subfolder in os.listdir(base_dir):
            subfolder_path = os.path.join(base_dir, subfolder)
            if os.path.isdir(subfolder_path):  # Ensure it's a directory
                print(f"   📂 Processing folder: {subfolder}")
                # Get all CSV files inside the current subfolder
                csv_files = glob.glob(os.path.join(subfolder_path, "*.csv"))
                # Initialize a dictionary to store row counts
                data = {"Type": [], "Rows": []}
                # Loop through each keyword and find matching files
                for keyword in keywords:
                    matching_files = [file for file in csv_files if keyword in file]

                    if matching_files:
                        file_path = matching_files[0]  # Take the first match if multiple exist
                        df = pd.read_csv(file_path)
                        row_count = len(df)
                    else:
                        row_count = ""

                    # Store the results
                    data["Type"].append(keyword)
                    data["Rows"].append(row_count)

                # Create DataFrame and save `row_counts.csv` inside the subfolder
                result_df = pd.DataFrame(data)
                output_file = os.path.join(subfolder_path, "row_counts.csv")
                result_df.to_csv(output_file, index=False)

                print(f"✅ Created: {output_file}")

    print("\n✅ All directories processed successfully!")

# Function to load retry errors from log file
def load_retry_errors(log_file):
    retry_errors = {}
    if os.path.exists(log_file):
        retry_df = pd.read_csv(log_file, header=None)
        empty_row = pd.DataFrame(columns=retry_df.columns)
        retry_df = pd.concat([empty_row, retry_df], ignore_index=True)

        if retry_df.shape[1] >= 1:
            retry_errors = retry_df.iloc[:, 0].astype(str).value_counts().to_dict()
    return retry_errors

# Function to load expected counts from CSV file
def load_expected_counts(expected_file):
    expected_counts = {}
    if os.path.exists(expected_file):
        expected_df = pd.read_csv(expected_file)
        if expected_df.shape[1] >= 3:
            expected_counts = dict(zip(expected_df.iloc[:, 1], expected_df.iloc[:, 2]))  # 2nd col = exchange, 3rd col = count
    return expected_counts

# Function to process row counts and aggregate data
def process_row_counts(base_dirs, keywords=["Listings", "Transposed"]):
    summary_data = {}
    for base_dir in base_dirs:
        if not os.path.exists(base_dir):
            print(f"Skipping missing directory: {base_dir}")
            continue

        for exchange in os.listdir(base_dir):
            exchange_path = os.path.join(base_dir, exchange)
            if not os.path.isdir(exchange_path):
                continue

            row_counts_file = os.path.join(exchange_path, "row_counts.csv")
            if not os.path.exists(row_counts_file):
                print(f"Missing row_counts.csv in {exchange_path}")
                continue

            df = pd.read_csv(row_counts_file)
            if "Type" not in df.columns or "Rows" not in df.columns:
                print(f"Skipping invalid file: {row_counts_file}")
                continue

            for _, row in df.iterrows():
                data_type = row["Type"]
                row_count = row["Rows"]
                key = (exchange, data_type)
                summary_data[key] = summary_data.get(key, 0) + row_count

    return summary_data

# Function to create the final summary dataframe
def create_summary_df(summary_data, retry_errors, expected_counts):
    summary_df = pd.DataFrame(
        [(exchange, data_type, rows,
          retry_errors.get(exchange, 0) if data_type in ["Listings", "Transposed"] else None,
          expected_counts.get(exchange, 0) if data_type in ["Listings", "Transposed"] else None,
          (expected_counts.get(exchange, 0) - (rows + retry_errors.get(exchange, 0))) if data_type in ["Listings", "Transposed"] else None)
         for (exchange, data_type), rows in summary_data.items()],
        columns=["Exchange", "Type", "Rows", "Errors", "Expected", "Reconciled"]
    )
    summary_df.insert(0, 'Date', TODAY)
    return summary_df

def process_and_transpose_rec_file(input_file, output_file):
    # Read the original Rec File
    df = pd.read_csv(input_file)

    # Fill NaN values with 0 to ensure they are included in pivot
    df[['Rows', 'Errors', 'Expected', 'Reconciled']] = df[['Rows', 'Errors', 'Expected', 'Reconciled']].fillna(0)

    # Pivot the dataframe
    pivot_df = df.pivot_table(index=['Date', 'Exchange'],
                              columns='Type',
                              values=['Rows', 'Errors', 'Expected', 'Reconciled'],
                              aggfunc='first')

    # Flatten the multi-level columns
    pivot_df.columns = [f'{col[1]}_{col[0]}' for col in pivot_df.columns]
    pivot_df.reset_index(inplace=True)

    # Save the transposed dataframe
    pivot_df.to_csv(output_file, index=False)

    # Re-read the transposed file to reorder columns
    df = pd.read_csv(output_file)

    # Rename columns
    df.columns = df.columns.str.replace('_Rows', '_Received')
    df.columns = df.columns.str.replace('Transposed', 'Statements')
    df.columns = df.columns.str.replace('_Reconciled', '_Difference')

    # Select only required columns
    filtered_columns = ['Date', 'Exchange',
                        'Insider_Transactions_Received', 'Listings_Received', 'Members_Received',
                        'Owners_Received', 'Statements_Received',
                        'Listings_Errors', 'Statements_Errors',
                        'Listings_Expected', 'Statements_Expected',
                        'Listings_Difference', 'Statements_Difference']

    df = df[filtered_columns]
    df.to_csv(output_file, index=False)
    print(f"✅ Processed and saved to: {output_file}")
