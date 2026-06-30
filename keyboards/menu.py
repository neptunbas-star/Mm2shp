from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 MM2 Прайс")],
        [KeyboardButton(text="👑 Админ Прайс")],
        [KeyboardButton(text="📢 Пиар Прайс")],
        [KeyboardButton(text="⭐ Отзывы")],
    ],
    resize_keyboard=True
)

buy_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💳 Купить",
                callback_data="buy"
            )
        ]
    ]
)

reviews_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⭐ Открыть отзывы",
                url="https://t.me/rishaproofsss"
            )
        ]
    ]
)
