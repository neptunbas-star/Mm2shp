from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_ID

router = Router()

class Payment(StatesGroup):
    waiting_for_check = State()

@router.message(Command("start"))
async def start_cmd(message: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="⚔️ MM2"), KeyboardButton(text="👑 Прайс админки")],
        [KeyboardButton(text="📢 Пиар прайс"), KeyboardButton(text="⭐ Отзывы")]
    ], resize_keyboard=True)
    await message.answer("Привет! Добро пожаловать в Qwerty shop.", reply_markup=kb)

@router.message(F.text == "⭐ Отзывы")
async def show_reviews(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Перейти к отзывам", url="https://t.me/rishaproofsss")]])
    await message.answer("Наши отзывы:", reply_markup=kb)

# Логика оплаты для разделов (MM2, Пиар прайс, Прайс админки)
@router.message(F.text.in_({"⚔️ MM2", "👑 Прайс админки", "📢 Пиар прайс"}))
async def payment_info(message: Message, state: FSMContext):
    await message.answer(
        "💳 **Оплата Каспи**\n"
        "Номер: `4400430392570518`\n"
        "Имя: Индира А\n\n"
        "Отправьте фото или скриншот чека прямо сюда.", parse_mode="Markdown"
    )
    await state.set_state(Payment.waiting_for_check)

@router.message(Payment.waiting_for_check, F.photo)
async def handle_check(message: Message, state: FSMContext, bot: Bot):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_{message.from_user.id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"decline_{message.from_user.id}")]
    ])
    await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, 
                         caption=f"📩 Новый чек от @{message.from_user.username or 'неизвестен'}", reply_markup=kb)
    await message.answer("✅ Чек отправлен на проверку!")
    await state.clear()
