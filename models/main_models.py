from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import UUID, Column, String, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM

from decimal import Decimal

from shemas.main_shemas import BoilerStatus


import uuid


class Base(DeclarativeBase):
    pass


class Order():
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status: Mapped[ENUM] = mapped_column(ENUM(BoilerStatus, create_type=False), nullable=False, default=BoilerStatus.IN_QUEUE)
    boiler: Mapped[str] = mapped_column(String(30), nullable=False, default='no info')
    power: Mapped[Decimal] = mapped_column(Numeric(scale=2, precision=6), CheckConstraint('power >= 0'), nullable=False, default=0.0)