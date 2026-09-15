from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import UUID, String, Numeric, CheckConstraint, ForeignKey, VARCHAR
from sqlalchemy.dialects.postgresql import ENUM

from decimal import Decimal

from schemas.main_shemas import BoilerStatus, FactoryRank


import uuid
import secrets
import string


class Base(DeclarativeBase): pass


class Order(Base):
    __tablename__ = "orders"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status: Mapped[ENUM] = mapped_column(ENUM(BoilerStatus, create_type=False), nullable=False, default=BoilerStatus.IN_QUEUE) #create_type как понимаю это просто чтобы не создавать снова тип в базе данных
    boiler: Mapped[str] = mapped_column(VARCHAR(30), nullable=False, default='no info')
    power: Mapped[Decimal] = mapped_column(Numeric(scale=2, precision=6), CheckConstraint('power >= 0'), nullable=False, default=0.0)
    who_work = mapped_column(UUID(as_uuid=True), ForeignKey("workers.id"))


class Worker(Base):
    __tablename__ = "workers"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    verification_id = mapped_column(VARCHAR(8), unique=True, default="".join((secrets.choice(string.ascii_letters) for _ in range (8))))
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    surname: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    grades: Mapped[str] = mapped_column(ENUM(FactoryRank, create_type=False), nullable=False, default=FactoryRank.RANK_1_2)
    password: Mapped[str] = mapped_column(String(300))