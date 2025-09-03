from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pricing_profile import PricingProfile


class PricingProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_for_lot(self, lot_id: int) -> Optional[PricingProfile]:
        # For now, return the first profile found for the lot
        return self.db.execute(
            select(PricingProfile).where(PricingProfile.parking_lot_id == lot_id).order_by(PricingProfile.id.asc())
        ).scalar_one_or_none()
