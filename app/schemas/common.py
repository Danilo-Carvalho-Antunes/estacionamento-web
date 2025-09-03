from datetime import datetime, time
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ContractorOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ParkingLotOut(BaseModel):
    id: int
    contractor_id: int
    name: str
    open_at: time
    close_at: time
    capacity: int

    model_config = ConfigDict(from_attributes=True)


class PricingProfileOut(BaseModel):
    id: int
    parking_lot_id: int
    name: str
    fraction_minutes: int
    fraction_rate: Decimal
    hourly_rate: Decimal
    daily_rate: Decimal
    nightly_rate: Decimal

    model_config = ConfigDict(from_attributes=True)


class VehicleOut(BaseModel):
    id: int
    plate: str
    owner_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class EventOut(BaseModel):
    id: int
    parking_lot_id: int
    name: str
    starts_at: datetime
    ends_at: datetime
    price: Decimal

    model_config = ConfigDict(from_attributes=True)


class QuoteResponse(BaseModel):
    lot_id: int
    start_at: datetime
    end_at: datetime
    charged_value: Decimal
    charging_type: str
