from datetime import datetime

from sqlalchemy import BOOLEAN, BigInteger, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.bot.internal.enums import SpaceType


class Base(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str]
    username: Mapped[str]
    is_subscribed: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    expired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    space_type: Mapped[SpaceType | None]
    area: Mapped[str | None]
    indoor_room: Mapped[str | None]
    budget: Mapped[str | None]
    geography: Mapped[str | None]
    style: Mapped[str | None]
    interests: Mapped[str | None]

    def __str__(self):
        return f"User fullname={self.fullname}, telegram_id={self.tg_id})"

    def __repr__(self):
        return self.__str__()


#
# class UserMessageHistory(Base):
#     __tablename__ = 'user_message_history'
#
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
#     user_tg_id: Mapped[int] = mapped_column(BigInteger)
#     bot_tg_id: Mapped[int | None] = mapped_column(BigInteger)
#     is_from_user: Mapped[bool] = mapped_column(BOOLEAN, default=True)
#     chat_id: Mapped[int] = mapped_column(BigInteger)
#     user_message_text: Mapped[str | None] = mapped_column(String(4096))
#     user_message_type: Mapped[str | None] = mapped_column(String(50))
#     role: Mapped[Role]
