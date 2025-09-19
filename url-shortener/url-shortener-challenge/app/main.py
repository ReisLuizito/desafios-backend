from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db import Base, engine, get_session
from app.schemas import ShortenRequest, ShortUrlResponse
from app.config import settings
from app import services

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener Challenge")

@app.post("/shorten-url", response_model=ShortUrlResponse)
def shorten_url(payload: ShortenRequest, db: Session = Depends(get_session)):
    created = services.create_short_url(db, str(payload.url))
    short = f"{settings.BASE_URL.rstrip('/')}/{created.code}"
    return ShortUrlResponse(url=short)

@app.get("/{code}")
def resolve(code: str, db: Session = Depends(get_session)):
    m = services.find_by_code(db, code)
    if not m or services.is_expired(m):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada ou expirada.")
    return RedirectResponse(url=m.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
