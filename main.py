import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pyrogram import Client, enums
from pyrogram.errors import AuthKeyUnregistered, AuthKeyDuplicated, SessionRevoked
from pyrogram.types import LinkPreviewOptions

from app.commands import start_router
from app.core import config, logger, setup_logging
from app.database import init_db, close_db
from app.services import run_gift_monitor


async def main() -> None:
    setup_logging()
    await init_db()
    logger.info("Database initialized")

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

    dp = Dispatcher()
    for router in [start_router]:
        dp.include_router(router)

    async with client as app:
        me = await app.get_me()
        logger.info(f"Logged in as @{me.username or ''} [{me.id}]")

        try:
            await asyncio.gather(
                run_gift_monitor(app, bot),
                dp.start_polling(
                    bot,
                    polling_timeout=30,
                    handle_as_tasks=True,
                    close_bot_session=True,
                )
            )
        finally:
            await bot.session.close()
            await close_db()
            logger.info("Application shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (AuthKeyUnregistered, AuthKeyDuplicated, SessionRevoked):
        logger.error("Authorization error: Session expired or invalid. Please re-authenticate.")
    except (KeyboardInterrupt, SystemExit):
        logger.info("Program successfully terminated")
    except Exception as ex:
        logger.exception(f"Unexpected error: {ex}")
