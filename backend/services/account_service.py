from bson import ObjectId
from bson.errors import InvalidId
from backend.db import accounts, users
from backend.services.customer_service import CustomerNotFound

class AccountNotFound(Exception):
    """Custom exception raised when a requested account is not found in MongoDB."""
    pass

def _format_account(doc: dict) -> dict:
    """Helper function to convert MongoDB's internal `_id` (ObjectId) 
    into a string `id` so Pydantic and JSON can serialize it properly.
    """
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
    return doc

def create(owner_id: str, account_type: str, balance: float = 0.0, 
           minimum_balance: float = None, overdraft_limit: float = None) -> dict:
    # Check if customer exists
    try:
        obj_id = ObjectId(owner_id)
    except InvalidId:
        raise CustomerNotFound()
        
    customer = users.find_one({"_id": obj_id, "is_active": True})
    if not customer:
        raise CustomerNotFound()

    # Generate account number (simple approach for now: max + 1)
    last_account = accounts.find_one(sort=[("account_number", -1)])
    next_account_number = 10000000 if not last_account else last_account["account_number"] + 1

    account_doc = {
        "account_number": next_account_number,
        "owner_id": obj_id,
        "account_type": account_type,
        "balance": balance,
    }

    # Apply account-specific defaults/rules
    if account_type == "savings":
        account_doc["minimum_balance"] = minimum_balance if minimum_balance is not None else 100.0
    elif account_type == "checking":
        account_doc["overdraft_limit"] = overdraft_limit if overdraft_limit is not None else 200.0
    
    result = accounts.insert_one(account_doc)
    account_doc["_id"] = result.inserted_id
    return _format_account(account_doc)

def get(account_number: int) -> dict:
    doc = accounts.find_one({"account_number": account_number})
    if not doc:
        raise AccountNotFound(account_number)
    return _format_account(doc)

def deposit(account_number: int, amount: float, session=None) -> dict:
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")

    # Use session if provided (for atomic transactions)
    update_kwargs = {"session": session} if session else {}
    
    result = accounts.find_one_and_update(
        {"account_number": account_number},
        {"$inc": {"balance": amount}},
        return_document=True, # This is for pymongo 4.0+
        **update_kwargs
    )
    
    if not result:
        raise AccountNotFound(account_number)
    
    return _format_account(result)

def withdraw(account_number: int, amount: float, session=None) -> dict:
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")

    # Find account first to check rules
    # Note: In a heavy concurrent environment, you'd want to do this inside the transaction
    update_kwargs = {"session": session} if session else {}
    
    account = accounts.find_one({"account_number": account_number}, session=session)
    if not account:
        raise AccountNotFound(account_number)

    # Business Rule Enforcement
    new_balance = account["balance"] - amount
    
    if account["account_type"] == "savings":
        min_bal = account.get("minimum_balance", 100.0)
        if new_balance < min_bal:
            raise ValueError(f"Withdrawal would go below minimum balance of ${min_bal:.2f}")
    
    elif account["account_type"] == "checking":
        overdraft = account.get("overdraft_limit", 200.0)
        if new_balance < -overdraft:
            raise ValueError(f"Withdrawal exceeds overdraft limit of ${overdraft:.2f}")

    # Execute withdrawal
    result = accounts.find_one_and_update(
        {"account_number": account_number},
        {"$inc": {"balance": -amount}},
        return_document=True,
        **update_kwargs
    )
    
    if not result:
        raise AccountNotFound(account_number)
        
    return _format_account(result)

def list_all(branch_id: str = None, min_balance: float = None) -> list[dict]:
    query = {}
    if min_balance is not None:
        query["balance"] = {"$gte": min_balance}

    cursor = accounts.find(query)
    account_list = [_format_account(doc) for doc in cursor]

    if branch_id is not None:
        filtered_accounts = []
        for acc in account_list:
            try:
                owner_id = acc["owner_id"]
                customer = users.find_one({"_id": ObjectId(owner_id)})
                if customer and str(customer.get("branch_id")) == str(branch_id):
                    filtered_accounts.append(acc)
            except (InvalidId, KeyError):
                continue
        return filtered_accounts

    return account_list
