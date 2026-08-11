# models/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


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