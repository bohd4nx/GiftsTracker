from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from app.commands.status import handle_status


async def handle_commands(client: Client, message: Message):
    if not message.text:
        return

    command = message.text.lower().strip()

    if command in ['.status', 'status', '/status']:
        await handle_status(client, message)


handle_commands.handlers = [(MessageHandler(handle_commands, filters.text & filters.me), 0)]
