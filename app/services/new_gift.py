import asyncio
import logging
from typing import Any

from aiogram import Bot
from pyrogram import Client

from app.methods import fetch_gifts, upload_sticker
from app.notifications import send_notification

from .emoji_pack import add_gift_to_pack
from .gift_changes import check_gift_changes, preserve_message_ids

logger = logging.getLogger(__name__)


async def process_gifts(
    app: Client, bot: Bot, gifts_history: dict[int, dict[str, Any]], last_hash: int = 0
) -> tuple[bool, int]:
    """Diffs Telegram gift list against history; processes new gifts and checks existing ones for changes."""
    # fetch current gift list; None means Telegram reported no changes
    new_hash, current_gifts = await fetch_gifts(app, last_hash)
    if current_gifts is None:
        return False, new_hash

    has_changes = False
    # gifts absent from history are brand new
    new_gifts = {k: v for k, v in current_gifts.items() if k not in gifts_history}

    if new_gifts:
        logger.info(f"Found {len(new_gifts)} new gifts to process")
        await _process_new_gifts(app, bot, new_gifts, gifts_history)
        has_changes = True

    # check existing gifts for upgrade / price / craft changes
    for gift_id, current_gift in current_gifts.items():
        if gift_id in new_gifts or gift_id not in gifts_history:
            continue

        old_gift = gifts_history[gift_id]
        # copy stored msg_id / emoji_id into the fresh snapshot before diffing
        preserve_message_ids(old_gift, current_gift)

        if await check_gift_changes(app, bot, old_gift, current_gift):
            has_changes = True

        gifts_history[gift_id] = current_gift

    return has_changes, new_hash


async def _process_new_gifts(
    app: Client, bot: Bot, new_gifts: dict[int, dict[str, Any]], gifts_history: dict[int, dict[str, Any]]
) -> None:
    """Uploads sticker, adds to emoji pack, and sends notification for each new gift."""
    new_gifts_list = list(new_gifts.values())

    for idx, gift in enumerate(new_gifts_list, 1):
        logger.info(f"Processing gift {idx}/{len(new_gifts_list)}: {gift['id']}")

        try:
            # upload the sticker and add it to the emoji pack concurrently
            sticker_msg_id, emoji_id = await asyncio.gather(
                upload_sticker(app, bot, gift),
                add_gift_to_pack(app, gift),
            )
            if not sticker_msg_id:
                raise Exception(f"Failed to upload sticker for gift {gift['id']}")

            # wait for Telegram to index the sticker post before referencing it
            # in the link preview, otherwise WebpageNotFound is raised.
            await asyncio.sleep(3)

            msg_id = await send_notification(app, gift, sticker_msg_id, is_upgrade=False)
            gift.update(
                {
                    "sticker_msg_id": sticker_msg_id,
                    "msg_id": msg_id,
                    "upgrade_msg_id": None,
                    "emoji_id": emoji_id,
                }
            )
            logger.info(f"Successfully processed gift {gift['id']}")
        except Exception as e:
            logger.error(f"Failed to process gift {gift['id']}: {e}")
            gift.update(
                {
                    "sticker_msg_id": None,
                    "msg_id": None,
                    "upgrade_msg_id": None,
                    "emoji_id": None,
                }
            )

        gifts_history[gift["id"]] = gift

        if idx < len(new_gifts_list):
            await asyncio.sleep(1)
