from sqlalchemy import Column, Integer, String
from app.db import Base
from app.config import settings
from app.types.encrypted_string import EncryptedString

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    userDocument = Column(EncryptedString(settings.encryption_key_bytes, length=512), nullable=False)
    creditCardToken = Column(EncryptedString(settings.encryption_key_bytes, length=512), nullable=False)
    value = Column(Integer, nullable=False)
