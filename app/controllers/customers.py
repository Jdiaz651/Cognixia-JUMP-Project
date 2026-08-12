from fastapi import APIRouter, HTTPException
from app.models.schemas import CustomerCreate, CustomerUpdate, CustomerOut
from app.services import customer_service as svc
from app.services.customer_service import CustomerNotFound

router = APIRouter(prefix="/api/v1/customers", tags=["customers"])


@router.post("", response_model=CustomerOut)
def create_customer(payload: CustomerCreate):
    return svc.create(payload.name, payload.email, payload.branch_id)


@router.get("", response_model=list[CustomerOut])
def list_customers():
    return svc.list_all()


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: str):
    try:
        return svc.get(customer_id)
    except CustomerNotFound:
        raise HTTPException(status_code=404, detail="Customer not found")


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: str, payload: CustomerUpdate):
    try:
        return svc.update(customer_id, payload.name, payload.email)
    except CustomerNotFound:
        raise HTTPException(status_code=404, detail="Customer not found")


@router.delete("/{customer_id}", response_model=CustomerOut)
def deactivate_customer(customer_id: str):
    try:
        return svc.delete(customer_id)
    except CustomerNotFound:
        raise HTTPException(status_code=404, detail="Customer not found")