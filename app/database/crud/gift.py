from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Gift
from app.utils import serialize_json, deserialize_json


class GiftCRUD:
    @staticmethod
    async def get_all(session: AsyncSession) -> list[Gift]:
        result = await session.execute(select(Gift))
        return list(result.scalars())

    @staticmethod
    async def get_by_id(session: AsyncSession, gift_id: int) -> Optional[Gift]:
        result = await session.execute(select(Gift).where(Gift.id == gift_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_or_update(session: AsyncSession, gift_data: dict, commit: bool = True) -> Gift:
        existing = await GiftCRUD.get_by_id(session, gift_data["id"])

        if existing:
            GiftCRUD._update_gift_fields(existing, gift_data)
            gift = existing
        else:
            gift = GiftCRUD._create_gift_instance(gift_data)
            session.add(gift)

        if commit:
            await session.commit()
            await session.refresh(gift)
        return gift

    @staticmethod
    async def save_batch(session: AsyncSession, gifts: list[dict]) -> None:
        for gift_data in gifts:
            await GiftCRUD.create_or_update(session, gift_data, commit=False)
        await session.commit()

    @staticmethod
    def _update_gift_fields(gift: Gift, data: dict) -> None:
        gift.price = data.get("price")
        gift.upgrade_price = data.get("upgrade_price")
        gift.total_amount = data.get("total_amount")
        gift.is_limited = data.get("is_limited", False)
        gift.is_sold_out = data.get("is_sold_out", False)
        gift.sticker_file_id = data.get("sticker_file_id")
        gift.sticker_raw = serialize_json(data.get("sticker_raw"))
        gift.sticker_msg_id = data.get("sticker_msg_id")
        gift.msg_id = data.get("msg_id")
        gift.upgrade_msg_id = data.get("upgrade_msg_id")
        gift.raw_data = serialize_json(data.get("raw"))

    @staticmethod
    def _create_gift_instance(data: dict) -> Gift:
        return Gift(
            id=data["id"],
            price=data.get("price"),
            upgrade_price=data.get("upgrade_price"),
            total_amount=data.get("total_amount"),
            is_limited=data.get("is_limited", False),
            is_sold_out=data.get("is_sold_out", False),
            sticker_file_id=data.get("sticker_file_id"),
            sticker_raw=serialize_json(data.get("sticker_raw")),
            sticker_msg_id=data.get("sticker_msg_id"),
            msg_id=data.get("msg_id"),
            upgrade_msg_id=data.get("upgrade_msg_id"),
            raw_data=serialize_json(data.get("raw"))
        )

    @staticmethod
    def gift_to_dict(gift: Gift) -> dict:
        return {
            "_": "Gift",
            "id": gift.id,
            "price": gift.price,
            "upgrade_price": gift.upgrade_price,
            "total_amount": gift.total_amount,
            "is_limited": gift.is_limited,
            "is_sold_out": gift.is_sold_out,
            "sticker_file_id": gift.sticker_file_id,
            "sticker_raw": deserialize_json(gift.sticker_raw) if gift.sticker_raw else None,
            "sticker_msg_id": gift.sticker_msg_id,
            "msg_id": gift.msg_id,
            "upgrade_msg_id": gift.upgrade_msg_id,
            "raw": deserialize_json(gift.raw_data)
        }
