# Simply-Wall-St-API-Workflow
This repository demonstrates the creation of a data pipeline that retrieves financial data from the Simply Wall St API, processes cleans and stores the data in a PostgreSQL database . The pipeline showcases an end-to-end workflow that integrates data acquisition, transformation, with end goal being to generate actionable financial insights.

The project is built using Python, PostgreSQL, Pandas and Simply Wall St API .

Key Features

●Retrieve financial data from the Simply Wall St API.
●Cleanse and process the raw financial data (e.g., handling missing values, data flattening).
●Store structured data in a PostgreSQL database.
●Query structured data & apply financial analysis.
●Demonstrate end-to-end data pipeline construction.

How It Works
1. Data Retrieval
The pipeline starts by fetching financial data from the Simply Wall St API. This data includes information about stocks, financial metrics, and other relevant data points.

2. Data Cleansing
Once the data is retrieved, it is cleansed to handle issues like missing values, incorrect data formats, and outliers. This step ensures that the data is in a usable format for further analysis.

3. Storing Data in PostgreSQL
After cleansing, the data is stored in a PostgreSQL database. This allows for efficient querying and further data analysis in future steps.

4. Financial analysis
Finally data is queried and stored in excel , conducting attribution analysis based on the snowflake components for a universe of stocks,
and creating a ranking system to filter stocks.

Key Python Script Parts

1.Exchanges&Counts.py

#Libraries
import pandas as pd
from datetime import datetime
import requests
import os
import csv
from sqlalchemy import create_engine
from sqlalchemy import text

# PostgreSQL connection
  ...
  engine = create_engine(db_url)
  
# Simply API connection
  ... 
  # GraphQL
  query = """query { exchanges{symbol companiesCount}}"""

#Query Response
response = requests.post(url, headers=headers, json={"query": query})
data = response.json()
df = pd.DataFrame(data)

# Preparing json for data flattening
# Add date column at position 0 for all rows

  


  

