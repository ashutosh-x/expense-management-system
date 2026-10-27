import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers import expenses as expenses_modules

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_expense():    
    expenses_modules.expenses.clear()
    expenses_modules.expense_id_counter = 1

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Expense Management System (EMS) is running"
    }

def test_create_expense():
    expense_body = {
        "amount": "200",
        "category": "Food",
        "description": "Lunch expense",
        "time": "2026-10-27"
    }
    response = client.post("/expenses/createExpense", json=expense_body)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] is not None
    assert data["category"] == "Food"
    assert data["description"] == "Lunch expense"

def test_get_expense_by_id():
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

def test_update_expense():
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
    assert update_expense_response.json()["amount"] == updated_expense_body["amount"]

def test_delete_expense():
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
        "amount": "136",
        "category": "Cab - deleted record",
        "description": "Travel expense for deletion",
        "time": "2026-10-27"
    }

def test_invalid_input():
    expense_body = {
        "amount": "-200",
        "category": "Food",
        "description": "Lunch expense",
        "time": "2026-10-27"
        }
    response = client.post("/expenses/createExpense", json=expense_body)
    assert response.status_code == 422