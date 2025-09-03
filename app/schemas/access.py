from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AccessEnterRequest(BaseModel):
    plate: str
    start_at: Optional[datetime] = None


class AccessExitRequest(BaseModel):
    plate: str
    end_at: Optional[datetime] = None


class AccessOut(BaseModel):
    id: int
    vehicle_id: int
    parking_lot_id: int
    start_at: datetime
    end_at: Optional[datetime] = None
    price: Optional[Decimal] = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class AccessClosedResponse(BaseModel):
    id: int
    charged_value: Decimal
    charging_type: str
