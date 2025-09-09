from sqlalchemy.orm import Session
from app import models, schemas

def create_payment(db: Session, data: schemas.PaymentCreate) -> models.Payment:
    obj = models.Payment(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_payment(db: Session, payment_id: int) -> models.Payment | None:
    return db.get(models.Payment, payment_id)

def list_payments(db: Session) -> list[models.Payment]:
    return db.query(models.Payment).all()

def update_payment(db: Session, payment_id: int, data: schemas.PaymentUpdate) -> models.Payment | None:
    obj = get_payment(db, payment_id)
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_payment(db: Session, payment_id: int) -> bool:
    obj = get_payment(db, payment_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
