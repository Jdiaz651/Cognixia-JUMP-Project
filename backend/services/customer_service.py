
from bson import ObjectId
from bson.errors import InvalidId
from backend.db import users  # Import the users collection handle from db.py
from pymongo import ReturnDocument
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CustomerNotFound(Exception):
    """Custom exception raised when a requested customer is not found in MongoDB."""
    pass


class AuthenticationError(Exception):
    """Custom exception raised when authentication fails."""
    pass


def _format_customer(doc: dict) -> dict:
    """Helper function to convert MongoDB's internal `_id` (ObjectId)
    into a string `id` so Pydantic and JSON can serialize it properly.
    """
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
    # Remove password from output for security
    if "password" in doc:
        del doc["password"]
    return doc


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create(name: str, email: str, password: str, branch_id: int, is_admin: bool = False) -> dict:
    # Check if email already exists
    if users.find_one({"email": email}):
        raise ValueError("Email already registered")

    customer_doc = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "branch_id": branch_id,
        "is_active": True,
        "is_admin": is_admin,
    }
    result = users.insert_one(customer_doc)
    customer_doc["_id"] = result.inserted_id
    return _format_customer(customer_doc)


def list_all() -> list[dict]:
    # Find all customers that are active
    cursor = users.find({"is_active": True})
    return [_format_customer(doc) for doc in cursor]


def get(customer_id: str) -> dict:
    # Convert the string ID from the URL into a MongoDB ObjectId
    try:
        obj_id = ObjectId(customer_id)
    except InvalidId:
        raise CustomerNotFound()

    doc = users.find_one({"_id": obj_id, "is_active": True})
    if not doc:
        raise CustomerNotFound()

    return _format_customer(doc)


# customer_service.py

def get_by_email(email: str) -> dict | None:
    """Public-facing lookup — safe to expose over HTTP."""
    doc = users.find_one({"email": email, "is_active": True})
    if not doc:
        return None
    return _format_customer(doc)


def _get_by_email_raw(email: str) -> dict | None:
    """Internal only — includes password hash, used for auth."""
    return users.find_one({"email": email, "is_active": True})


def authenticate(email: str, password: str) -> dict:
    user_doc = _get_by_email_raw(email)
    if not user_doc or not verify_password(password, user_doc["password"]):
        raise AuthenticationError("Invalid email or password")
    return _format_customer(user_doc)


def update(customer_id: str, name: str | None = None, email: str | None = None) -> dict:
    try:
        obj_id = ObjectId(customer_id)
    except InvalidId:
        raise CustomerNotFound()

    # find_one_and_update updates the document and returns the updated version
    updated_doc = users.find_one_and_update(
        {"_id": obj_id, "is_active": True},
        {"$set": {"name": name, "email": email}},
        return_document=ReturnDocument.AFTER,
    )

    if not updated_doc:
        raise CustomerNotFound()

    return _format_customer(updated_doc)


def deactivate(customer_id: str) -> dict:
    try:
        obj_id = ObjectId(customer_id)
    except InvalidId:
        raise CustomerNotFound()

    # Soft delete: set is_active to False instead of completely deleting the record

    deactivated_doc = users.find_one_and_update(
        {"_id": obj_id, "is_active": True},
        {"$set": {"is_active": False}},
        return_document=ReturnDocument.AFTER,
    )

    if not deactivated_doc:
        raise CustomerNotFound()

    return _format_customer(deactivated_doc)


def delete(customer_id: str) -> dict:
    try:
        obj_id = ObjectId(customer_id)
    except InvalidId:
        raise CustomerNotFound()

    # Permanently deletes the document matching the _id from MongoDB
    deleted_doc = users.find_one_and_delete({"_id": obj_id})

    # If no document was found with that ID
    if not deleted_doc:
        raise CustomerNotFound()

    return _format_customer(deleted_doc)
