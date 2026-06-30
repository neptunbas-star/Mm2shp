from aiogram import Bot, Dispatcher
import asyncio

# Импортируем токен из твоего файла config.py
from config import BOT_TOKEN

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Здесь позже будем подключать роутеры (handlers)
# dp.include_router(user.router)

async def main():
    print("Бот успешно запущен!")
    # Запуск процесса опроса (polling)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
