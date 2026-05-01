from typing import Any

from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dto import GiftsDTO
from app.database.models import Gifts
from app.utils import deserialize_json, serialize_json


class GiftsCRUD:
    # columns synced on every upsert; JSON blobs are handled separately.
    SYNC_FIELDS = (
        "price",
        "upgrade_price",
        "total_amount",
        "sticker_file_id",
        "sticker_msg_id",
        "msg_id",
        "upgrade_msg_id",
        "emoji_id",
    )

    @staticmethod
    async def get_all(session: AsyncSession) -> list[Gifts]:
        result = await session.execute(select(Gifts))
        return list(result.scalars())

    @staticmethod
    async def count(session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(Gifts))
        return result.scalar_one()

    @staticmethod
    async def get_by_msg_id(session: AsyncSession, msg_id: int) -> tuple[Gifts | None, bool]:
        """Looks up a gift by msg_id (regular) or upgrade_msg_id; returns (row, is_upgrade)."""
        result = await session.execute(select(Gifts).where(Gifts.msg_id == msg_id))
        row = result.scalar_one_or_none()
        if row:
            return row, False

        result = await session.execute(select(Gifts).where(Gifts.upgrade_msg_id == msg_id))
        row = result.scalar_one_or_none()
        return row, True

    @staticmethod
    async def update_emoji_id(session: AsyncSession, gift_id: int, emoji_id: int) -> None:
        """Updates emoji_id for a single gift row by primary key."""
        result = await session.execute(select(Gifts).where(Gifts.id == gift_id))
        row = result.scalar_one_or_none()
        if row is not None:
            row.emoji_id = emoji_id
            await session.commit()

    @staticmethod
    async def save_batch(session: AsyncSession, gifts: list[dict[str, Any] | GiftsDTO]) -> None:
        """Upserts a batch of gifts via a single INSERT … ON CONFLICT query; never overwrites first_seen."""
        if not gifts:
            return

        # normalise to DTO so we always have a consistent attribute interface
        payloads = [gift if isinstance(gift, GiftsDTO) else GiftsDTO.from_dict(gift) for gift in gifts]

        # serialise JSON blobs to TEXT; scalar fields are passed as-is
        rows = [
            {
                "id": p.id,
                **{field: getattr(p, field) for field in GiftsCRUD.SYNC_FIELDS},
                "sticker_raw": serialize_json(p.sticker_raw),
                "raw_data": serialize_json(p.raw),
            }
            for p in payloads
        ]

        # single INSERT ... ON CONFLICT upsert for the whole batch
        stmt = insert(Gifts).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={col: stmt.excluded[col] for col in GiftsCRUD.SYNC_FIELDS}
            | {
                "sticker_raw": stmt.excluded.sticker_raw,
                "raw_data": stmt.excluded.raw_data,
                "last_updated": func.now(),
            },
        )
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    def gifts_to_dict(gift: Gifts) -> dict[str, Any]:
        """Converts an ORM row to the in-memory gift dict used by services."""
        data = {
            "_": "Gift",
            "id": gift.id,
            **{field: getattr(gift, field) for field in GiftsCRUD.SYNC_FIELDS},
            "sticker_raw": (deserialize_json(gift.sticker_raw) if gift.sticker_raw else None),
            "raw": deserialize_json(gift.raw_data),
        }

        return data
