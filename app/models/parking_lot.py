from datetime import time

from sqlalchemy import Column, Integer, String, TIMESTAMP, Time, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class ParkingLot(Base):
    __tablename__ = "parking_lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contractor_id: Mapped[int] = mapped_column(ForeignKey("contractors.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    open_at: Mapped[time] = mapped_column(Time, nullable=False)
    close_at: Mapped[time] = mapped_column(Time, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP)

    contractor = relationship("Contractor", back_populates="parking_lots")
    pricing_profiles = relationship("PricingProfile", back_populates="parking_lot", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="parking_lot", cascade="all, delete-orphan")
    accesses = relationship("Access", back_populates="parking_lot")
