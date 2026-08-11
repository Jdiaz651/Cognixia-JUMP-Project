from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException
from app.models.schemas import TransferRequest, TransactionOut
from app.services import transaction_service as svc
from app.services.account_service import AccountNotFound
from app.store import bank

router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


@router.post("/transfer", response_model=TransactionOut)
def transfer(payload: TransferRequest):
    try:
        return svc.transfer(bank, payload.from_account, payload.to_account, payload.amount)
    except AccountNotFound as e:
        raise HTTPException(status_code=404, detail=f"Account {e} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[TransactionOut])
def list_transactions(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    type: Optional[str] = None,
):
    return svc.list_all(bank, start_date=start_date, end_date=end_date, type=type)