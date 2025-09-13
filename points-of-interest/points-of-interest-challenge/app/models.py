from sqlalchemy import Column, Integer, String
from app.db import Base

class POI(Base):
    __tablename__ = "pois"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
