from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class PricingProfile(Base):
    __tablename__ = "pricing_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parking_lot_id: Mapped[int] = mapped_column(ForeignKey("parking_lots.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    fraction_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=15)
    fraction_rate = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    daily_rate = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    nightly_rate = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    created_at = Column(TIMESTAMP)

    parking_lot = relationship("ParkingLot", back_populates="pricing_profiles")
