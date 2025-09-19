import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.config import settings
from app.models import UrlMap

ALPHABET = string.ascii_letters + string.digits

def _now() -> datetime:
    return datetime.utcnow()

def generate_code(min_len: int, max_len: int) -> str:
    n = secrets.choice(list(range(min_len, max_len + 1)))
    return "".join(secrets.choice(ALPHABET) for _ in range(n))

def find_by_code(db: Session, code: str) -> Optional[UrlMap]:
    stmt = select(UrlMap).where(UrlMap.code == code)
    return db.execute(stmt).scalar_one_or_none()

def create_short_url(db: Session, long_url: str) -> UrlMap:
    for _ in range(20):
        code = generate_code(settings.CODE_MIN_LENGTH, settings.CODE_MAX_LENGTH)
        if find_by_code(db, code) is None:
            break
    else:
        raise RuntimeError("Não foi possível gerar código único para URL curta.")

    expires_at = _now() + timedelta(minutes=settings.DEFAULT_TTL_MINUTES)
    obj = UrlMap(code=code, long_url=long_url, expires_at=expires_at)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def is_expired(m: UrlMap) -> bool:
    return _now() >= m.expires_at
