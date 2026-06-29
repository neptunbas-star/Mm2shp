from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from config import ADMIN_ID

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("У вас нет доступа.")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Управление товарами", callback_data="manage_products")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="📨 Рассылка", callback_data="broadcast")]
    ])
    await message.answer("🛠 Админ-панель Qwerty Shop:", reply_markup=kb)

# ДОБАВЬ ЭТОТ ОБРАБОТЧИК:
@router.callback_query(F.data == "manage_products")
async def manage_products(callback: CallbackQuery):
    await callback.message.edit_text(
        "📦 **Управление товарами**\n\n"
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить товар", callback_data="add_product")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="admin_main")]
        ])
    )
