from utils.api_utils import fetch_companies
from utils.io_utils import init_failed_log, load_exchanges
from utils.sql_utils import load_csvs_to_sql

def extract_all_exchanges():
    init_failed_log()
    exchange_list, company_counts = load_exchanges()

    for exchange in exchange_list:
        company_count = company_counts.get(exchange, 0)
        if company_count == 0:
            print(f"⚠️ Skipping {exchange} — no company count recorded.")
            continue

        fetch_companies(exchange, company_count)

def main():
    extract_all_exchanges()
    load_csvs_to_sql()

if __name__ == "__main__":
    main()
