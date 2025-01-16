import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from database import Database
from config import BOT_TOKEN, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from handlers import setup_handlers

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

        dp.db = db
        
        setup_handlers(dp)
        print("Бот запущен")
        await dp.start_polling(bot)
    finally:
        if db.pool:
            db.pool.close()
            await db.pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())