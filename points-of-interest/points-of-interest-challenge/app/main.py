from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db import Base, engine, get_session
from app.schemas import POICreate, POIRead
from app import crud, services

Base.metadata.create_all(bind=engine)

app = FastAPI(title="POIs Challenge")

@app.post("/pois", response_model=POIRead, status_code=201)
def create_poi(payload: POICreate, db: Session = Depends(get_session)):
    return crud.create_poi(db, payload)

@app.get("/pois", response_model=list[POIRead])
def get_pois(db: Session = Depends(get_session)):
    return crud.list_pois(db)

@app.get("/pois/nearby", response_model=list[POIRead])
def get_nearby_pois(
    x: int = Query(..., ge=0),
    y: int = Query(..., ge=0),
    max_distance: float = Query(..., gt=0),
    db: Session = Depends(get_session),
):
    pois = services.nearby_pois(db, x, y, max_distance)
    return pois
