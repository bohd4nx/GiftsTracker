import asyncio
import json
from pathlib import Path

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pyrogram import Client, enums
from pyrogram.types import LinkPreviewOptions

from app.core import config, logger, setup_logging
from app.notifications import edit_notification


async def update_messages():
    client = Client(
        name="GiftsTracker",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        phone_number=config.PHONE_NUMBER,
        password=config.PASSWORD if config.PASSWORD else None,
        device_model="MacBook Pro M3 Pro",
        system_version="macOS 26.2",
        app_version="Telegram Desktop 6.5 arm64",
        lang_pack="tdesktop",
        lang_code="en",
        workdir=str(Path(__file__).parent),
        client_platform=enums.ClientPlatform.DESKTOP,
        parse_mode=enums.ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        sleep_threshold=30,
        max_concurrent_transmissions=10
    )

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        )
    )

    async with client as app:
        me = await app.get_me()
        logger.info(f"Logged in as @{me.username or ''} [{me.id}]")

        # Load history
        history_file = Path(__file__).parent / "history.json"
        with open(history_file, "r", encoding="utf-8") as f:
            gifts = json.load(f)

        logger.info(f"Loaded {len(gifts)} gifts from history")

        total_edits = 0
        for idx, gift_data in enumerate(gifts, 1):
            gift_id = gift_data.get("id")
            msg_id = gift_data.get("msg_id")
            upgrade_msg_id = gift_data.get("upgrade_msg_id")
            sticker_msg_id = gift_data.get("sticker_msg_id")

            logger.info(f"Processing gift {idx}/{len(gifts)}: {gift_id}")

            # Edit main message
            if msg_id and sticker_msg_id:
                logger.info(f"  Editing main message {msg_id} for gift {gift_id}")
                try:
                    await edit_notification(app, bot, msg_id, gift_data, sticker_msg_id, is_upgrade=False)
                    total_edits += 1
                    logger.info(f"  Successfully edited main message {msg_id}")
                    await asyncio.sleep(3)
                except Exception as e:
                    logger.error(f"  Failed to edit main message {msg_id}: {e}")

            # Edit upgrade message
            if upgrade_msg_id and sticker_msg_id:
                logger.info(f"  Editing upgrade message {upgrade_msg_id} for gift {gift_id}")
                try:
                    await edit_notification(app, bot, upgrade_msg_id, gift_data, sticker_msg_id, is_upgrade=True)
                    total_edits += 1
                    logger.info(f"  Successfully edited upgrade message {upgrade_msg_id}")
                    await asyncio.sleep(3)
                except Exception as e:
                    logger.error(f"  Failed to edit upgrade message {upgrade_msg_id}: {e}")

        logger.info(f"Finished! Edited {total_edits} messages total")
        await bot.session.close()


if __name__ == "__main__":
    setup_logging()
    try:
        asyncio.run(update_messages())
    except KeyboardInterrupt:
        logger.info("Update interrupted by user")
    except Exception as ex:
        logger.exception(f"Unexpected error: {ex}")
