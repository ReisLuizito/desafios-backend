import hashlib
import hmac
import base64
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Transfer

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def body_signature(secret: str, raw_body: bytes) -> str:
    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("ascii")

def find_by_idem_key(db: Session, key: str) -> Optional[Transfer]:
    stmt = select(Transfer).where(Transfer.idempotency_key == key)
    return db.execute(stmt).scalar_one_or_none()

def create_transfer(db: Session, payload: dict, idem_key: str, raw_body: bytes) -> Transfer:
    t = Transfer(
        amount=payload["amount"],
        currency=payload["currency"],
        beneficiary_account=payload["beneficiary_account"],
        idempotency_key=idem_key,
        body_hash=sha256_hex(raw_body),
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t