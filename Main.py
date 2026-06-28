import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = "8904523107:AAEWjUe72LjE0allJ-42FIPW1I30DrKlctA"
ADMIN_ID = 8875311417
CARD_NUMBER = "4400430392570518"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- ТОВАРЫ ---
goods = {
    "Ножи": {
        "Корупт": "2100tg", "Candy": "580tg", "Посох сердца": "1700tg",
        "Лезвия сердце": "650tg", "Топор вампира": "2700tg", "Бита": "800tg", "Sweet": "1200tg"
    },
    "Пистолеты": {
        "Raygun": "3500tg", "Снежная пушка": "2550tg", "Арбалет": "1600tg",
        "Зимний арбалет": "1400tg", "Ватерган": "1500tg", "Buble": "2550tg"
    },
    "Сеты": {
        "Rainbow set": "2700tg", "Sakura set": "4600tg", "Sunset": "3000tg",
        "Flora set": "2700tg", "Дух сет": "2700tg", "Австралия сет": "850tg",
        "Ляденой сет": "850tg", "Candy set": "800tg"
    }
}

# --- ВЕБ-СЕРВЕР ---
async def handle(request):
    return web.Response(text="Бот в сети")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

# --- КНОПКИ И ЛОГИКА ---
@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [[types.KeyboardButton(text="Ножи"), types.KeyboardButton(text="Пистолеты")],
          [types.KeyboardButton(text="Сеты"), types.KeyboardButton(text="Написать сообщение")]]
    await message.answer("Добро пожаловать в Sweet Shop!", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text.in_(["Ножи", "Пистолеты", "Сеты"]))
async def show_category(message: types.Message):
    cat = message.text
    items = goods.get(cat, {})
    kb = [[InlineKeyboardButton(text=f"{name} - {price}", callback_data=f"buy_{cat}_{name}")] for name, price in items.items()]
    await message.answer(f"Каталог - {cat}:", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(F.data.startswith("buy_"))
async def buy_item(callback: types.CallbackQuery):
    _, cat, item = callback.data.split("_")
    price = goods[cat][item]
    await callback.message.answer(f"Вы выбрали: {item} ({price})\nОплатите на карту: `{CARD_NUMBER}`\nПришлите скриншот чека сюда!")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_{message.from_user.id}"),
         InlineKeyboardButton(text="❌ Отклонить", callback_data=f"decline_{message.from_user.id}")]
    ])
    await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    await bot.send_message(ADMIN_ID, f"Новый чек от @{message.from_user.username or message.from_user.id}", reply_markup=kb)
    await message.answer("Чек принят на проверку.")

@dp.callback_query(F.data.startswith(("accept_", "decline_")))
async def check_decision(callback: types.CallbackQuery):
    action, user_id = callback.data.split("_")
    status = "ПРИНЯТ ✅" if action == "accept" else "ОТКЛОНЕН ❌"
    await bot.send_message(int(user_id), f"Ваш заказ: {status}")
    await callback.message.edit_text(f"Решение: {status}")

# --- ОБРАТНАЯ СВЯЗЬ ---
class AdminStates(StatesGroup): waiting_for_message = State()

@dp.message(F.text == "Написать сообщение")
async def contact_start(message: types.Message, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_message)
    await message.answer("Напиши сообщение админу:")

@dp.message(AdminStates.waiting_for_message)
async def contact_process(message: types.Message, state: FSMContext):
    await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    await message.answer("Сообщение отправлено!")
    await state.clear()

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
