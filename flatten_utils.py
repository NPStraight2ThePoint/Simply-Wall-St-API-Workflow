import os
from datetime import datetime
import csv
import pandas as pd
import logging
import requests

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def safe_get(data, key, default=None):
    try:
        if data is None:
            return default
        return data.get(key, default)
    except Exception as e:
        logging.error(f"Error accessing {key} in data: {data}. Error: {str(e)}")
        return default

def flatten_statements(company, ticker, exchange, today):
    statements_data = []
    for statement in company.get("statements", []):
        try:
            statements_data.append({
                "ticker": ticker,
                "exchange": exchange,
                "date": today,
                "name": safe_get(statement, 'name'),
                "title": safe_get(statement, 'title'),
                "area": safe_get(statement, 'area'),
                "type": safe_get(statement, 'type'),
                "value": safe_get(statement, 'value'),
                "description": safe_get(statement, 'description'),
                "state": safe_get(statement, 'state'),
                "severity": safe_get(statement, 'severity'),
                "outcomeName": safe_get(statement, 'outcomeName'),
            })
        except Exception as e:
            logging.error(f"Error processing statement for {ticker}: {str(e)}")
    return statements_data

def flatten_listings(company, ticker, exchange, today):
    listings_data = []
    try:
        listings_data.append({
            'id': safe_get(company, "id", ""),
            'date': today,
            'exchange_symbol': safe_get(company, "exchangeSymbol", ""),
            'ticker_symbol': safe_get(company, "tickerSymbol", ""),
            'name': safe_get(company, "name", ""),
            'market_cap_usd': safe_get(company, "marketCapUSD", 0),
            'primary_industry': safe_get(company.get("primaryIndustry", {}), "name", ""),
            'secondary_industry': safe_get(company.get("secondaryIndustry", {}), "name", ""),
            'tertiary_industry': safe_get(company.get("tertiaryIndustry", {}), "name", ""),
            'market': safe_get(company.get("market", {}), "name", ""),
            'market_iso2': safe_get(company.get("market", {}), "iso2", ""),
            'active': safe_get(company, "active", ""),
            'classification_status': safe_get(company, "classificationStatus", ""),
        })
    except Exception as e:
        logging.error(f"Error processing listings for {ticker}: {str(e)}")
    return listings_data

def flatten_owners(company, ticker, exchange, today):
    owners_data = []
    for owner in company.get("owners", []):
        try:
            owners_data.append({
                "ticker": safe_get(company, "tickerSymbol", ""),
                "exchange": safe_get(company, "exchangeSymbol", ""),
                "date": today,
                "owner_name": safe_get(owner, "name"),
                "owner_type": safe_get(owner, "type"),
                "sharesHeld": safe_get(owner, "sharesHeld"),
                "holdingDate": safe_get(owner, "holdingDate"),
                "periodStartDate": safe_get(owner, "periodStartDate"),
                "periodEndDate": safe_get(owner, "periodEndDate"),
                "rankSharesHeld": safe_get(owner, "rankSharesHeld"),
                "rankSharesSold": safe_get(owner, "rankSharesSold")
            })
        except Exception as e:
            logging.error(f"Error processing owner data for {ticker}: {str(e)}")
    return owners_data

def flatten_insider_transactions(company, ticker, exchange, today):
    insider_transactions_data = []
    for transaction in company.get("insiderTransactions", []):
        try:
            insider_transactions_data.append({
                "ticker": safe_get(company, "tickerSymbol", ""),
                "exchange": safe_get(company, "exchangeSymbol", ""),
                "date": today,
                "owner_name": safe_get(transaction, "ownerName"),
                "owner_type": safe_get(transaction, "ownerType"),
                "type": safe_get(transaction, "type"),
                "description": safe_get(transaction, "description"),
                "tradeDateMin": safe_get(transaction, "tradeDateMin"),
                "tradeDateMax": safe_get(transaction, "tradeDateMax"),
                "shares": safe_get(transaction, "shares"),
                "priceMin": safe_get(transaction, "priceMin"),
                "priceMax": safe_get(transaction, "priceMax"),
                "transactionValue": safe_get(transaction, "transactionValue"),
                "percentageSharesTraded": safe_get(transaction, "percentageSharesTraded"),
                "percentageChangeTransShares": safe_get(transaction, "percentageChangeTransShares"),
                "isManagementInsider": safe_get(transaction, "isManagementInsider"),
                "filingDate": safe_get(transaction, "filingDate")
            })
        except Exception as e:
            logging.error(f"Error processing insider transaction for {ticker}: {str(e)}")
    return insider_transactions_data

def flatten_members(company, ticker, exchange, today):
    members_data = []
    for member in company.get("members", []):
        try:
            members_data.append({
                "ticker": safe_get(company, "tickerSymbol", ""),
                "exchange": safe_get(company, "exchangeSymbol", ""),
                "date": today,
                "age": safe_get(member, "age"),
                "name": safe_get(member, "name"),
                "title": safe_get(member, "title"),
                "tenure": safe_get(member, "tenure"),
                "compensation": safe_get(member, "compensation")
            })
        except Exception as e:
            logging.error(f"Error processing member data for {ticker}: {str(e)}")
    return members_data

def flatten_all(company, ticker, exchange, today):
    statements_data = flatten_statements(company, ticker, exchange, today)
    listings_data = flatten_listings(company, ticker, exchange, today)
    owners_data = flatten_owners(company, ticker, exchange, today)
    insider_transactions_data = flatten_insider_transactions(company, ticker, exchange, today)
    members_data = flatten_members(company, ticker, exchange, today)

    return statements_data, listings_data, owners_data, insider_transactions_data, members_data


