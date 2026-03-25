from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class TransactionCategory(str, Enum):
    housing = "housing"
    transportation = "transportation"
    food = "food"
    utilities = "utilities"
    insurance = "insurance"
    healthcare = "healthcare"
    personal_care = "personal_care"
    entertainment = "entertainment"
    education = "education"
    debt_payments = "debt_payments"
    savings_investments = "savings_investments"
    miscellaneous_expense = "miscellaneous_expense"

    salary = "salary"
    freelance = "freelance"
    investments_income = "investments_income"
    gifts = "gifts"
    bonus = "bonus"
    rental_income = "rental_income"
    miscellaneous_income = "miscellaneous_income"

class TransactionBase(BaseModel):
    description: str = Field(..., max_length=255)
    amount: float = Field(..., gt=0)
    transaction_date: datetime = Field(default_factory=datetime.now)
    category: TransactionCategory
    transaction_type: TransactionType
    note: Optional[str] = Field(None, max_length=500)

class TransactionCreate(TransactionBase):
    pass

class TransactionInDBBase(TransactionBase):
    id: Optional[int] = None
    user_id: int

    class Config:
        from_attributes = True

class Transaction(TransactionInDBBase):
    pass
