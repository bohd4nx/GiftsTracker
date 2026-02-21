from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dto import GiftsDTO
from app.database.models import Gifts
from app.utils import serialize_json, deserialize_json


class GiftsCRUD:
    @staticmethod
    async def get_all(session: AsyncSession) -> list[Gifts]:
        result = await session.execute(select(Gifts))
        return list(result.scalars())

    @staticmethod
    async def save_batch(session: AsyncSession, gifts: list[dict | GiftsDTO]) -> None:
        if not gifts:
            return

        payloads = [gift if isinstance(gift, GiftsDTO) else GiftsDTO.from_dict(gift) for gift in gifts]
        gift_ids = [gift.id for gift in payloads]

        result = await session.execute(select(Gifts).where(Gifts.id.in_(gift_ids)))
        existing_map = {gift.id: gift for gift in result.scalars()}

        for payload in payloads:
            gift = existing_map.get(payload.id)
            if not gift:
                gift = Gifts(id=payload.id)
                session.add(gift)

            for field in Gifts.SYNC_FIELDS:
                setattr(gift, field, getattr(payload, field))

            gift.sticker_raw = serialize_json(payload.sticker_raw)
            gift.raw_data = serialize_json(payload.raw)

        await session.commit()

    @staticmethod
    def gifts_to_dict(gift: Gifts) -> dict:
        data = {
            "_": "Gift",
            "id": gift.id,
            **{field: getattr(gift, field) for field in Gifts.SYNC_FIELDS},
            "sticker_raw": deserialize_json(gift.sticker_raw) if gift.sticker_raw else None,
            "raw": deserialize_json(gift.raw_data)
        }

        return data
