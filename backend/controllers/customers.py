from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from backend.models.schemas import CustomerCreate, CustomerUpdate, CustomerOut, Token
from backend.services import customer_service as svc
from backend.services.customer_service import CustomerNotFound, AuthenticationError
from backend.auth import get_current_user

router = APIRouter(prefix="/api/v1/customers", tags=["customers"])

# Security configuration (Should be in env)
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




@router.post("", response_model=CustomerOut)
def register_customer(payload: CustomerCreate):
    try:
        return svc.create(
            payload.name,
            payload.email,
            payload.password,
            payload.branch_id,
            is_admin=payload.is_admin
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login_customer(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = svc.authenticate(form_data.username, form_data.password)
        access_token = create_access_token(data={"sub": user["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Incorrect email or password")


@router.get("/me", response_model=CustomerOut)
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/email", response_model=CustomerOut)
def get_by_email(email: str = Query(...)):
    user = svc.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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
