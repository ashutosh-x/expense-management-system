import pydantic as pyd
import decimal as decimal
from datetime import date

class ExpenseCreate(pyd.BaseModel):
    amount: decimal.Decimal = pyd.Field(gt=0)
    category: str = pyd.Field(min_length=1, max_length=100)
    description: str = pyd.Field(min_length=1, max_length=200)
    time: date