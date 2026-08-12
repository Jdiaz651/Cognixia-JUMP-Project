# db.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING

load_dotenv()

MONGO_URI = os.environ["MONGO_URI"]

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
    transactions.create_index([("created_at", ASCENDING)])