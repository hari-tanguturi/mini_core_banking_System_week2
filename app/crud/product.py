from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.product import SavingsProduct, ProductStatus
from app.schemas.product import ProductCreateRequest


def get_product_by_code(db: Session, product_code: str) -> Optional[SavingsProduct]:
    return db.query(SavingsProduct).filter(SavingsProduct.product_code == product_code).first()


def get_product_by_name(db: Session, product_name: str) -> Optional[SavingsProduct]:
    return db.query(SavingsProduct).filter(SavingsProduct.product_name == product_name).first()


def get_product_by_name_or_code(db: Session, product_name: str, product_code: str) -> Optional[SavingsProduct]:
    return db.query(SavingsProduct).filter(
        (SavingsProduct.product_name == product_name) |
        (SavingsProduct.product_code == product_code)
    ).first()


def get_all_products(db: Session) -> List[SavingsProduct]:
    return db.query(SavingsProduct).all()


def create_product(db: Session, request: ProductCreateRequest, created_by: str) -> SavingsProduct:
    data = request.model_dump()
    data["created_by"] = created_by
    new_product = SavingsProduct(**data)
    db.add(new_product)
    try:
        db.commit()
        db.refresh(new_product)
    except:
        db.rollback()
        raise
    return new_product


def update_product(db: Session, db_product: SavingsProduct, update_data: Dict[str, Any]) -> SavingsProduct:
    for key, value in update_data.items():
        setattr(db_product, key, value)
    try:
        db.commit()
        db.refresh(db_product)
    except:
        db.rollback()
        raise
    return db_product


def deactivate_product(db: Session, db_product: SavingsProduct, updated_by: str) -> SavingsProduct:
    db_product.product_status = ProductStatus.INACTIVE
    db_product.updated_by = updated_by
    try:
        db.commit()
        db.refresh(db_product)
    except:
        db.rollback()
        raise
    return db_product
