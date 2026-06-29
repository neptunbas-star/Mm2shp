from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🗡 ММ2"), KeyboardButton(text="👑 Прайс админки")],
        [KeyboardButton(text="📢 Пиар прайс"), KeyboardButton(text="📞 Связь с владельцем")]
    ], resize_keyboard=True)
    await message.answer("👋 Добро пожаловать в Qwerty Shop!", reply_markup=kb)
