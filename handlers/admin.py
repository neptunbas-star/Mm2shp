from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID: return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Добавить товар", callback_data="add_prod")],
        [InlineKeyboardButton(text="🗑 Удалить товар", callback_data="del_prod")]
    ])
    await message.answer("Админ-панель:", reply_markup=kb)

# Логика принятия чека (в админке)
@router.message(F.caption.contains("Новый чек"))
async def accept_check(message: Message, bot: Bot):
    # Тут можно добавить кнопки под пересланным чеком
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Принять", callback_data="accept"), 
         InlineKeyboardButton(text="❌ Отклонить", callback_data="decline")]
    ])
    await message.answer("Что делаем с чеком?", reply_markup=kb)

@router.callback_query(F.data == "accept")
async def confirm(callback: CallbackQuery, bot: Bot):
    user_id = callback.message.caption.split("ID пользователя: ")[1]
    await bot.send_message(user_id, "✅ Ваш чек принят! Скоро с вами свяжется владелец.")
    await callback.message.edit_text("✅ Чек принят.")
