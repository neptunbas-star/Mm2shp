from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить товар")],
        [KeyboardButton(text="🗑️ Удалить товар")],
        [KeyboardButton(text="✏️ Изменить цену")],
        [KeyboardButton(text="📋 Все товары")],
        [KeyboardButton(text="🏠 Главное меню")]
    ],
    resize_keyboard=True
)
