from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.core.db import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plate: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    owner_name: Mapped[str | None] = mapped_column(String(255))
    created_at = Column(TIMESTAMP)

    accesses = relationship("Access", back_populates="vehicle")
