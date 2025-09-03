from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repositories.parking_lot import ParkingLotRepository
from app.repositories.pricing_profile import PricingProfileRepository
from app.schemas.common import ParkingLotOut, PricingProfileOut, QuoteResponse
from app.services.pricing import calculate_price

router = APIRouter(prefix="/v1/lots", tags=["lots"])


@router.get("/", response_model=list[ParkingLotOut])
def list_lots(db: Session = Depends(get_db)):
    repo = ParkingLotRepository(db)
    return repo.list()


@router.get("/{lot_id}", response_model=ParkingLotOut)
def get_lot(lot_id: int, db: Session = Depends(get_db)):
    repo = ParkingLotRepository(db)
    lot = repo.get(lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    return lot


@router.get("/{lot_id}/pricing", response_model=PricingProfileOut)
def get_lot_pricing(lot_id: int, db: Session = Depends(get_db)):
    repo = PricingProfileRepository(db)
    prof = repo.get_for_lot(lot_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Pricing profile not found for lot")
    return prof


@router.get("/{lot_id}/quote", response_model=QuoteResponse)
def quote(
    lot_id: int,
    start_at: datetime = Query(..., description="ISO8601 start datetime (UTC recommended)"),
    end_at: datetime = Query(..., description="ISO8601 end datetime (UTC recommended)"),
    plate: str | None = Query(None, description="Optional vehicle plate"),
    db: Session = Depends(get_db),
):
    result = calculate_price(db, lot_id=lot_id, start_at=start_at, end_at=end_at)
    return QuoteResponse(
        lot_id=lot_id,
        start_at=start_at,
        end_at=end_at,
        charged_value=result.charged_value,
        charging_type=result.charging_type,
    )
