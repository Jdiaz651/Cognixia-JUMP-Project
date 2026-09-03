
from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal


# ---------- Customers ----------

class CustomerCreate(BaseModel):
    name: str
    email: str
    password: str
    branch_id: int
    is_admin: bool = False


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class CustomerOut(BaseModel):
    id: str  # MongoDB IDs are 24-char strings, not integers!
    name: str
    email: str
    branch_id: int
    is_active: bool
    is_admin: bool = False


# ---------- Authentication ----------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ---------- Accounts ----------

class AccountCreate(BaseModel):
    account_type: Literal["checking", "savings"]
    balance: float = 0.0
    minimum_balance: Optional[float] = None
    overdraft_limit: Optional[float] = None


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_number: int
    owner_id: str
    account_type: str
    balance: float
    minimum_balance: Optional[float] = None
    overdraft_limit: Optional[float] = None


class DepositRequest(BaseModel):
    account_number: int
    amount: float


class WithdrawRequest(BaseModel):
    account_number: int
    amount: float

# ---------- Transactions ----------

class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: float

class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    from_account: Optional[int]
    to_account: Optional[int]
    amount: float
    type: str
