from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from config import ADMIN_ID

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("У вас нет доступа.")
    
    # Создаем кнопки
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Управление товарами", callback_data="manage_products")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="📨 Рассылка", callback_data="broadcast")]
    ])
    
    await message.answer("🛠 Админ-панель Qwerty Shop. Выберите действие:", reply_markup=kb)
