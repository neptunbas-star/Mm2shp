from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID

router = Router()

class BuyState(StatesGroup):
    waiting_for_check = State()

@router.message(Command("start"))
async def start(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="⚔️ MM2"), KeyboardButton(text="👑 Прайс админки")],
        [KeyboardButton(text="📢 Пиар прайс"), KeyboardButton(text="⭐ Отзывы")]
    ], resize_keyboard=True)
    await message.answer("Привет! Выберите раздел:", reply_markup=kb)

@router.message(F.text == "⭐ Отзывы")
async def reviews(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти к отзывам", url="https://t.me/rishaproofsss")]])
    await message.answer("Наши отзывы:", reply_markup=kb)

# Пример покупки
@router.message(F.text == "⚔️ MM2")
async def buy_mm2(message: Message, state: FSMContext):
    await message.answer(f"Реквизиты для оплаты (Каспи):\n4400430392570518 (Имя: Индира А)\n\nОтправьте скриншот чека в этот чат.")
    await state.set_state(BuyState.waiting_for_check)

@router.message(BuyState.waiting_for_check, F.photo)
async def get_check(message: Message, state: FSMContext):
    # Пересылка чека админу
    await message.bot.send_photo(ADMIN_ID, message.photo[-1].file_id, 
                                 caption=f"📩 Новый чек от @{message.from_user.username}\nID пользователя: {message.from_user.id}")
    await message.answer("✅ Чек отправлен на проверку!")
    await state.clear()
