from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID

router = Router()

# ... твой текущий код (start и другие) ...

@router.message(F.text == "📞 Связь с владельцем")
async def contact_admin(message: Message, state: FSMContext):
    await state.set_state("waiting_for_message")
    await message.answer("Напишите ваше сообщение владельцу.")

# Добавь этот блок:
@router.message(F.text, State("waiting_for_message"))
async def send_to_admin(message: Message, state: FSMContext):
    await message.bot.send_message(
        ADMIN_ID, 
        f"📩 Новое сообщение от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{message.text}"
    )
    await message.answer("✅ Ваше сообщение отправлено владельцу!")
    await state.clear()
