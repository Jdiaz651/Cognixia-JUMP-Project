from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from backend.models.schemas import TransferRequest, TransactionOut
from backend.services import transaction_service as svc
from backend.services.account_service import AccountNotFound
from backend.auth import get_current_user

router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


@router.post("/transfer", response_model=TransactionOut)
def transfer(payload: TransferRequest, current_user: dict = Depends(get_current_user)):
    try:
        return svc.transfer(payload.from_account, payload.to_account, payload.amount)
    except AccountNotFound as e:
        raise HTTPException(status_code=404, detail=f"Account {e} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[TransactionOut])
def list_transactions(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    type: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    return svc.list_all(start_date=start_date, end_date=end_date, type=type)
