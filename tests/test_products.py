from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from datetime import date, timedelta

from app.main import app
from app.core.database import Base, get_db
from app.core.dependencies import get_current_admin, get_current_user

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/mini_core_banking_test"

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

valid_date = (date.today() + timedelta(days=1)).isoformat()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_get_current_admin():
        return {"sub": "bank_admin", "role": "ADMIN"}

    def override_get_current_user():
        return {"sub": "bank_admin", "role": "ADMIN"}

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_admin] = override_get_current_admin
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c


def test_create_savings_product(client):
    """Create a standard savings account product."""
    response = client.post("/api/products/", json={
        "product_code": "SB_REGULAR_001",
        "product_name": "Regular Savings Account",
        "interest_rate_percent": 3.50,
        "minimum_opening_balance_amount": 1000.00,
        "minimum_maintaining_balance_amount": 500.00,
        "interest_application_frequency_code": "QUARTERLY",
        "effective_from_date": valid_date,
        "expiry_date": "2030-12-31",
        "min_age": 18,
        "max_age": 70
    })
    assert response.status_code == 201
    assert response.json()["product_code"] == "SB_REGULAR_001"
    assert "savings_product_id" in response.json()
    assert "created_at" in response.json()


def test_create_product_with_negative_interest_rate_fails(client):
    """Interest rate below 0 must be rejected."""
    response = client.post("/api/products/", json={
        "product_code": "SB_INVALID_001",
        "product_name": "Invalid Interest Savings",
        "interest_rate_percent": -2.00,
        "minimum_opening_balance_amount": 1000.00,
        "minimum_maintaining_balance_amount": 500.00,
        "effective_from_date": valid_date,
        "min_age": 18,
        "max_age": 65
    })
    assert response.status_code == 422


def test_get_savings_product_by_code(client):
    """Fetch a specific product by its product code."""
    client.post("/api/products/", json={
        "product_code": "SB_WOMEN_001",
        "product_name": "Mahila Savings Account",
        "interest_rate_percent": 4.00,
        "minimum_opening_balance_amount": 500.00,
        "minimum_maintaining_balance_amount": 250.00,
        "interest_application_frequency_code": "MONTHLY",
        "effective_from_date": valid_date,
        "min_age": 18,
        "max_age": 65
    })

    response = client.get("/api/products/SB_WOMEN_001")
    assert response.status_code == 200
    assert response.json()["product_code"] == "SB_WOMEN_001"
    assert response.json()["product_name"] == "Mahila Savings Account"
    assert response.json()["interest_rate_percent"] == "4.00"


def test_get_product_with_invalid_code_returns_404(client):
    """Fetching a non-existent product must return 404."""
    response = client.get("/api/products/NONEXISTENT_CODE")
    assert response.status_code == 404


@pytest.mark.parametrize("code,name,interest,min_open,min_main,min_age,max_age", [
    ("SB_STUDENT_001", "Student Savings Account", 3.00, 250.00, 0.00, 10, 25),
    ("SB_SENIOR_001", "Senior Citizen Savings Account", 5.50, 1000.00, 500.00, 60, 100),
    ("SB_SALARY_001", "Corporate Salary Account", 3.25, 0.00, 0.00, 18, 65),
])
def test_create_multiple_product_types(client, code, name, interest, min_open, min_main, min_age, max_age):
    """Create different product types that a real bank would offer."""
    response = client.post("/api/products/", json={
        "product_code": code,
        "product_name": name,
        "interest_rate_percent": interest,
        "minimum_opening_balance_amount": min_open,
        "minimum_maintaining_balance_amount": min_main,
        "interest_application_frequency_code": "MONTHLY",
        "effective_from_date": valid_date,
        "min_age": min_age,
        "max_age": max_age
    })
    assert response.status_code == 201


def test_update_savings_product_interest_rate(client):
    """Update the interest rate of an existing product (RBI rate revision scenario)."""
    response = client.patch("/api/products/SB_REGULAR_001", json={
        "interest_rate_percent": 4.00,
        "minimum_maintaining_balance_amount": 750.00
    })
    assert response.status_code == 200
    assert response.json()["product_code"] == "SB_REGULAR_001"
    assert response.json()["interest_rate_percent"] == "4.00"
    assert response.json()["updated_by"] == "bank_admin"


def test_deactivate_savings_product(client):
    """Soft delete (deactivate) a product — product is discontinued but not erased."""
    response = client.delete("/api/products/SB_REGULAR_001")
    assert response.status_code == 200
    assert response.json()["product_code"] == "SB_REGULAR_001"
    assert response.json()["product_status"] == "INACTIVE"
    assert response.json()["updated_by"] == "bank_admin"
