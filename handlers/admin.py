from aiogram import Router
from aiogram.types import Message
from config import ADMIN_ID

router = Router()

@router.message(lambda m: m.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "👑 Админ-панель\n\n"
        "➕ Добавить товар\n"
        "🗑️ Удалить товар\n"
        "✏️ Изменить цену\n"
        "📦 Список товаров"
    )
