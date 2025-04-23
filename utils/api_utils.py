import time
import csv
import requests
from pathlib import Path

from config.settings import HEADERS, BASE_URL as url, TODAY
from utils.dir_utils import failed_log_path, companies_path
from utils.io_utils import write_csv_header_if_needed
from config.api_queries import QUERY_ALL_COMPANIES_MINIMAL

limit = 100

def fetch_companies(exchange, company_count):
    """Fetch company data for a single exchange and write to CSV."""
    offset = 0
    csv_path = Path(companies_path) / f"{exchange}_{TODAY}.csv"

    print(f"\n🚀 Fetching data for {exchange}...")
    write_csv_header_if_needed(csv_path)

    while offset < company_count:
        page_num = offset // limit + 1
        total_pages = company_count // limit + 1
        print(f"📚 Page {page_num} of {total_pages} for {exchange}")

        payload = {
            "query": QUERY_ALL_COMPANIES_MINIMAL,
            "variables": {
                "exchange": exchange,
                "limit": limit,
                "offset": offset
            }
        }

        try:
            response = requests.post(url, json=payload, headers=HEADERS)
            response.raise_for_status()  # handles 4xx/5xx errors

            try:
                companies = response.json()["data"]["companies"]
            except (KeyError, TypeError) as parse_error:
                print(f"⚠️ JSON parsing error at offset {offset}: {parse_error}")
                print(f"Raw response:\n{response.text}")
                _log_failure(exchange, offset)
                offset += limit
                continue

            _write_company_rows(companies, csv_path)
            offset += limit
            time.sleep(0.3)

        except Exception as e:
            print(f"❌ Exception for {exchange} @ offset {offset}: {e}")
            _log_failure(exchange, offset)
            break

    print(f"✅ Completed {exchange}: Data saved to {csv_path}")


def _write_company_rows(companies, filepath):
    with open(filepath, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for c in companies:
            writer.writerow([
                TODAY,
                c.get("id"),
                c.get("name"),
                c.get("tickerSymbol"),
                c.get("exchangeSymbol"),
                c.get("active"),
                c.get("marketCapUSD")
            ])


def _log_failure(exchange, offset):
    with open(failed_log_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([exchange, offset])
