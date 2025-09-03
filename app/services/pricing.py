from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.parking_lot import ParkingLot
from app.repositories.parking_lot import ParkingLotRepository
from app.repositories.pricing_profile import PricingProfileRepository
from app.repositories.event import EventRepository


@dataclass
class PriceResult:
    charged_value: Decimal
    charging_type: str


def _within_open_hours(open_at: time, close_at: time, start_at: datetime, end_at: datetime) -> bool:
    # Simple same-day window check; for cross-day windows use open@00:00/close@23:59:59
    s_t = start_at.time()
    e_t = end_at.time()
    return (open_at <= s_t <= close_at) and (open_at <= e_t <= close_at)


def calculate_price(db: Session, lot_id: int, start_at: datetime, end_at: datetime) -> PriceResult:
    if end_at <= start_at:
        raise HTTPException(status_code=400, detail="end_at must be after start_at")

    lot_repo = ParkingLotRepository(db)
    prof_repo = PricingProfileRepository(db)
    evt_repo = EventRepository(db)

    lot: ParkingLot | None = lot_repo.get(lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    # Validate within open window
    if not _within_open_hours(lot.open_at, lot.close_at, start_at, end_at):
        raise HTTPException(status_code=400, detail="Requested time outside lot operating hours")

    # Event overrides
    evt = evt_repo.find_overlapping(lot_id, start_at, end_at)
    if evt:
        return PriceResult(charged_value=Decimal(evt.price), charging_type="event")

    prof = prof_repo.get_for_lot(lot_id)
    if not prof:
        raise HTTPException(status_code=400, detail="No pricing profile configured for lot")

    # Nightly rule: if entry at or after 18:00 or before 06:00 -> nightly rate
    if start_at.time() >= time(18, 0) or start_at.time() < time(6, 0):
        return PriceResult(charged_value=Decimal(prof.nightly_rate), charging_type="nightly")

    # Duration in minutes
    total_minutes = int((end_at - start_at).total_seconds() // 60)

    # Daily if > 9h (540min)
    if total_minutes > 9 * 60:
        return PriceResult(charged_value=Decimal(prof.daily_rate), charging_type="daily")

    # Hourly if >= 1h
    if total_minutes >= 60:
        hours = (total_minutes + 59) // 60  # ceil hours
        return PriceResult(charged_value=Decimal(prof.hourly_rate) * hours, charging_type="hourly")

    # Fractional (<1h)
    frac = prof.fraction_minutes or 15
    intervals = (total_minutes + frac - 1) // frac
    if intervals == 0:
        intervals = 1
    return PriceResult(charged_value=Decimal(prof.fraction_rate) * intervals, charging_type="fraction")
