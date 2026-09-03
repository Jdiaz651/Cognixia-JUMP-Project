from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from backend.models.schemas import TokenData
from backend.services import customer_service as svc

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/customers/login")

# Re-using the same configuration as in customers.py for simplicity in this example
# In a real app, these would be in a config file or env vars.
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = svc.get_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user
