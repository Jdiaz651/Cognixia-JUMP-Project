# db.py
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING

# Get the directory where db.py is located
BASE_DIR = Path(__file__).resolve().parent
# Load .env from the backend directory explicitly
load_dotenv(BASE_DIR / ".env.local")

# Use .get() to avoid KeyError and provide a helpful error message
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI not found in environment. "
        "Please ensure a .env file exists in the 'backend/' directory with 'MONGO_URI=your_connection_string'"
    )

client = MongoClient(MONGO_URI)
db = client["bank_db"]

# Collection handles — import these, not `db` directly, from services/controllers
users = db["users"]
accounts = db["accounts"]
transactions = db["transactions"]
branches = db["branches"]


def create_indexes():
    accounts.create_index([("account_number", ASCENDING)], unique=True)
    branches.create_index([("branch_code", ASCENDING)], unique=True)
    transactions.create_index([("timestamp", ASCENDING)])

# Automatically create indexes on module load
create_indexes()
