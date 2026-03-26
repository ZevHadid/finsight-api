from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
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

def get_user_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit).all()

def get_transaction_summary(db: Session, user_id: int):
    # Get total income
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "income"
    ).scalar() or 0.0

    # Get total expense
    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "expense"
    ).scalar() or 0.0

    # Get expenses by category
    category_expenses = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total_amount")
    ).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "expense"
    ).group_by(Transaction.category).all()

    expenses_by_category = [
        {"category": row[0], "total_amount": row[1]}
        for row in category_expenses
    ]

    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "balance": float(total_income - total_expense),
        "expenses_by_category": expenses_by_category
    }