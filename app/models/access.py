from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, TIMESTAMP, DECIMAL, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.mysql import DATETIME as MySQLDateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class AccessStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class Access(Base):
    __tablename__ = "accesses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=False)
    parking_lot_id: Mapped[int] = mapped_column(ForeignKey("parking_lots.id"), nullable=False)
    start_at: Mapped[datetime] = mapped_column(MySQLDateTime(fsp=6), nullable=False)
    end_at: Mapped[datetime | None] = mapped_column(MySQLDateTime(fsp=6))
    price = Column(DECIMAL(10, 2))
    status: Mapped[AccessStatus] = mapped_column(SAEnum(AccessStatus), default=AccessStatus.OPEN, nullable=False)
    created_at = Column(TIMESTAMP)

    vehicle = relationship("Vehicle", back_populates="accesses")
    parking_lot = relationship("ParkingLot", back_populates="accesses")
