import asyncio
import logging

from pyrogram import Client
from pyrogram.errors import FloodWait

from app.core import config
from app.services.gift_processor import process_gifts
from app.utils.history import load_history, save_history

logger = logging.getLogger(__name__)


async def run_gift_monitor(app: Client, bot) -> None:
    cycle_count = 0

    while True:
        try:
            cycle_count += 1
            logger.info(f"Starting gift check cycle #{cycle_count}")

            history = await load_history()
            gifts_history = {gift["id"]: gift for gift in history}

            if await process_gifts(app, bot, gifts_history):
                await save_history(list(gifts_history.values()))

            await asyncio.sleep(config.INTERVAL)
        except FloodWait as e:
            logger.warning(f"Flood wait triggered, sleeping for {e.value}s")
            await asyncio.sleep(e.value)
        except Exception:
            logger.exception("Unexpected error in gift monitor loop")
            await asyncio.sleep(config.INTERVAL)
