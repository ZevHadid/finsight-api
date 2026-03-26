from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.services import transaction_service
from app.schemas.transaction import TransactionCreate, Transaction, TransactionSummary
from app.models.user import User

router = APIRouter()

@router.post("/transactions/", response_model=Transaction)
def create_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    transaction = transaction_service.create_transaction(db=db, transaction=transaction_in, user_id=current_user.id)
    return transaction

@router.get("/history", response_model=List[Transaction])
def read_transaction_history(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve transaction history for current user.
    """
    transactions = transaction_service.get_user_transactions(db, user_id=current_user.id, skip=skip, limit=limit)
    return transactions

@router.get("/summary", response_model=TransactionSummary)
def read_transaction_summary(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve transaction summary (total income/expense/balance) for current user.
    """
    summary = transaction_service.get_transaction_summary(db, user_id=current_user.id)
    return summary
