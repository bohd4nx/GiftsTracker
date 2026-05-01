import logging
from typing import Any

from pyrogram import Client, raw
from pyrogram.file_id import FileId, FileType

logger = logging.getLogger(__name__)


async def fetch_gifts(app: Client, last_hash: int = 0) -> tuple[int, dict[int, dict[str, Any]] | None]:
    """Fetches star gifts from Telegram using last_hash for change detection; returns (hash, gifts_dict) or (hash, None) if unchanged."""
    try:
        result = await app.invoke(raw.functions.payments.GetStarGifts(hash=last_hash))

        # telegram returns StarGiftsNotModified when the list hasn't changed.
        if isinstance(result, raw.types.payments.StarGiftsNotModified):
            logger.debug("No changes in gift list since last check")
            return last_hash, None

        hash_value = result.hash
        gifts_dict = {gift.id: _extract_gift_data(gift) for gift in result.gifts}
        return hash_value, gifts_dict or None
    except Exception:
        logger.exception("Failed to fetch gifts from Telegram API")
        return last_hash, None


def _encode_sticker(sticker: Any, gift_id: int) -> tuple[str | None, dict[str, Any] | None]:
    """Encodes a raw MTProto sticker into a Pyrogram file_id string and a serialisable raw dict."""
    if not sticker:
        return None, None

    dc_id = getattr(sticker, "dc_id", 0)
    media_id = getattr(sticker, "id", 0)
    access_hash = getattr(sticker, "access_hash", 0)
    file_reference = getattr(sticker, "file_reference", b"")

    # all four fields are required to build a valid file_id
    if not all([dc_id, media_id, access_hash, file_reference]):
        return None, None

    # raw dict is stored in DB so the sticker can be re-used without a live session
    sticker_raw = {
        "dc_id": dc_id,
        "id": media_id,
        "access_hash": access_hash,
        "file_reference": file_reference,
    }

    try:
        # encode to a Pyrogram-compatible base64 file_id string
        sticker_file_id = FileId(
            file_type=FileType.DOCUMENT,
            dc_id=dc_id,
            media_id=media_id,
            access_hash=access_hash,
            file_reference=file_reference,
        ).encode()
        return sticker_file_id, sticker_raw
    except Exception as e:
        logger.exception(f"Failed to encode file_id for gift {gift_id}: {e}")
        return None, sticker_raw


def _extract_released_by(gift: Any) -> dict[str, Any] | None:
    """Returns a normalised peer dict for the releasing channel/user, or None."""
    peer = getattr(gift, "released_by", None)
    if not peer:
        return None
    return {
        "_": peer.__class__.__name__,
        "id": getattr(peer, "channel_id", getattr(peer, "user_id", None)),
    }


def _extract_gift_data(gift: Any) -> dict[str, Any]:
    sticker_file_id, sticker_raw = _encode_sticker(getattr(gift, "sticker", None), gift.id)

    return {
        "_": "Gift",
        "id": gift.id,
        "price": gift.stars,
        "upgrade_price": getattr(gift, "upgrade_stars", None),
        "total_amount": getattr(gift, "availability_total", None),
        "sticker_file_id": sticker_file_id,
        "sticker_raw": sticker_raw,
        "sticker_msg_id": None,
        "msg_id": None,
        "upgrade_msg_id": None,
        "raw": {
            "_": "StarGift",
            "title": getattr(gift, "title", None),
            "require_premium": getattr(gift, "require_premium", False),
            "limited_per_user": getattr(gift, "limited_per_user", False),
            "per_user_total": getattr(gift, "per_user_total", None),
            "locked_until_date": getattr(gift, "locked_until_date", None),
            "released_by": _extract_released_by(gift),
            "auction": getattr(gift, "auction", False),
            "auction_slug": getattr(gift, "auction_slug", None),
            "gifts_per_round": getattr(gift, "gifts_per_round", None),
            "upgrade_variants": getattr(gift, "upgrade_variants", None),
            "models_count": None,
        },
    }
