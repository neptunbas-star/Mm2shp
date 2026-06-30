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

from aiogram.types import CallbackQuery


@router.callback_query(F.data.startswith("accept_"))
async def accept(callback: CallbackQuery):

    user = int(callback.data.split("_")[1])

    await callback.bot.send_message(
        user,
        "✅ Ваш чек принят!\n\n"
        "Скоро владелец свяжется с вами для выдачи товара.\n\n"
        "Спасибо за покупку ❤️"
    )

    await callback.message.edit_reply_markup()


@router.callback_query(F.data.startswith("reject_"))
async def reject(callback: CallbackQuery):

    user = int(callback.data.split("_")[1])

    await callback.bot.send_message(
        user,
        "❌ Ваш чек отклонён.\n\n"
        "Отправьте более качественный чек."
    )

    await callback.message.edit_reply_markup()
