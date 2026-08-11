from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import AccountCreate, AccountOut
from app.services import account_service as svc
from app.services.customer_service import CustomerNotFound
from app.store import bank

router = APIRouter(prefix="/api/v1/accounts", tags=["accounts"])


@router.post("", response_model=AccountOut)
def create_account(payload: AccountCreate):
    try:
        return svc.create(bank, payload.owner_id, payload.account_type, payload.balance)
    except CustomerNotFound:
        raise HTTPException(status_code=404, detail="Owner (customer) not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[AccountOut])
def list_accounts(
    branch_id: Optional[str] = None,
    min_balance: Optional[float] = Query(None, ge=0),
):
    return svc.list_all(bank, branch_id=branch_id, min_balance=min_balance)