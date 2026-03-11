from sqlalchemy import Column, Integer, String, Numeric, Enum as SQLEnum, Date, DateTime, CheckConstraint
from sqlalchemy.sql import func
from enum import Enum
from app.core.database import Base

class ProductStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'

class SavingsProduct(Base):
    __tablename__ = 'savings_products'

    savings_product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_code = Column(String(50), nullable=False, unique=True, index=True)
    product_name = Column(String(100), nullable=False, unique=True)
    
    interest_rate_percent = Column(Numeric(5, 2), nullable=False)
    minimum_opening_balance_amount = Column(Numeric(15, 2), nullable=False)
    minimum_maintaining_balance_amount = Column(Numeric(15, 2), nullable=False)
    
    interest_application_frequency_code = Column(String(20), nullable=False, default='MONTHLY')
    product_status = Column(SQLEnum(ProductStatus, name='enum_product_status'), nullable=False, default=ProductStatus.ACTIVE)
    
    effective_from_date = Column(Date, nullable=False, default=func.current_date())
    expiry_date = Column(Date, nullable=True)

    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)
    created_by = Column(String(100), nullable=False)
    updated_by = Column(String(100), nullable=True)

    __table_args__ = (
        CheckConstraint('interest_rate_percent >= 0.00 AND interest_rate_percent <= 20.00', name='chk_savings_product_interest_rate'),
        CheckConstraint('minimum_opening_balance_amount >= 0 AND minimum_opening_balance_amount <= 10000000.00', name='chk_savings_product_min_open_balance'),
        CheckConstraint('minimum_maintaining_balance_amount >= 0', name='chk_savings_product_min_maint_balance'),
        CheckConstraint('expiry_date IS NULL OR expiry_date >= effective_from_date', name='chk_expiry_after_effective'),
        CheckConstraint('min_age >= 10 AND min_age <= 100', name='chk_min_age_range'),
        CheckConstraint('max_age >= 10 AND max_age <= 100', name='chk_max_age_range'),
        CheckConstraint('max_age >= min_age', name='chk_age_range_valid'),
    )
