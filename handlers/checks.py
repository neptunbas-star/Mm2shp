from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import ADMIN_ID

router = Router()


def admin_buttons(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Принять",
                    callback_data=f"accept_{user_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject_{user_id}"
                )
            ]
        ]
    )


@router.message(F.photo | F.document)
async def check(message: Message):

    text = f"""
🧾 Новый чек

👤 Пользователь:
@{message.from_user.username}

🆔 ID:
{message.from_user.id}
"""

    if message.photo:
        await message.bot.send_photo(
            ADMIN_ID,
            photo=message.photo[-1].file_id,
            caption=text,
            reply_markup=admin_buttons(message.from_user.id)
        )

    elif message.document:
        await message.bot.send_document(
            ADMIN_ID,
            document=message.document.file_id,
            caption=text,
            reply_markup=admin_buttons(message.from_user.id)
        )

    await message.answer(
        "✅ Чек отправлен.\n\nОжидайте проверки администратора."
    )
