import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from decimal import Decimal

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
    "check_same_thread": False
    },
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

@pytest.fixture()
def client():

    #Setup
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    #Test Client
    with TestClient(app) as test_client:
        yield test_client

    #Cleanup
    app.dependency_overrides.pop(get_db, None)
    Base.metadata.drop_all(bind=test_engine)

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Expense Management System (EMS) is running"
    }

def test_create_expense(client):
    expense_body = {
        "amount": "200",
        "category": "Food",
        "description": "Lunch expense",
        "time": "2026-10-27"
    }
    response = client.post("/expenses/createExpense", json=expense_body)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["category"] == "Food"
    assert data["description"] == "Lunch expense"

def test_get_expense_by_id(client):
    expense_body = {
        "amount": "136",
        "category": "Cab",
        "description": "Travel expense",
        "time": "2026-10-27"
    }

    expense_id = client.post("/expenses/createExpense", json=expense_body).json()["id"]
    get_expense_by_id_response = client.get(f"/expenses/getExpense/{expense_id}")
    assert get_expense_by_id_response.status_code == 200
    assert get_expense_by_id_response.json()["id"] == expense_id

def test_update_expense(client):
    expense_body = {
        "amount": "136",
        "category": "Cab",
        "description": "Travel expense",
        "time": "2026-10-27"
    }
    
    expense_id = client.post("/expenses/createExpense", json=expense_body).json()["id"]

    updated_expense_body = {
            "amount": "178",
            "category": "Cab - updated",
            "description": "Travel expense - updated",
            "time": "2026-10-27"
        }

    update_expense_response = client.put(f"/expenses/updateExpense/{expense_id}", json=updated_expense_body)
    assert update_expense_response.status_code == 200
    assert update_expense_response.json()["category"] == updated_expense_body["category"]
    assert update_expense_response.json()["description"] == updated_expense_body["description"]
    assert Decimal(str(update_expense_response.json()["amount"])) == Decimal(updated_expense_body["amount"])

def test_delete_expense(client):
    expense_body = {
        "amount": "136",
        "category": "Cab - deleted record",
        "description": "Travel expense for deletion",
        "time": "2026-10-27"
    }
        
    expense_id = client.post("/expenses/createExpense", json=expense_body).json()["id"]

    delete_expense_response = client.delete(f"/expenses/deleteExpense/{expense_id}")
    assert delete_expense_response.status_code == 200
    assert delete_expense_response.json() == {
        "id": expense_id,
        "amount": "136.00",
        "category": "Cab - deleted record",
        "description": "Travel expense for deletion",
        "time": "2026-10-27"
    }

def test_invalid_input(client):
    expense_body = {
        "amount": "-200",
        "category": "Food",
        "description": "Lunch expense",
        "time": "2026-10-27"
        }
    response = client.post("/expenses/createExpense", json=expense_body)
    assert response.status_code == 422

def test_get_all_expenses(client):

    create_test_expense(client, {
        "amount": "200",
        "category": "Food",
        "description": "Lunch expense",
        "time": "2026-10-27"
    })
    
    response = client.get("/expenses/getAllExpense")

    assert response.status_code == 200
    assert len(response.json()) == 1

def test_delete_all_expenses(client):
    create_test_expense(client, {
            "amount": "200",
            "category": "Food",
            "description": "Lunch expense",
            "time": "2026-10-27"
        })

    create_test_expense(client, {
            "amount": "2010",
            "category": "Food",
            "description": "Dinner expense",
            "time": "2026-10-28"
        })

    response = client.delete("/expenses/deleteAllExpenses")
    assert response.status_code == 200
    assert response.json() == {
        "message": "All 2 expenses deleted"
    }

    get_response = client.get("/expenses/getAllExpense")
    assert get_response.status_code == 200
    assert get_response.json() == []

def test_get_expense_not_found(client):
    response = client.get("/expenses/getExpense/999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Expense not found"
    }

def test_update_expense_not_found(client):
    updated_expense_body = {
                "amount": "178",
                "category": "Cab - updated",
                "description": "Travel expense - updated",
                "time": "2026-10-27"
            }
    update_expense_response = client.put("/expenses/updateExpense/8987", json=updated_expense_body)
    assert update_expense_response.status_code == 404
    assert update_expense_response.json() == {
        "detail": "Expense not found"
    }

def test_delete_expense_not_found(client):
    expense_body = {
                "amount": "178",
                "category": "Cab - updated",
                "description": "Travel expense - updated",
                "time": "2026-10-27"
            }
    expense_response = client.put("/expenses/updateExpense/8987", json=expense_body)
    assert expense_response.status_code == 404
    assert expense_response.json() == {
        "detail": "Expense not found"
    }

def create_test_expense(client, expense_body):
    return client.post("/expenses/createExpense", json=expense_body)