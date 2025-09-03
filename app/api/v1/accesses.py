from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.access import Access
from app.models.vehicle import Vehicle
from app.repositories.access import AccessRepository
from app.repositories.parking_lot import ParkingLotRepository
from app.repositories.vehicle import VehicleRepository
from app.schemas.access import (
    AccessEnterRequest,
    AccessExitRequest,
    AccessOut,
    AccessClosedResponse,
)
from app.services.pricing import calculate_price

router = APIRouter(prefix="/v1/lots/{lot_id}/accesses", tags=["accesses"])


def _is_within_hours(open_at, close_at, instant: datetime) -> bool:
    t = instant.time()
    return open_at <= t <= close_at


@router.post("/enter", response_model=AccessOut, status_code=201)
def enter(lot_id: int, payload: AccessEnterRequest, db: Session = Depends(get_db)):
    lot_repo = ParkingLotRepository(db)
    veh_repo = VehicleRepository(db)
    acc_repo = AccessRepository(db)

    lot = lot_repo.get(lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    start_at = payload.start_at or datetime.utcnow()
    if not _is_within_hours(lot.open_at, lot.close_at, start_at):
        raise HTTPException(status_code=400, detail="Outside operating hours")

    # Capacity check
    open_count = lot_repo.count_open_accesses(lot_id)
    if open_count >= lot.capacity:
        raise HTTPException(status_code=409, detail="Parking lot is full")

    # Vehicle lookup or create
    vehicle = veh_repo.get_by_plate(payload.plate)
    if not vehicle:
        vehicle = Vehicle(plate=payload.plate)
        vehicle = veh_repo.create(vehicle)

    # Prevent duplicate open access
    existing = acc_repo.find_open_by_vehicle(lot_id, vehicle.id)
    if existing:
        raise HTTPException(status_code=409, detail="Vehicle already inside")

    access = Access(vehicle_id=vehicle.id, parking_lot_id=lot_id, start_at=start_at)
    access = acc_repo.create(access)
    return access


@router.post("/exit", response_model=AccessClosedResponse)
def exit_(lot_id: int, payload: AccessExitRequest, db: Session = Depends(get_db)):
    lot_repo = ParkingLotRepository(db)
    veh_repo = VehicleRepository(db)
    acc_repo = AccessRepository(db)

    lot = lot_repo.get(lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    vehicle = veh_repo.get_by_plate(payload.plate)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    access = acc_repo.find_open_by_vehicle(lot_id, vehicle.id)
    if not access:
        raise HTTPException(status_code=404, detail="No open access for this vehicle")

    end_at = payload.end_at or datetime.utcnow()
    result = calculate_price(db, lot_id=lot_id, start_at=access.start_at, end_at=end_at)
    access = acc_repo.close(access, end_at=end_at, price=result.charged_value)

    return AccessClosedResponse(
        id=access.id,
        charged_value=result.charged_value,
        charging_type=result.charging_type,
    )
