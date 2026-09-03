from datetime import datetime
from typing import Optional
from bson import ObjectId
from bson.errors import InvalidId
from backend.db import client, accounts, transactions
from backend.services.account_service import AccountNotFound, withdraw, deposit

def transfer(from_account_number: int, to_account_number: int, amount: float) -> dict:
    # Use a session to ensure atomicity of the transfer
    with client.start_session() as session:
        with session.start_transaction():
            # 1. Withdraw from source
            withdraw(from_account_number, amount, session=session)
            
            # 2. Deposit to destination
            deposit(to_account_number, amount, session=session)

            # 3. Record the transaction
            txn_doc = {
                "from_account": from_account_number,
                "to_account": to_account_number,
                "amount": amount,
                "type": "transfer",
                "timestamp": datetime.now()
            }
            
            result = transactions.insert_one(txn_doc, session=session)
            txn_doc["_id"] = result.inserted_id
            return txn_doc

def list_all(start_date=None, end_date=None, type: str = None) -> list[dict]:
    query = {}
    
    if type:
        query["type"] = type.lower()
    
    if start_date or end_date:
        date_query = {}
        if start_date:
            date_query["$gte"] = datetime.combine(start_date, datetime.min.time())
        if end_date:
            date_query["$lte"] = datetime.combine(end_date, datetime.max.time())
        query["timestamp"] = date_query

    cursor = transactions.find(query).sort("timestamp", 1)
    
    results = []
    for doc in cursor:
        doc["id"] = str(doc["_id"])
        results.append(doc)
        
    return results
