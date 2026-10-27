from fastapi import APIRouter, HTTPException
import app.schemas.expense as schema_expense

router = APIRouter(prefix="/expenses", tags=["Expense"])
expense_id_counter = 1
expenses = []

@router.post("/createExpense")
def create_expense(expense: schema_expense.ExpenseCreate):
    global expense_id_counter

    new_expense = {
        "id": expense_id_counter,
        **expense.model_dump(mode="json"),
    }
    expenses.append(new_expense)
    expense_id_counter += 1
    return new_expense

@router.get("/getAllExpense")
def getAllExpenses():
    return expenses

@router.get("/getExpense/{expense_id}")
def getExpense(expense_id: int):
    for expense in expenses:
        if expense_id == expense["id"]:
            return expense
    raise HTTPException(status_code=404, detail="Not found")

@router.put("/updateExpense/{expense_id}")
def updateExpense(expense_id: int, updated_expense: schema_expense.ExpenseCreate):
    for index, expense in enumerate(expenses):
        if expense_id == expense["id"]:
            expenses[index] = {
                "id": expense_id,
                **updated_expense.model_dump(mode="json")
            }
            return expenses[index]
    raise HTTPException(status_code=404, detail="Expense not found")

@router.delete("/deleteExpense/{expense_id}")
def delete_expense(expense_id: int):
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            return expenses.pop(index)
    raise HTTPException(status_code=404, detail="Expense not found")
