import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from database import Database
from config import BOT_TOKEN, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

from handlers.start import start_router
from handlers.category import category_router
from handlers.back import menu_router
from handlers.theme import theme_router
from handlers.subtheme import subtheme_router
from handlers.search import search_router

from middleware import DatabaseMiddleware, BotMiddleware

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

router = Router()
dp.include_router(router)

db = Database(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    db=DB_NAME
)

async def main():
    try:
        await db.connect()

        dp.update.middleware(DatabaseMiddleware(db))
        dp.update.middleware(BotMiddleware(bot))
        
        dp.include_router(start_router)
        dp.include_router(category_router)
        dp.include_router(menu_router)
        dp.include_router(theme_router)
        dp.include_router(subtheme_router)
        dp.include_router(search_router)
        
        print("Бот запущен")
        await dp.start_polling(bot)
    finally:
        if db.pool:
            db.pool.close()
            await db.pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())