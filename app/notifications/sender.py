import asyncio
import logging

from pyrogram.errors import FloodWait, WebpageNotFound

from app.core import config
from app.utils import get_released_peer, create_link_preview
from app.notifications.messages import create_message_text

logger = logging.getLogger(__name__)


async def _send_or_edit(app, text: str, link_preview, message_id: int | None = None) -> int:
    if message_id:
        await app.edit_message_text(
            chat_id=config.CHANNEL_ID,
            message_id=message_id,
            text=text,
            link_preview_options=link_preview
        )
        return message_id

    message = await app.send_message(
        chat_id=config.CHANNEL_ID,
        text=text,
        link_preview_options=link_preview
    )
    return message.id


async def send_notification(
        app,
        bot,
        gift_data: dict,
        sticker_message_id: int,
        is_upgrade: bool = False
) -> int | None:
    try:
        username = await get_released_peer(app, gift_data)
        link_preview = create_link_preview(gift_data, sticker_message_id)
        text = create_message_text(gift_data, username, is_upgrade)

        try:
            msg_id = await _send_or_edit(app, text, link_preview)
        except WebpageNotFound:
            logger.warning(f"Preview unavailable for gift {gift_data['id']}, sending without preview")
            msg_id = await _send_or_edit(app, text, None)

        return msg_id
    except FloodWait as e:
        logger.warning(f"Flood wait triggered, sleeping for {e.value}s on gift {gift_data['id']}")
        await asyncio.sleep(e.value)
        return await send_notification(app, bot, gift_data, sticker_message_id, is_upgrade)
    except Exception as e:
        logger.exception(f"Failed to send notification for gift {gift_data['id']}: {e}")
        return None


async def edit_notification(
        app,
        bot,
        message_id: int,
        gift_data: dict,
        sticker_message_id: int,
        is_upgrade: bool = False
) -> bool:
    try:
        username = await get_released_peer(app, gift_data)
        link_preview = create_link_preview(gift_data, sticker_message_id)
        text = create_message_text(gift_data, username, is_upgrade)

        try:
            await _send_or_edit(app, text, link_preview, message_id)
        except WebpageNotFound:
            logger.warning(f"Preview unavailable for gift {gift_data['id']}, editing without preview")
            await _send_or_edit(app, text, None, message_id)

        return True
    except FloodWait as e:
        logger.warning(f"Flood wait triggered, sleeping for {e.value}s while editing gift {gift_data['id']}")
        await asyncio.sleep(e.value)
        return await edit_notification(app, bot, message_id, gift_data, sticker_message_id, is_upgrade)
    except Exception as e:
        if "MESSAGE_NOT_MODIFIED" not in str(e):
            logger.exception(f"Failed to edit notification for gift {gift_data['id']}: {e}")
        return False
