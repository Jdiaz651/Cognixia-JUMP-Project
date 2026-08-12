# app/seed.py
from datetime import datetime, timezone
from backend.db import db

branches = db["branches"]


def seed_branches():
    if branches.count_documents({}) > 0:
        return

    now = datetime.now(timezone.utc)

    branches.insert_many([
        {
            "branch_code": "B1",
            "location": "Downtown",
            "manager_id": "M001",
            "staff": [
                {"staff_id": "S001", "staff_type": "direct"},
                {"staff_id": "S002", "staff_type": "direct"},
                {"staff_id": "S003", "staff_type": "contract"},
            ],
            "created_at": now,
        },
        {
            "branch_code": "B2",
            "location": "Uptown",
            "manager_id": "M002",
            "staff": [
                {"staff_id": "S004", "staff_type": "contract"},
            ],
            "created_at": now,
        },
    ])