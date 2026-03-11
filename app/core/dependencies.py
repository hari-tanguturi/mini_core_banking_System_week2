from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token

security = HTTPBearer()

def get_current_user_token_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

def get_current_user(payload: dict = Depends(get_current_user_token_payload)):
    """Any authenticated user (Admin or Customer)"""
    return payload

def get_current_admin(payload: dict = Depends(get_current_user_token_payload)):
    """Only an Admin"""
    role = payload.get("role")
    if role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admins only."
        )
    return payload
