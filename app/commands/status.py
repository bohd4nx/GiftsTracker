import time
from datetime import datetime, timezone

from pyrogram import Client
from pyrogram.raw.functions import Ping
from pyrogram.types import Message

from app.core import config
from app.database import SessionLocal
from app.database.crud import GiftsCRUD
from app.utils import format_uptime

STARTED_AT = datetime.now(timezone.utc)


async def handle_status(client: Client, message: Message):
    async with SessionLocal() as session:
        gifts = await GiftsCRUD.get_all(session)
        total_gifts = len(gifts)

    start_time = time.time()
    await client.invoke(Ping(ping_id=0))
    ping_ms = round((time.time() - start_time) * 1000, 2)

    uptime_delta = datetime.now(timezone.utc) - STARTED_AT
    uptime_str = format_uptime(uptime_delta)
    dc_id = getattr(getattr(client, "session", None), "dc_id", "Unknown")

    status_text = (
        '<emoji id="5258503720928288433">ℹ️</emoji> <b>Gifts Tracker Status</b>\n\n'
        f'<emoji id="5260687681733533075">🔃</emoji> <b>Datacenter:</b> '
        f'<a href="https://docs.pyrogram.org/faq/what-are-the-ip-addresses-of-telegram-data-centers">DC{dc_id}</a> [<code>{ping_ms} ms</code>]\n'
        f'<emoji id="5323761960829862762">⚡️</emoji> <b>Uptime:</b> <code>{uptime_str}</code>\n'
        f'<emoji id="5258419835922030550">🕔</emoji> <b>Interval:</b> <code>{config.INTERVAL}s</code>\n'
        f'<emoji id="5257965810634202885">📁</emoji> <b>Total gifts in DB:</b> <code>{total_gifts}</code>'
    )

    await message.edit_text(status_text)
