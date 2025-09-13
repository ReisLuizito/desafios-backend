import math
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import POI

def euclidean_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    return math.hypot(x1 - x2, y1 - y2)

def nearby_pois(db: Session, ref_x: int, ref_y: int, dmax: float) -> list[POI]:
    stmt = select(POI)
    pois = list(db.execute(stmt).scalars().all())
    result = [p for p in pois if euclidean_distance(ref_x, ref_y, p.x, p.y) <= dmax]
    result.sort(key=lambda p: p.name.lower())
    return result
