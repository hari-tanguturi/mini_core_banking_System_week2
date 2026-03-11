from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.product import ProductStatus


class ProductBase(BaseModel):
    product_code: str = Field(..., max_length=50, examples=["ENTER THE PRODUCT CODE IT SHOULD BE UNIQUE"])
    product_name: str = Field(..., min_length=3, max_length=100, examples=["ENTER THE PRODUCT NAME"])
    interest_rate_percent: Decimal = Field(..., ge=0.00, le=20.00, decimal_places=2, examples=[4.50])
    minimum_opening_balance_amount: Decimal = Field(..., ge=0, le=10000000.00, decimal_places=2, examples=[1000.00])
    minimum_maintaining_balance_amount: Decimal = Field(..., ge=0, decimal_places=2, examples=[500.00])
    interest_application_frequency_code: str = Field(default="MONTHLY", max_length=20, examples=["MONTHLY"])
    effective_from_date: date = Field(..., examples=["YYYY-MM-DD"])
    expiry_date: Optional[date] = Field(None, examples=["YYYY-MM-DD"])
    min_age: int = Field(..., ge=10, le=100, examples=[18])
    max_age: int = Field(..., ge=10, le=100, examples=[65])

    @model_validator(mode='after')
    def validate_dates_and_ages(self) -> 'ProductBase':
        today = date.today()
        if self.expiry_date:
            if self.expiry_date <= today:
                raise ValueError('expiry_date must be a future date')
            if self.expiry_date <= self.effective_from_date:
                raise ValueError('expiry_date must be after effective_from_date')

        if self.min_age is not None and self.max_age is not None and self.max_age < self.min_age:
            raise ValueError('max_age must be >= min_age')

        if self.minimum_maintaining_balance_amount > self.minimum_opening_balance_amount:
            raise ValueError("minimum_maintaining_balance_amount cannot exceed minimum_opening_balance_amount")

        return self


class ProductCreateRequest(ProductBase):
    pass


class ProductUpdateRequest(BaseModel):
    product_name: Optional[str] = Field(None, max_length=100, examples=["Premium Savings Account"])
    interest_rate_percent: Optional[Decimal] = Field(None, ge=0, le=20.00, decimal_places=2, examples=[5.25])
    minimum_opening_balance_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2, examples=[2000.00])
    minimum_maintaining_balance_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2, examples=[1000.00])
    interest_application_frequency_code: Optional[str] = Field(None, max_length=20, examples=["MONTHLY"])
    effective_from_date: Optional[date] = Field(None, examples=["YYYY-MM-DD"])
    expiry_date: Optional[date] = Field(None, examples=["YYYY-MM-DD"])
    min_age: Optional[int] = Field(None, ge=10, le=100, examples=[18])
    max_age: Optional[int] = Field(None, ge=10, le=100, examples=[70])

    @model_validator(mode='after')
    def validate_dates_and_ages(self) -> 'ProductUpdateRequest':
        today = date.today()
        if self.effective_from_date and self.effective_from_date < today:
            raise ValueError('effective_from_date must be today or a future date')
        if self.expiry_date and self.expiry_date <= today:
            raise ValueError('expiry_date must be a future date')
        if self.effective_from_date and self.expiry_date and self.expiry_date <= self.effective_from_date:
            raise ValueError('expiry_date must be after effective_from_date')
        if self.min_age is not None and self.max_age is not None and self.max_age < self.min_age:
            raise ValueError('max_age must be >= min_age')
        return self


class ProductResponse(ProductBase):
    savings_product_id: int
    product_status: ProductStatus
    created_by: str
    updated_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProductCreateResponse(BaseModel):
    savings_product_id: int
    product_code: str
    created_by: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ProductDeleteResponse(BaseModel):
    product_code: str
    product_name: str
    product_status: ProductStatus
    updated_by: Optional[str]
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "product_code": "PREMIUM_SAV_01",
                "product_name": "Premium Savings Plus",
                "product_status": "INACTIVE",
                "updated_by": "bank_admin",
                "updated_at": "2026-03-05T08:00:00.000Z"
            }
        }
    }
