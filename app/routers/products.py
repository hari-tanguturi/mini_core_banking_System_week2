from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_admin, get_current_user
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest, ProductResponse, ProductCreateResponse, ProductDeleteResponse
from app.services.product import product_service

router = APIRouter(prefix="/api/products", tags=["Products WEEK 2 IMPLEMENTATION CRUD OPERATIONS"])


@router.post("/", response_model=ProductCreateResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    request: ProductCreateRequest,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_username = current_admin["sub"]
    return product_service.create_product(db=db, request=request, created_by=admin_username)


@router.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return product_service.get_all_products(db=db)


@router.get("/{product_code}", response_model=ProductResponse)
def get_product(product_code: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return product_service.get_product(db=db, product_code=product_code)


@router.patch("/{product_code}", response_model=ProductResponse)
def update_product(
    product_code: str,
    request: ProductUpdateRequest,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_username = current_admin["sub"]
    return product_service.update_product(db=db, product_code=product_code, request=request, updated_by=admin_username)


@router.delete("/{product_code}", response_model=ProductDeleteResponse)
def deactivate_product(
    product_code: str,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    admin_username = current_admin["sub"]
    return product_service.deactivate_product(db=db, product_code=product_code, updated_by=admin_username)
