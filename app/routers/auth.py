from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from app.core.security import create_access_token
from app.core.config import settings
from datetime import timedelta

router = APIRouter()

ADMIN_USERNAME = "bank_admin"
ADMIN_PASSWORD = "Admin@24"
CUSTOMER_USERNAME = "bank_user"
CUSTOMER_PASSWORD = "User@123"


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=15, examples=["your_username"])
    password: str = Field(..., min_length=6, max_length=8, examples=["P@ssw0rd"])

    @field_validator("username")
    @classmethod
    def username_no_spaces(cls, v):
        if " " in v:
            raise ValueError("Username must not contain spaces")
        return v

    @field_validator("password")
    @classmethod
    def password_no_spaces(cls, v):
        if " " in v:
            raise ValueError("Password must not contain spaces")
        return v


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    message: str


@router.post("/login", response_model=LoginResponse, summary="Admin Login")
def login_for_access_token(request: LoginRequest):
    if request.username == ADMIN_USERNAME and request.password == ADMIN_PASSWORD:
        role = "ADMIN"
        message = "Login successful."
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": request.username, "role": role},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        role=role,
        message=message
    )
