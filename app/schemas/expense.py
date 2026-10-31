from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import date

class ExpenseCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)
    time: date

class ExpenseResponse(BaseModel):
    id: int
    category: str
    description: str
    amount: Decimal
    time: date

    model_config = ConfigDict(from_attributes=True)