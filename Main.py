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
CARD_NUMBER = "4400430392570518"  # Карта обновлена

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
async def handle(request):
    return web.Response(text="Бот работает")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
# ------------------------------

class AdminStates(StatesGroup):
    waiting_for_item_name = State()
    waiting_for_message = State()

goods = {"Ножи": {}, "Пистолеты": {}, "Сеты": {}}

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [[types.KeyboardButton(text="Ножи"), types.KeyboardButton(text="Пистолеты")],
          [types.KeyboardButton(text="Сеты"), types.KeyboardButton(text="Написать сообщение")]]
    await message.answer("Добро пожаловать в Sweet Shop!", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text.in_(["Ножи", "Пистолеты", "Сеты"]))
async def show_category(message: types.Message):
    cat = message.text
    if not goods[cat]:
        await message.answer(f"В разделе {cat} пока пусто.")
        return
    kb = [[InlineKeyboardButton(text=f"{item} - {price}", callback_data=f"buy_{cat}_{item}")] for item, price in goods[cat].items()]
    await message.answer(f"Каталог - {cat}:", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))

@dp.callback_query(F.data.startswith("buy_"))
async def buy_item(callback: types.CallbackQuery):
    _, cat, item = callback.data.split("_")
    await callback.message.answer(f"Вы выбрали: {item}\nОплатите на карту: `{CARD_NUMBER}`\nПосле оплаты пришлите скриншот чека в этот чат!")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_{message.from_user.id}"),
         InlineKeyboardButton(text="❌ Отклонить", callback_data=f"decline_{message.from_user.id}")]
    ])
    await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    await bot.send_message(ADMIN_ID, "Решение по чеку:", reply_markup=kb)
    await message.answer("Чек принят на проверку.")

@dp.callback_query(F.data.startswith(("accept_", "decline_")))
async def check_decision(callback: types.CallbackQuery):
    action, user_id = callback.data.split("_")
    status = "ПРИНЯТ ✅" if action == "accept" else "ОТКЛОНЕН ❌"
    await bot.send_message(int(user_id), f"Ваш чек: {status}")
    await callback.message.edit_text(f"Решение: {status}")

@dp.message(F.text == "Написать сообщение")
async def contact_start(message: types.Message, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_message)
    await message.answer("Напиши сообщение админу:")

@dp.message(AdminStates.waiting_for_message)
async def contact_process(message: types.Message, state: FSMContext):
    await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    await message.answer("Сообщение отправлено!")
    await state.clear()

@dp.message(F.chat.id == ADMIN_ID, F.reply_to_message)
async def reply_to_user(message: types.Message):
    user_id = message.reply_to_message.forward_from.id
    await bot.send_message(user_id, f"Ответ Sweet Shop: {message.text}")
    await message.answer("Ответ отправлен.")

@dp.message(Command("admin"))
async def admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        kb = [[types.KeyboardButton(text="Добавить товар"), types.KeyboardButton(text="Удалить товар")]]
        await message.answer("Админка:", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text == "Добавить товар")
async def add_item_menu(message: types.Message):
    kb = [[types.KeyboardButton(text="В Ножи"), types.KeyboardButton(text="В Пистолеты"), types.KeyboardButton(text="В Сеты")]]
    await message.answer("Куда добавляем?", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text.startswith("В "))
async def add_item_step1(message: types.Message, state: FSMContext):
    cat = message.text.replace("В ", "")
    await state.update_data(category=cat)
    await state.set_state(AdminStates.waiting_for_item_name)
    await message.answer(f"Напиши Название-Цена:")

@dp.message(AdminStates.waiting_for_item_name)
async def add_item_step2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cat = data['category']
    try:
        name, price = message.text.split("-")
        goods[cat][name.strip()] = price.strip()
        await message.answer(f"Товар {name} добавлен в {cat}!")
    except:
        await message.answer("Ошибка формата! (Нужно: Название-Цена)")
    await state.clear()

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
