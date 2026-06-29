from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_ID

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    # Проверка, что команду вводит именно админ
    if message.from_user.id != ADMIN_ID:
        return await message.answer("У вас нет доступа к этой команде.")
    
    await message.answer(
        "🛠 **Админ-панель Qwerty Shop**\n\n"
        "Доступные функции:\n"
        "📦 Управление товарами\n"
        "📊 Статистика\n"
        "📨 Рассылка\n\n"
        "Выберите действие (пока в разработке).",
        parse_mode="Markdown"
    )
