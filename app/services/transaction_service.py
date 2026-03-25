from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    data = transaction.model_dump()

    data.update({
        "category": transaction.category.value,
        "transaction_type": transaction.transaction_type.value,
        "user_id": user_id
    })

    try:
        db_transaction = Transaction(**data)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except SQLAlchemyError:
        db.rollback()
        raise