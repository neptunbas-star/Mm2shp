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
    
@router.message(lambda m: m.text == "➕ Добавить товар")
async def add_start(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "Введите категорию:\n\nMM2\nАдмин\nПиар"
    )

    await state.set_state(AddProduct.category)


@router.message(AddProduct.category)
async def category(message: Message, state: FSMContext):

    await state.update_data(category=message.text)

    await message.answer("Введите название товара:")

    await state.set_state(AddProduct.name)


@router.message(AddProduct.name)
async def name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    await message.answer("Введите цену:")

    await state.set_state(AddProduct.price)


@router.message(AddProduct.price)
async def price(message: Message, state: FSMContext):

    data = await state.get_data()

    await add_product(
        data["category"],
        data["name"],
        int(message.text)
    )

    await message.answer("✅ Товар успешно добавлен!")

    await state.clear()
