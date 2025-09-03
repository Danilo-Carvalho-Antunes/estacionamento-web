from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.parking_lot import ParkingLot
from app.models.access import Access, AccessStatus


class ParkingLotRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[ParkingLot]:
        return list(self.db.execute(select(ParkingLot)).scalars().all())

    def get(self, lot_id: int) -> Optional[ParkingLot]:
        return self.db.get(ParkingLot, lot_id)

    def create(self, obj: ParkingLot) -> ParkingLot:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, lot: ParkingLot) -> ParkingLot:
        self.db.add(lot)
        self.db.commit()
        self.db.refresh(lot)
        return lot

    def delete(self, lot: ParkingLot) -> None:
        self.db.delete(lot)
        self.db.commit()

    def count_open_accesses(self, lot_id: int) -> int:
        return (
            self.db.execute(
                select(func.count(Access.id)).where(
                    Access.parking_lot_id == lot_id,
                    Access.status == AccessStatus.OPEN,
                )
            ).scalar_one()
        )
