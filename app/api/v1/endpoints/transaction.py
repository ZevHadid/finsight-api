from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.services import transaction_service
from app.schemas.transaction import TransactionCreate, Transaction
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
