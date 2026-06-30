from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()

def main_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="ММ2"), KeyboardButton(text="Пиар прайс")],
        [KeyboardButton(text="Админки")]
    ], resize_keyboard=True)

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Выбери раздел:", reply_markup=main_kb())

@router.message(F.text == "ММ2")
async def mm2(message: Message):
    await message.answer("Раздел ММ2. Все товары и цены в нашем канале: @Qwerty5Shop")

@router.message(F.text == "Пиар прайс")
async def piar(message: Message):
    await message.answer("🔥 Пиар Курс: от 15 до 75 участников.\nЦена: 8 тг за 1 участника.\nКанал: @Qwerty5Shop")

@router.message(F.text == "Админки")
async def admin(message: Message):
    await message.answer("👑 Админки:\n1 неделя — 200 тг\n2 недели — 400 тг\nМесяц — 900 тг\nПиши в @Qwerty5Shop")
