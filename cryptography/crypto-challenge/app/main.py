from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import Base, engine, get_session
from app import schemas, crud

# cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Crypto Challenge")

@app.post("/payments", response_model=schemas.PaymentRead, status_code=201)
def create_payment(payload: schemas.PaymentCreate, db: Session = Depends(get_session)):
    return crud.create_payment(db, payload)

@app.get("/payments/{payment_id}", response_model=schemas.PaymentRead)
def get_payment(payment_id: int, db: Session = Depends(get_session)):
    obj = crud.get_payment(db, payment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Payment not found")
    return obj

@app.get("/payments", response_model=list[schemas.PaymentRead])
def list_payments(db: Session = Depends(get_session)):
    return crud.list_payments(db)

@app.patch("/payments/{payment_id}", response_model=schemas.PaymentRead)
def update_payment(payment_id: int, payload: schemas.PaymentUpdate, db: Session = Depends(get_session)):
    obj = crud.update_payment(db, payment_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Payment not found")
    return obj

@app.delete("/payments/{payment_id}", status_code=204)
def delete_payment(payment_id: int, db: Session = Depends(get_session)):
    ok = crud.delete_payment(db, payment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Payment not found")
    return
