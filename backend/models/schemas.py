
from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal


# ---------- Customers ----------

class CustomerCreate(BaseModel):
    name: str
    email: str
    branch_id: int


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class CustomerOut(BaseModel):
    id: str  # MongoDB IDs are 24-char strings, not integers!
    name: str
    email: str
    branch_id: int
    is_active: bool

class CustomerLogin(BaseModel):
    name: str
    email: str

# ---------- Accounts ----------

class AccountCreate(BaseModel):
    owner_id: int
    account_type: Literal["checking", "savings"]
    balance: float = 0.0


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_number: int
    owner_id: int
    balance: float


# ---------- Transactions ----------

class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: float


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    from_account: Optional[int]
    to_account: Optional[int]
    amount: float
    type: str