from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session

from app.models.event import Event


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_overlapping(self, lot_id: int, start_at: datetime, end_at: datetime) -> Optional[Event]:
        # Overlap if NOT (ends_at < start_at OR starts_at > end_at)
        stmt = select(Event).where(
            and_(
                Event.parking_lot_id == lot_id,
                or_(Event.ends_at >= start_at, Event.starts_at <= end_at),
                ~or_(Event.ends_at < start_at, Event.starts_at > end_at),
            )
        ).limit(1)
        return self.db.execute(stmt).scalar_one_or_none()
