from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle


class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Vehicle]:
        return list(self.db.execute(select(Vehicle)).scalars().all())

    def get(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.db.get(Vehicle, vehicle_id)

    def get_by_plate(self, plate: str) -> Optional[Vehicle]:
        return self.db.execute(select(Vehicle).where(Vehicle.plate == plate)).scalar_one_or_none()

    def create(self, obj: Vehicle) -> Vehicle:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, vehicle: Vehicle) -> Vehicle:
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self.db.delete(vehicle)
        self.db.commit()
