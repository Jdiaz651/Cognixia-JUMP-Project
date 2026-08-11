# controllers/customers.py
from fastapi import APIRouter
from app.models.schemas import CustomerCreate, CustomerOut
from app.services import customer_service as svc
from app.store import bank

router = APIRouter(prefix="/api/v1/customers", tags=["customers"])


@router.post("", response_model=CustomerOut)
def create_customer(payload: CustomerCreate):
    return svc.create(bank, payload.name, payload.email, payload.branch_id)


@router.get("", response_model=list[CustomerOut])
def list_customers():
    return svc.list_all(bank)