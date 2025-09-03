from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import DATETIME as MySQLDateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parking_lot_id: Mapped[int] = mapped_column(ForeignKey("parking_lots.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(MySQLDateTime(fsp=6), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(MySQLDateTime(fsp=6), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    created_at = Column(TIMESTAMP)

    parking_lot = relationship("ParkingLot", back_populates="events")
