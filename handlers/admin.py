from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from config import ADMIN_ID

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID: return
    await message.answer("🛠 Админ-панель: управление товарами и ценами доступно.")

@router.callback_query(F.data.startswith("accept_"))
async def accept_check(callback: CallbackQuery, bot: Bot):
    user_id = callback.data.split("_")[1]
    await bot.send_message(user_id, "✅ Ваш чек принят! Скоро с вами свяжется владелец для того чтобы выдать товар. Спасибо за покупку!")
    await callback.message.edit_caption(caption="✅ Чек принят.")

@router.callback_query(F.data.startswith("decline_"))
async def decline_check(callback: CallbackQuery, bot: Bot):
    user_id = callback.data.split("_")[1]
    await bot.send_message(user_id, "❌ Ваш чек отклонен.")
    await callback.message.edit_caption(caption="❌ Чек отклонен.")
