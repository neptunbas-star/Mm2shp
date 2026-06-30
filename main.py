import asyncio
from aiogram import Bot, Dispatcher
from handlers import user

# Твой токен внедрен сюда
TOKEN = "8744469494:AAE7U5sYSBv8K60ln9aLjPDiO3FgKzOcZ_A"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    dp.include_router(user.router)
    
    print("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
