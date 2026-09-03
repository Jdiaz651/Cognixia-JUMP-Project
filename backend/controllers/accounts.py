from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from backend.models.schemas import AccountCreate, AccountOut, DepositRequest, WithdrawRequest
from backend.services import account_service as svc
from backend.services.customer_service import CustomerNotFound
from backend.auth import get_current_user

router = APIRouter(prefix="/api/v1/accounts", tags=["accounts"])


@router.post("", response_model=AccountOut)
def create_account(payload: AccountCreate, current_user: dict = Depends(get_current_user)):
    try:
        return svc.create(
            owner_id=current_user["id"],
            account_type=payload.account_type,
            balance=payload.balance,
            minimum_balance=payload.minimum_balance,
            overdraft_limit=payload.overdraft_limit
        )
    except CustomerNotFound:
        raise HTTPException(status_code=404, detail="Owner (customer) not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[AccountOut])
def list_accounts(
    branch_id: Optional[str] = None,
    min_balance: Optional[float] = Query(None, ge=0),
    current_user: dict = Depends(get_current_user)
):
    # In a real app, we'd filter by current_user's accounts.
    # For now, let's just return all accounts as a placeholder or filter by current user's accounts.
    # To keep it simple, let's just return all accounts for now.
    return svc.list_all(branch_id=branch_id, min_balance=min_balance)


@router.post("/deposit", response_model=AccountOut)
def deposit(payload: DepositRequest, current_user: dict = Depends(get_current_user)):
    try:
        return svc.deposit(payload.account_number, payload.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/withdraw", response_model=AccountOut)
def withdraw(payload: WithdrawRequest, current_user: dict = Depends(get_current_user)):
    try:
        return svc.withdraw(payload.account_number, payload.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
