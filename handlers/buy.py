from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

CARD = """
💳 Реквизиты для оплаты

💳 Карта:
4400 4303 9257 0518

👤 Получатель:
Индира А

🏦 Банк:
Kaspi

📸 После оплаты отправьте фото или документ с чеком.
"""


@router.callback_query(F.data == "buy")
async def buy(callback: CallbackQuery):
    await callback.message.answer(CARD)
    await callback.answer()
