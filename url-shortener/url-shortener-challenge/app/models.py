from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime
from app.db import Base

class UrlMap(Base):
    __tablename__ = "url_map"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(16), unique=True, index=True, nullable=False)
    long_url = Column(String(2048), nullable=False)
    created_at = Column(DateTime(timezone=False), default=lambda: datetime.utcnow(), nullable=False)
    expires_at = Column(DateTime(timezone=False), nullable=False)
