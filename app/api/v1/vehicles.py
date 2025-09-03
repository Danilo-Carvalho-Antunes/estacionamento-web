from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.vehicle import VehicleRepository
from app.schemas.common import VehicleOut

router = APIRouter(prefix="/v1/vehicles", tags=["vehicles"])


@router.get("/", response_model=list[VehicleOut])
def list_vehicles(db: Session = Depends(get_db)):
    repo = VehicleRepository(db)
    return repo.list()


@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    repo = VehicleRepository(db)
    v = repo.get(vehicle_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return v
