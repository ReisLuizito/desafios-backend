from fastapi import FastAPI, Depends, HTTPException, Header, Request, status, Response
from sqlalchemy.orm import Session
from app.db import Base, engine, get_session
from app.config import settings
from app.schemas import TransferIn, TransferOut
from app.models import Transfer
from app import services

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Idempotent Transfers Challenge")

def hmac_compare(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y
    return result == 0

@app.post("/transfers", response_model=TransferOut, status_code=201)
async def create_transfer_endpoint(
    request: Request,
    response: Response,
    payload: TransferIn,
    x_idempotency_key: str | None = Header(default=None),
    x_signature: str | None = Header(default=None),
    db: Session = Depends(get_session),
):
    if not x_idempotency_key:
        raise HTTPException(status_code=400, detail="Missing X-Idempotency-Key")
    if not x_signature:
        raise HTTPException(status_code=401, detail="Missing X-Signature")

    import json
    raw_body = json.dumps(payload.model_dump(), separators=(",", ":")).encode("utf-8")

    expected = services.body_signature(settings.SIGNING_SECRET, raw_body)
    if not hmac_compare(x_signature, expected):
        raise HTTPException(status_code=401, detail="Invalid signature")

    existing = services.find_by_idem_key(db, x_idempotency_key)
    current_hash = services.sha256_hex(raw_body)
    if existing:
        if existing.body_hash != current_hash:
            raise HTTPException(status_code=409, detail="Idempotency key reused with a different payload")
        response.status_code = status.HTTP_200_OK
        return TransferOut.model_validate(existing)

    created = services.create_transfer(db, payload.model_dump(), x_idempotency_key, raw_body)
    return TransferOut.model_validate(created)


@app.get("/transfers/{transfer_id}", response_model=TransferOut)
def get_transfer(transfer_id: int, db: Session = Depends(get_session)):
    t = db.get(Transfer, transfer_id)
    if not t:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return TransferOut.model_validate(t)
