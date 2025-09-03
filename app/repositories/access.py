from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.access import Access, AccessStatus


class AccessRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_open_by_vehicle(self, lot_id: int, vehicle_id: int) -> Optional[Access]:
        stmt = select(Access).where(
            Access.parking_lot_id == lot_id,
            Access.vehicle_id == vehicle_id,
            Access.status == AccessStatus.OPEN,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, access: Access) -> Access:
        self.db.add(access)
        self.db.commit()
        self.db.refresh(access)
        return access

    def close(self, access: Access, end_at: datetime, price) -> Access:
        access.end_at = end_at
        access.price = price
        access.status = AccessStatus.CLOSED
        self.db.add(access)
        self.db.commit()
        self.db.refresh(access)
        return access
