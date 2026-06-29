from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🗡 ММ2"), KeyboardButton(text="👑 Прайс админки")],
        [KeyboardButton(text="📢 Пиар прайс"), KeyboardButton(text="📞 Связь с владельцем")],
        [KeyboardButton(text="⭐ Отзывы")]
    ], resize_keyboard=True)
    await message.answer("👋 Добро пожаловать в Qwerty Shop!\n\nВыберите нужный раздел ниже.", reply_markup=kb)

@router.message(F.text == "⭐ Отзывы")
async def show_reviews(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к отзывам", url="https://t.me/rishaproofsss")]
    ])
    await message.answer("Наши отзывы:", reply_markup=kb)

@router.message(F.text == "📞 Связь с владельцем")
async def contact_admin(message: Message, state: FSMContext):
    await state.set_state("waiting_for_message")
    await message.answer("Напишите ваше сообщение владельцу.")
