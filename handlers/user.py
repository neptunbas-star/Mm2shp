from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from config import ADMIN_ID

router = Router()

# 1. Приветствие и кнопки
@router.message(Command("start"))
async def start_cmd(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="⚔️ MM2"), KeyboardButton(text="👑 Прайс админки")],
        [KeyboardButton(text="📢 Пиар прайс"), KeyboardButton(text="📞 Связь с владельцем")],
        [KeyboardButton(text="⭐ Отзывы")]
    ], resize_keyboard=True)
    await message.answer("Привет! Добро пожаловать в Qwerty shop.", reply_markup=kb)

# 2. Кнопка "Отзывы"
@router.message(F.text == "⭐ Отзывы")
async def show_reviews(message: Message):
    await message.answer("Наши отзывы: https://t.me/ссылка_на_отзывы")

# 3. Связь с владельцем (логика)
@router.message(F.text == "📞 Связь с владельцем")
async def contact_admin(message: Message, state: FSMContext):
    await state.set_state("waiting_for_message")
    await message.answer("Напишите ваше сообщение владельцу:")

@router.message(F.text, State("waiting_for_message"))
async def send_to_admin(message: Message, state: FSMContext):
    await message.bot.send_message(
        ADMIN_ID, 
        f"📩 Сообщение от @{message.from_user.username}:\n\n{message.text}"
    )
    await message.answer("✅ Сообщение отправлено владельцу!")
    await state.clear()
