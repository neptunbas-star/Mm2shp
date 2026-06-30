from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database import get_products

router = Router()

buy = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💳 Купить",
                callback_data="buy"
            )
        ]
    ]
)


@router.message(lambda m: m.text == "🛒 MM2 Прайс")
async def mm2(message: Message):

    products = await get_products("MM2")

    if not products:
        await message.answer("❌ Пока товаров нет.")
        return

    text = "🛒 MM2 Прайс\n\n"

    for product in products:
        text += f"📦 {product[1]}\n💰 {product[2]}₸\n\n"

    await message.answer(text, reply_markup=buy)


@router.message(lambda m: m.text == "👑 Админ Прайс")
async def admin_price(message: Message):

    products = await get_products("Админ")

    if not products:
        await message.answer("❌ Пока товаров нет.")
        return

    text = "👑 Админ Прайс\n\n"

    for product in products:
        text += f"📦 {product[1]}\n💰 {product[2]}₸\n\n"

    await message.answer(text, reply_markup=buy)


@router.message(lambda m: m.text == "📢 Пиар Прайс")
async def promo(message: Message):

    products = await get_products("Пиар")

    if not products:
        await message.answer("❌ Пока услуг нет.")
        return

    text = "📢 Пиар Прайс\n\n"

    for product in products:
        text += f"📦 {product[1]}\n💰 {product[2]}₸\n\n"

    await message.answer(text, reply_markup=buy)
