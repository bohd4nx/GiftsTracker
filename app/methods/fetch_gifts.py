import logging
from typing import Any

from pyrogram import Client, raw
from pyrogram.file_id import FileId, FileType

logger = logging.getLogger(__name__)


async def fetch_gifts(app: Client) -> tuple[int, dict[int, dict]]:
    try:
        star_gifts = await app.invoke(raw.functions.payments.GetStarGifts(hash=0))
        logger.debug(f"Full GetStarGifts response: {star_gifts}")
        hash_value = getattr(star_gifts, 'hash', 0)

        gifts_dict = {
            gift.id: _extract_gift_data(gift)
            for gift in star_gifts.gifts  # type: ignore[arg-type]
        }

        if gifts_dict:
            # logger.info(f"Successfully fetched {len(gifts_dict)} gifts")
            return hash_value, gifts_dict

        return 0, {}
    except Exception:
        logger.exception("Failed to fetch gifts from Telegram API")
        return 0, {}


def _encode_sticker(sticker, gift_id: int) -> tuple[str | None, dict | None]:
    if not sticker:
        return None, None

    dc_id = getattr(sticker, 'dc_id', 0)
    media_id = getattr(sticker, 'id', 0)
    access_hash = getattr(sticker, 'access_hash', 0)
    file_reference = getattr(sticker, 'file_reference', b'')

    if not all([dc_id, media_id, access_hash, file_reference]):
        return None, None

    sticker_raw = {
        "dc_id": dc_id,
        "id": media_id,
        "access_hash": access_hash,
        "file_reference": file_reference
    }

    try:
        sticker_file_id = FileId(
            file_type=FileType.DOCUMENT,
            dc_id=dc_id,
            media_id=media_id,
            access_hash=access_hash,
            file_reference=file_reference
        ).encode()
        return sticker_file_id, sticker_raw
    except Exception as e:
        logger.exception(f"Failed to encode file_id for gift {gift_id}: {e}")
        return None, sticker_raw


def _extract_gift_data(gift) -> dict[str, Any]:
    return {
        "_": "Gift",
        "id": gift.id,
        "price": gift.stars,
        "upgrade_price": getattr(gift, 'upgrade_stars', None),
        "total_amount": getattr(gift, 'availability_total', None),
        "sticker_file_id": (sticker_data := _encode_sticker(getattr(gift, 'sticker', None), gift.id))[0],
        "sticker_raw": sticker_data[1],
        "sticker_msg_id": None,
        "msg_id": None,
        "upgrade_msg_id": None,
        "raw": {
            "_": "StarGift",
            "require_premium": getattr(gift, 'require_premium', False),
            "limited_per_user": getattr(gift, 'limited_per_user', False),
            "per_user_total": getattr(gift, 'per_user_total', None),
            "locked_until_date": getattr(gift, 'locked_until_date', None),
            "released_by": (
                {
                    "_": rb.__class__.__name__,
                    "id": getattr(rb, "channel_id", getattr(rb, "user_id", None))
                }
                if (rb := getattr(gift, "released_by", None))
                else None
            ),
            "auction": getattr(gift, 'auction', False),
            "auction_slug": getattr(gift, 'auction_slug', None),
            "gifts_per_round": getattr(gift, 'gifts_per_round', None)
        }
    }
