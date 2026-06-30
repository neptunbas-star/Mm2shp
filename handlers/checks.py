from aiogram import Router
from aiogram.types import Message
from config import ADMIN_ID

router = Router()

CARD = """💳 Реквизиты

4400430392570518

Получатель:
Индира А

Банк:
Kaspi

После оплаты отправьте фото или документ с чеком.
"""

@router.message(lambda m: m.photo or m.document)
async def check(message: Message):
    await message.forward(ADMIN_ID)

    await message.answer(
        "✅ Чек отправлен.\n\n"
        "Ожидайте проверки администратора."
    )
