from datetime import datetime

from sqlalchemy import BOOLEAN, BigInteger, DateTime, func
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
    ai_tread: Mapped[str | None]
    is_subscribed: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    is_intro_shown: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    expired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    space: Mapped[str | None]
    budget: Mapped[str | None]
    geography: Mapped[str | None]
    style: Mapped[str | None]

    def __str__(self):
        return f"User fullname={self.fullname}, telegram_id={self.tg_id})"

    def __repr__(self):
        return self.__str__()
