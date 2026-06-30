from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.menu import main_menu, reviews_button

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в Qwerty Shop!\n\n"
        "Выберите нужный раздел:",
        reply_markup=main_menu
    )


@router.message(lambda message: message.text == "⭐ Отзывы")
async def reviews(message: Message):
    await message.answer(
        "Нажмите кнопку ниже, чтобы открыть отзывы:",
        reply_markup=reviews_button
    )
