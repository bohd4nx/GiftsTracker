import asyncio
import logging

from pyrogram import Client
from pyrogram.errors import FloodWait

from app.core import config
from app.methods import fetch_gifts, upload_sticker
from app.notifications import send_notification, notify_upgrade_available, notify_upgrade_changed
from app.utils.history import (
    load_history,
    save_history,
    preserve_message_ids,
    detect_upgrade_availability,
    detect_upgrade_price_change
)

logger = logging.getLogger(__name__)


async def run_gift_monitor(app: Client, bot) -> None:
    cycle_count = 0

    while True:
        try:
            cycle_count += 1
            logger.info(f"Starting gift check cycle #{cycle_count}")

            history = await load_history()
            gifts_history = {gift["id"]: gift for gift in history}

            if await _process_gifts(app, bot, gifts_history):
                await save_history(list(gifts_history.values()))

            await asyncio.sleep(config.INTERVAL)
        except FloodWait as e:
            logger.warning(f"Flood wait triggered, sleeping for {e.value}s")
            await asyncio.sleep(e.value)
        except Exception:
            logger.exception("Unexpected error in gift monitor loop")
            await asyncio.sleep(config.INTERVAL)


async def _process_gifts(app: Client, bot, gifts_history: dict[int, dict]) -> bool:
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

        if await _check_gift_changes(app, bot, old_gift, current_gift):
            has_changes = True

        gifts_history[gift_id] = current_gift

    return has_changes


async def _process_new_gifts(app: Client, bot, new_gifts: dict[int, dict], gifts_history: dict[int, dict]) -> None:
    new_gifts_list = list(new_gifts.values())

    for idx, gift in enumerate(new_gifts_list, 1):
        logger.info(f"Processing gift {idx}/{len(new_gifts_list)}: {gift['id']}")

        try:
            await _process_single_gift(app, bot, gift)
            logger.info(f"Successfully processed gift {gift['id']}")
        except Exception as e:
            logger.error(f"Failed to process gift {gift['id']}: {e}")
            gift.update({"sticker_msg_id": None, "msg_id": None, "upgrade_msg_id": None})

        gifts_history[gift["id"]] = gift

        if idx < len(new_gifts_list):
            await asyncio.sleep(1)


async def _process_single_gift(app: Client, bot, gift_data: dict) -> None:
    sticker_msg_id = await upload_sticker(app, bot, gift_data)
    if not sticker_msg_id:
        raise Exception(f"Failed to upload sticker for gift {gift_data['id']}")

    msg_id = await send_notification(app, bot, gift_data, sticker_msg_id, is_upgrade=False)
    gift_data.update({"sticker_msg_id": sticker_msg_id, "msg_id": msg_id, "upgrade_msg_id": None})


async def _check_gift_changes(app: Client, bot, old_gift: dict, new_gift: dict) -> bool:
    if detect_upgrade_availability(old_gift, new_gift):
        await notify_upgrade_available(app, bot, new_gift)
        return True

    if detect_upgrade_price_change(old_gift, new_gift):
        await notify_upgrade_changed(app, bot, new_gift, old_gift)
        return True

    return False
