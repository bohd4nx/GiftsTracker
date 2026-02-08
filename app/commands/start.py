from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database import SessionLocal
from app.database.crud import GiftCRUD
from app.utils import escape_html

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    user = message.from_user

    async with SessionLocal() as session:
        gifts = await GiftCRUD.get_all(session)
        total_gifts = len(gifts)

    welcome_text = (
        f"🎁 <b>@GiftsRelease</b>\n\n"
        f"👋 Welcome, <b>{escape_html(user.first_name)}</b>!\n\n"
        f"📊 <b>Total Gifts:</b> <code>{total_gifts}</code>\n"
        f"🤖 <b>Bot Status:</b> 🟢 <b>Active</b>"
    )

    await message.answer(welcome_text)
