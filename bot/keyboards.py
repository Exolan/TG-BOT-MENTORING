from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database import Database

async def main_keyboard(db: Database):
    categories = await db.fetch_all('SELECT * FROM categories')

    if categories:
        print(categories)