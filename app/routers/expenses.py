from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.expenses import (create_expense_service, get_expense_by_id_service,
        get_all_expenses_service, update_expense_service,delete_expense_service, delete_all_expenses_service)

router = APIRouter(prefix="/expenses", tags=["Expense"])

@router.post("/createExpense", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return create_expense_service(expense, db)

@router.get("/getExpense/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = get_expense_by_id_service(expense_id, db)
    if expense is None:
        raise HTTPException(
            status_code=404, detail="Expense not found"
        )
    return expense

@router.get("/getAllExpense", response_model=list[ExpenseResponse])
def get_all_expenses(db: Session = Depends(get_db)):
    return get_all_expenses_service(db)

@router.put("/updateExpense/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, updated_expense: ExpenseCreate, db: Session = Depends(get_db)):
    expense = update_expense_service(expense_id, updated_expense, db)
    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found")
    return expense

@router.delete("/deleteExpense/{expense_id}",response_model=ExpenseResponse)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = delete_expense_service(expense_id, db)
    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found")
    return expense

@router.delete("/deleteAllExpenses")
def delete_all_expense(db: Session = Depends(get_db)):
    return {
        "message": f"All {delete_all_expenses_service(db)} expenses deleted"
    }