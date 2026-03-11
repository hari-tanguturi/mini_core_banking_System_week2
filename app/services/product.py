from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.crud import product as crud_product
from app.models.product import SavingsProduct
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest


class ProductService:
    @staticmethod
    def create_product(db: Session, request: ProductCreateRequest, created_by: str) -> SavingsProduct:
        existing = crud_product.get_product_by_name_or_code(
            db=db, product_name=request.product_name, product_code=request.product_code
        )
        if existing:
            raise HTTPException(status_code=409, detail="Product with this code or name already exists")
        return crud_product.create_product(db=db, request=request, created_by=created_by)

    @staticmethod
    def get_all_products(db: Session) -> List[SavingsProduct]:
        return crud_product.get_all_products(db=db)

    @staticmethod
    def get_product(db: Session, product_code: str) -> SavingsProduct:
        product = crud_product.get_product_by_code(db=db, product_code=product_code)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def update_product(db: Session, product_code: str, request: ProductUpdateRequest, updated_by: str) -> SavingsProduct:
        product = crud_product.get_product_by_code(db=db, product_code=product_code)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        update_data = request.model_dump(exclude_unset=True)
        update_data["updated_by"] = updated_by

        if 'product_name' in update_data and update_data['product_name'] != product.product_name:
            conflict = crud_product.get_product_by_name(db=db, product_name=update_data['product_name'])
            if conflict:
                raise HTTPException(status_code=400, detail="Product name already exists")

        if 'expiry_date' in update_data and 'effective_from_date' not in update_data:
            if update_data['expiry_date'] and update_data['expiry_date'] <= product.effective_from_date:
                raise HTTPException(status_code=400, detail="New expiry date must be strictly after existing effective_from_date")

        if 'effective_from_date' in update_data and 'expiry_date' not in update_data:
            if product.expiry_date and update_data['effective_from_date'] >= product.expiry_date:
                raise HTTPException(status_code=400, detail="New effective_from_date must be strictly before existing expiry_date")

        if 'max_age' in update_data and 'min_age' not in update_data:
            if update_data['max_age'] is not None and product.min_age is not None and update_data['max_age'] < product.min_age:
                raise HTTPException(status_code=400, detail="New max_age cannot be less than existing min_age")

        return crud_product.update_product(db=db, db_product=product, update_data=update_data)

    @staticmethod
    def deactivate_product(db: Session, product_code: str, updated_by: str) -> SavingsProduct:
        product = crud_product.get_product_by_code(db=db, product_code=product_code)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return crud_product.deactivate_product(db=db, db_product=product, updated_by=updated_by)


product_service = ProductService()
