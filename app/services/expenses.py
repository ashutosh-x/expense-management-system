from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate

def create_expense_service(expense: ExpenseCreate, db: Session):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

def get_expense_by_id_service(expense_id: int, db: Session):
    return db.query(Expense).filter(Expense.id == expense_id).first()

def get_all_expenses_service(db: Session):
    return db.query(Expense).all()

def update_expense_service(expense_id: int, updated_expense: ExpenseCreate, db: Session):

    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        return None
    expense.amount = updated_expense.amount
    expense.category = updated_expense.category
    expense.description = updated_expense.description
    expense.time = updated_expense.time
    db.commit()
    db.refresh(expense)
    return expense

def delete_expense_service(expense_id: int, db: Session):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        return None
    db.delete(expense)
    db.commit()
    return expense

def delete_all_expenses_service(db: Session):
    deleted_count = db.query(Expense).delete()
    db.commit()
    return deleted_count