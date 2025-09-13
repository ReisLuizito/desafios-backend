from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import POI
from app.schemas import POICreate

def create_poi(db: Session, data: POICreate) -> POI:
    obj = POI(name=data.name.strip(), x=data.x, y=data.y)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_pois(db: Session) -> list[POI]:
    stmt = select(POI).order_by(POI.name.asc())
    return list(db.execute(stmt).scalars().all())
