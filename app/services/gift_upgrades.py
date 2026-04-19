import logging
from typing import Any

from pyrogram import Client

from app.notifications import edit_notification, send_notification

logger = logging.getLogger(__name__)


async def notify_upgrade_available(app: Client, gift_data: dict[str, Any]) -> None:
    if not (sticker_msg_id := gift_data.get("sticker_msg_id")):
        return

    try:
        msg_id = await send_notification(app, gift_data, sticker_msg_id, is_upgrade=True)
        gift_data["upgrade_msg_id"] = msg_id
        logger.info(f"Successfully sent upgrade notification for gift {gift_data['id']}, message_id={msg_id}")
    except Exception:
        logger.exception(f"Failed to send upgrade notification for gift {gift_data['id']}")


async def notify_upgrade_changed(app: Client, new_gift: dict[str, Any], old_gift: dict[str, Any]) -> None:
    sticker_msg_id = new_gift.get("sticker_msg_id")
    upgrade_msg_id = old_gift.get("upgrade_msg_id")

    if not sticker_msg_id or not upgrade_msg_id:
        return

    try:
        await edit_notification(app, upgrade_msg_id, new_gift, sticker_msg_id, is_upgrade=True)
        logger.info(f"Successfully edited upgrade notification for gift {new_gift['id']}")
    except Exception:
        logger.exception(f"Failed to edit upgrade notification for gift {new_gift['id']}")
