from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database import add_product
from config import ADMIN_ID
from keyboards.admin import admin_menu

router = Router()

class AddProduct(StatesGroup):
    category = State()
    name = State()
    price = State()

@router.message(lambda m: m.text == "/admin")
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "👑 Добро пожаловать в админ-панель!",
        reply_markup=admin_menu
    )
