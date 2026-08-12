
from bson import ObjectId
from bson.errors import InvalidId
from app.db import users  # Import the users collection handle from db.py
from pymongo import ReturnDocument

class CustomerNotFound(Exception):
    """Custom exception raised when a requested customer is not found in MongoDB."""
    pass


def _format_customer(doc: dict) -> dict:
    """Helper function to convert MongoDB's internal `_id` (ObjectId) 

    into a string `id` so Pydantic and JSON can serialize it properly.
    """
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
    return doc


def create(name: str, email: str, branch_id: int) -> dict:
    customer_doc = {
        "name": name,
        "email": email,
        "branch_id": branch_id,
        "is_active": True,
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