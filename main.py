import asyncio
from pathlib import Path

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pyrogram import Client, enums
from pyrogram.errors import AuthKeyUnregistered, AuthKeyDuplicated, SessionRevoked
from pyrogram.types import LinkPreviewOptions

from app.core import config, logger, setup_logging
from app.services import run_gift_monitor


class App:
    @staticmethod
    async def run() -> None:
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
            skip_updates=True,
            workers=8,
            sleep_threshold=30,
            max_concurrent_transmissions=10,
            no_joined_notifications=True,
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

            try:
                await run_gift_monitor(app, bot)
            finally:
                await bot.session.close()


if __name__ == "__main__":
    setup_logging()
    try:
        asyncio.run(App.run())
    except (AuthKeyUnregistered, AuthKeyDuplicated, SessionRevoked):
        logger.error("Authorization error: Session expired or invalid. Please re-authenticate.")
    except (KeyboardInterrupt, SystemExit):
        logger.info("Program successfully terminated")
    except Exception as ex:
        logger.exception(f"Unexpected error: {ex}")
