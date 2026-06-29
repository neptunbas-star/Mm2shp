import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import user, admin
from aiohttp import web

async def handle(request): return web.Response(text="Бот в сети")

async def main():
    # Запуск веб-сервера для Render
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(user.router)
    dp.include_router(admin.router) # Добавь эту строку

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
