from datetime import datetime

from sqlalchemy import BOOLEAN, BigInteger, DateTime, ForeignKey, Integer, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str]
    username: Mapped[str]
    ai_thread: Mapped[str | None]
    action_count: Mapped[int] = mapped_column(Integer, default=0)
    is_subscribed: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    is_autopayment_enabled: Mapped[bool] = mapped_column(BOOLEAN, default=False, server_default="false")
    is_context_added: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    expired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    space: Mapped[str | None]
    geography: Mapped[str | None]
    request: Mapped[str | None]
    payment_method_id: Mapped[str | None]


class UserCounters(Base):
    __tablename__ = "user_counters"

    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))
    period_started_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    image_count: Mapped[int] = mapped_column(Integer, default=0)
