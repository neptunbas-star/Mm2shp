from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

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
    await message.answer(
        """🛒 MM2

Пока товаров нет.

Позже они будут отображаться здесь автоматически.""",
        reply_markup=buy
    )


@router.message(lambda m: m.text == "👑 Админ Прайс")
async def admin(message: Message):
    await message.answer(
        """👑 Админ Прайс

Пока товаров нет.""",
        reply_markup=buy
    )


@router.message(lambda m: m.text == "📢 Пиар Прайс")
async def promo(message: Message):
    await message.answer(
        """📢 Пиар Прайс

Пока услуг нет.""",
        reply_markup=buy
    )
