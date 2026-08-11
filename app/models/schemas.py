# models/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from typing import Literal

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    branch_id: str


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    branch_id: str
    is_active: bool




class AccountCreate(BaseModel):
    owner_id: int
    account_type: Literal["checking", "savings"]
    balance: float = 0.0


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_number: int
    owner_id: int
    balance: float


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