import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import user, admin
from database import init_db

# Настройка логирования (чтобы видеть ошибки в консоли)
logging.basicConfig(level=logging.INFO)

async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Запуск базы данных
    await init_db()

    # Подключение роутеров (частей бота)
    dp.include_router(user.router)
    dp.include_router(admin.router)

    # Запуск бота
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
