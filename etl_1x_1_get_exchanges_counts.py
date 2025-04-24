from utils.core_pipeline import post_request
from utils.io_utils import flatten_and_save_csv_exchanges, csv_to_sql_table
from utils.dir_utils import get_exchanges_csv_path, get_exchanges_csv_path2
from config.settings import BASE_URL, HEADERS, TODAY, DB_CONNECTION
from config.api_queries import QUERY_EXCHANGES

def main():

    csv_path = get_exchanges_csv_path(TODAY)
    csv_path2 = get_exchanges_csv_path2(TODAY)
    # Fetch data from API
    json_data = post_request(BASE_URL, HEADERS, QUERY_EXCHANGES)

    if json_data:
        statements = json_data.get('data', {}).get('exchanges', [])

        # Flatten and save the data to CSV
        flatten_and_save_csv_exchanges(statements, csv_path, TODAY)
        flatten_and_save_csv_exchanges(statements, csv_path2, TODAY)
        # Save the CSV data to the database
        csv_to_sql_table(csv_path, "exchanges_counts", DB_CONNECTION)
    else:
        print("API request failed or returned empty data.")

if __name__ == "__main__":
    main()
