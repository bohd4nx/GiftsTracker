import asyncio
import logging

from pyrogram import Client
from pyrogram.errors import FloodWait

from app.core import config
from app.database import SessionLocal
from app.database.crud import GiftsCRUD
from app.services.gifts import process_gifts

logger = logging.getLogger(__name__)


async def run_gift_monitor(app: Client, bot) -> None:
    cycle_count = 0

    while True:
        try:
            cycle_count += 1
            logger.info(f"Starting gift check cycle #{cycle_count}")

            async with SessionLocal() as session:
                gifts = await GiftsCRUD.get_all(session)
                gifts_history = {gift.id: GiftsCRUD.gifts_to_dict(gift) for gift in gifts}

                if await process_gifts(app, bot, gifts_history):
                    await GiftsCRUD.save_batch(session, list(gifts_history.values()))

            await asyncio.sleep(config.INTERVAL)
        except FloodWait as e:
            logger.warning(f"Flood wait triggered, sleeping for {e.value}s")
            await asyncio.sleep(e.value)
        except Exception:
            logger.exception("Unexpected error in gift monitor loop")
            await asyncio.sleep(config.INTERVAL)
