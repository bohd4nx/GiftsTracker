import logging
from io import BytesIO

from aiogram.types import BufferedInputFile

from app.core import config

logger = logging.getLogger(__name__)


async def upload_sticker(app, bot, gift_data: dict) -> int | None:
    sticker_file_id = gift_data.get("sticker_file_id")
    if not sticker_file_id:
        logger.error(f"Missing sticker_file_id for gift {gift_data['id']}")
        return None

    try:
        sticker_bytes: BytesIO = await app.download_media(sticker_file_id, in_memory=True)

        # TODO: Fix cases when Telegram returns an empty or unrecognized file.
        # Sometimes the downloaded media is not sent as a sticker by Telegram
        # (e.g. empty buffer or invalid format for .tgs).
        if not sticker_bytes or sticker_bytes.getbuffer().nbytes == 0:
            raise Exception(f"Downloaded file is empty for gift {gift_data['id']}")

        sticker = BufferedInputFile(
            file=sticker_bytes.getvalue(),
            filename="AnimatedSticker.tgs"
        )

        message = await bot.send_sticker(
            chat_id=config.STICKERS_CHANNEL_ID,
            sticker=sticker
        )

        return message.message_id
    except Exception as e:
        raise Exception(f"Upload error for gift {gift_data['id']}: {e}")
