import asyncio
import logging

from pyrogram import Client

from app.methods import fetch_gifts, upload_sticker
from app.notifications import send_notification
from app.services.changes import (
    preserve_message_ids,
    check_gift_changes
)

logger = logging.getLogger(__name__)


async def process_gifts(app: Client, bot, gifts_history: dict[int, dict]) -> bool:
    _, current_gifts = await fetch_gifts(app)
    if not current_gifts:
        return False

    has_changes = False
    new_gifts = {k: v for k, v in current_gifts.items() if k not in gifts_history}

    if new_gifts:
        logger.info(f"Found {len(new_gifts)} new gifts to process")
        await _process_new_gifts(app, bot, new_gifts, gifts_history)
        has_changes = True

    for gift_id, current_gift in current_gifts.items():
        if gift_id in new_gifts or gift_id not in gifts_history:
            continue

        old_gift = gifts_history[gift_id]
        preserve_message_ids(old_gift, current_gift)

        if await check_gift_changes(app, bot, old_gift, current_gift):
            has_changes = True

        gifts_history[gift_id] = current_gift

    return has_changes


async def _process_new_gifts(app: Client, bot, new_gifts: dict[int, dict], gifts_history: dict[int, dict]) -> None:
    new_gifts_list = list(new_gifts.values())

    for idx, gift in enumerate(new_gifts_list, 1):
        logger.info(f"Processing gift {idx}/{len(new_gifts_list)}: {gift['id']}")

        try:
            sticker_msg_id = await upload_sticker(app, bot, gift)
            if not sticker_msg_id:
                raise Exception(f"Failed to upload sticker for gift {gift['id']}")

            msg_id = await send_notification(app, gift, sticker_msg_id, is_upgrade=False)
            gift.update({"sticker_msg_id": sticker_msg_id, "msg_id": msg_id, "upgrade_msg_id": None})
            logger.info(f"Successfully processed gift {gift['id']}")
        except Exception as e:
            logger.error(f"Failed to process gift {gift['id']}: {e}")
            gift.update({"sticker_msg_id": None, "msg_id": None, "upgrade_msg_id": None})

        gifts_history[gift["id"]] = gift

        if idx < len(new_gifts_list):
            await asyncio.sleep(1)
