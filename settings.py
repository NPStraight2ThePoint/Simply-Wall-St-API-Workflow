# settings.py

from config.env_utils import API_KEY, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from utils.dir_utils import get_today_date
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# API Configuration
# ─────────────────────────────────────────────────────────────
BASE_URL = "https://api.simplywall.st/graphql"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ─────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────
TODAY = datetime.now().replace(day=1).strftime("%Y-%m-%d")

# Paths
EXCHANGES_CSV_PATH = f"./Data/Exchanges_Counts/Exchanges_{TODAY}.csv"

# ─────────────────────────────────────────────────────────────
# Database URI for SQLAlchemy
# ─────────────────────────────────────────────────────────────
DB_CONNECTION = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy-style
db_params = {
    'username': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT,
    'database': DB_NAME
}

# alt-style for compatibility
db_params1 = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT,
    'database': DB_NAME
}

# psycopg2 style
db_params2 = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'port': DB_PORT
}
import psycopg2
# psycopg2 style
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
