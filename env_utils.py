# config/env_utils.py
import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

    def raise_error(var):
        raise EnvironmentError(f"{var} not found in .env file")

    return {
        "API_KEY": os.getenv("API_KEY") or raise_error("API_KEY"),
        "DB_USER": os.getenv("DB_USER") or raise_error("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD") or raise_error("DB_PASSWORD"),
        "DB_HOST": os.getenv("DB_HOST") or raise_error("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT") or raise_error("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME") or raise_error("DB_NAME"),
        "DB_NAME2": os.getenv("DB_NAME2") or raise_error("DB_NAME2")
    }

# Load once and expose
_env = load_env()
API_KEY = _env["API_KEY"]
DB_USER = _env["DB_USER"]
DB_PASSWORD = _env["DB_PASSWORD"]
DB_HOST = _env["DB_HOST"]
DB_PORT = _env["DB_PORT"]
DB_NAME = _env["DB_NAME"]
DB_NAME2 = _env["DB_NAME2"]


