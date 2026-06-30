from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(lambda m: m.text == "🛒 MM2 Прайс")
async def mm2(message: Message):
    await message.answer(
        "🛒 MM2 Прайс\n\n"
        "Пока товаров нет.\n"
        "Позже они будут загружаться из базы данных."
    )


@router.message(lambda m: m.text == "👑 Админ Прайс")
async def admin_price(message: Message):
    await message.answer(
        "👑 Админ Прайс\n\n"
        "Пока товаров нет."
    )


@router.message(lambda m: m.text == "📢 Пиар Прайс")
async def promo(message: Message):
    await message.answer(
        "📢 Пиар Прайс\n\n"
        "Пока услуг нет."
    )
