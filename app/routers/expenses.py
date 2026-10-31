from fastapi import APIRouter, HTTPException, Depends
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.expense import Expense

router = APIRouter(prefix="/expenses", tags=["Expense"])

@router.post("/createExpense", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/getAllExpense")
def getAllExpenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()

@router.get("/getExpense/{expense_id}")
def getExpense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404, detail="Expense not found"
        )
    return expense

@router.put("/updateExpense/{expense_id}")
def updateExpense(
    expense_id: int,
    updated_expense: ExpenseCreate,
    db: Session = Depends(get_db)):

    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found")
    
    expense.amount = updated_expense.amount
    expense.category = updated_expense.category
    expense.description = updated_expense.description
    expense.time = updated_expense.time

    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/deleteExpense/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)):

    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found")

    db.delete(expense)
    db.commit()
    return expense

@router.delete("/deleteAllExpenses")
def delete_all_expense(
    db: Session = Depends(get_db)):

    deleted_count = db.query(Expense).delete()
    db.commit()
    return {
        "message": f"All {deleted_count} expenses deleted"
    }