import logging

from pyrogram.types import LinkPreviewOptions

from app.core import config

logger = logging.getLogger(__name__)


def format_number(number: int) -> str:
    if number >= 1000:
        return "{:,}".format(number).replace(",", ".")
    return str(number)


async def create_link_preview(app, gift_data: dict, sticker_message_id: int) -> LinkPreviewOptions | None:
    raw_data = gift_data.get('raw', {})
    auction_slug = raw_data.get('auction_slug')

    # Если есть auction_slug и auction, показываем превью аукциона
    if auction_slug and raw_data.get('auction'):
        return LinkPreviewOptions(
            url=f"https://t.me/auction/{auction_slug}",
            prefer_small_media=True,
            show_above_text=True
        )

    if not sticker_message_id:
        return None

    return LinkPreviewOptions(
        url=f"https://t.me/{config.STICKERS_CHANNEL_USERNAME}/{sticker_message_id}",
        prefer_small_media=True,
        show_above_text=True
    )


async def get_released_peer(app, gift_data: dict) -> str | None:
    try:
        raw_data = gift_data.get('raw', {})
        released_by = raw_data.get('released_by', {})
        peer_id = released_by.get('id')

        if not peer_id:
            return None

        try:
            chat_id = int(f"-100{peer_id}")
            chat = await app.get_chat(chat_id)
            return chat.username
        except Exception:
            return None

    except Exception:
        return None
