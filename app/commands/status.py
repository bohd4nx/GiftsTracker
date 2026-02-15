import time
from datetime import datetime, timezone

from pyrogram import Client
from pyrogram.raw.functions import Ping
from pyrogram.types import Message

from app.core import config
from app.database import SessionLocal
from app.database.crud import GiftCRUD

STARTED_AT = datetime.now(timezone.utc)


async def handle_status(client: Client, message: Message):
    async with SessionLocal() as session:
        gifts = await GiftCRUD.get_all(session)
        total_gifts = len(gifts)

    start_time = time.time()
    await client.invoke(Ping(ping_id=0))
    ping_ms = round((time.time() - start_time) * 1000, 2)

    uptime_delta = datetime.now(timezone.utc) - STARTED_AT
    uptime_str = str(uptime_delta).split(".")[0]
    dc_id = getattr(getattr(client, "session", None), "dc_id", "Unknown")

    status_text = (
        "<b>📊 Gifts Tracker Status</b>\n\n"
        f"<b>🌐 Datacenter:</b> <a href=\"https://docs.pyrogram.org/faq/what-are-the-ip-addresses-of-telegram-data-centers\">DC{dc_id}</a>\n"
        f"<b>⚡️ Latency:</b> <code>{ping_ms} ms</code>\n\n"
        f"<b>⏱️ Uptime:</b> <code>{uptime_str}</code>\n"
        f"<b>⏰ Interval:</b> <code>{config.INTERVAL}s</code>\n"
        f"<b>🎁 Total gifts in DB:</b> <code>{total_gifts}</code>"
    )

    await message.edit_text(status_text)
