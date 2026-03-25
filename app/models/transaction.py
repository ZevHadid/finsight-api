from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.schemas.transaction import TransactionType, TransactionCategory

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    category = Column(String(50), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    note = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="transactions")
