from fastapi import APIRouter, HTTPException
from backend.models.schemas import CustomerCreate, CustomerUpdate, CustomerOut
from backend.services import customer_service as svc
from backend.services.customer_service import CustomerNotFound
from backend.models.schemas import CustomerLogin 

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

    from backend.models.schemas import CustomerLogin  # Import your schema

@router.post("/login", response_model=CustomerOut)
def login_customer(payload: CustomerLogin):
    try:
        return svc.login(name=payload.name, email=payload.email)
    except CustomerNotFound:
        raise HTTPException(status_code=401, detail="Invalid name or email combination")