from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime
from app.db import Base

class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    currency = Column(String(8), nullable=False)
    beneficiary_account = Column(String(128), nullable=False)
    idempotency_key = Column(String(64), unique=True, index=True, nullable=False)
    body_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=False), default=lambda: datetime.utcnow(), nullable=False)

Index("ix_transfers_idempotency_key_unique", Transfer.idempotency_key, unique=True)