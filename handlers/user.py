from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from config import ADMIN_ID

router = Router()

# Класс состояний
class OrderForm(StatesGroup):
    waiting_for_piar_count = State()
    waiting_for_admin_weeks = State()
    waiting_for_receipt = State()

# Клавиатура
admin_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ Добавить товар"), KeyboardButton(text="➖ Убрать товар")],
    [KeyboardButton(text="ММ2"), KeyboardButton(text="Пиар прайс")],
    [KeyboardButton(text="Админки"), KeyboardButton(text="Отзывы")]
], resize_keyboard=True)

# 1. ОБРАБОТКА ЧЕКА (Фото или Документ)
@router.message(OrderForm.waiting_for_receipt, F.photo | F.document)
async def process_receipt(message: Message, state: FSMContext):
    await message.answer("✅ Чек принят на проверку. Владелец скоро свяжется!")
    await state.clear()

# 2. ПИАР ПРАЙС
@router.message(F.text == "Пиар прайс")
async def show_piar(message: Message):
    text = "🔥 Пиар Курс 8: от 15 до 75 участников.\nЦена: 8 тг за 1 уч.\nКанал: @Qwerty5Shop"
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Купить", callback_data="buy_piar")]])
    await message.answer(text, reply_markup=kb)

@router.callback_query(F.data == "buy_piar")
async def ask_piar_count(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите количество человек (15-75):")
    await state.set_state(OrderForm.waiting_for_piar_count)

@router.message(OrderForm.waiting_for_piar_count)
async def calc_piar(message: Message, state: FSMContext):
    try:
        count = int(message.text)
        if 15 <= count <= 75:
            price = count * 8
            await state.update_data(price=price)
            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Оплатить", callback_data="show_req")]])
            await message.answer(f"Выйдет {price} тенге. Нажмите кнопку:", reply_markup=kb)
        else:
            await message.answer("Пожалуйста, введите число от 15 до 75.")
    except:
        await message.answer("Введите корректное число.")

# 3. АДМИНКИ
@router.message(F.text == "Админки")
async def show_admin_price(message: Message):
    text = "👑 Админки: 1 нед (200тг), 2 нед (400тг), 3 нед (600тг), Месяц (900тг)."
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Купить", callback_data="buy_admin")]])
    await message.answer(text, reply_markup=kb)

@router.callback_query(F.data == "buy_admin")
async def ask_admin_weeks(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите срок (1 неделя, 2 недели, 3 недели или Месяц):")
    await state.set_state(OrderForm.waiting_for_admin_weeks)

@router.message(OrderForm.waiting_for_admin_weeks)
async def calc_admin(message: Message, state: FSMContext):
    text = message.text.lower()
    prices = {"1 неделя": 200, "2 недели": 400, "3 недели": 600, "месяц": 900}
    if text in prices:
        price = prices[text]
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Оплатить", callback_data="show_req")]])
        await message.answer(f"Выйдет {price} тенге. Нажмите кнопку:", reply_markup=kb)
    else:
        await message.answer("Введите корректно: 1 неделя, 2 недели, 3 недели или Месяц.")

# 4. РЕКВИЗИТЫ И ФИНАЛ
@router.callback_query(F.data == "show_req")
async def show_requisites(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("💳 Kaspi: 4400430392570518 (Индира А)\n\nПришлите чек или документ:")
    await state.set_state(OrderForm.waiting_for_receipt)

# 5. КНОПКИ
@router.message(F.text == "ММ2")
async def show_mm2(message: Message):
    await message.answer("Раздел ММ2 в разработке.")

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Админ-панель открыта:", reply_markup=admin_kb)
