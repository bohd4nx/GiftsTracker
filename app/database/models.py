from datetime import datetime

from sqlalchemy import String, DateTime, func, BigInteger, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Gifts(Base):
    __tablename__ = "gifts"
    SYNC_FIELDS = (
        "price",
        "upgrade_price",
        "total_amount",
        "sticker_file_id",
        "sticker_msg_id",
        "msg_id",
        "upgrade_msg_id",
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    upgrade_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sticker_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sticker_raw: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON as TEXT
    sticker_msg_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    msg_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    upgrade_msg_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    raw_data: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON as TEXT
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), index=True)
