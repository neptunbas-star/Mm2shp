import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import create_db
from handlers.start import router as start_router
from handlers.admin import router as admin_router
from handlers.checks import router as checks_router

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(shop_router)
dp.include_router(admin_router)
dp.include_router(checks_router)


async def main():
    await create_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
