from aiogram import Router, Bot
from aiogram.types import Message
from database import Database
from keyboards import back_buttons

search_router = Router()

@search_router.message()
async def search_info(message: Message, bot: Bot, db: Database):
    search_text = message.text.strip()

    if len(search_text) < 5:
        await message.answer("Я вас не понимаю. Напишите более подробно", reply_markup=back_buttons())
        return

    try:
        query_categories = 'SELECT * FROM categories WHERE LOWER(category_name) LIKE LOWER(%s) OR LOWER(category_text) LIKE LOWER(%s)'

        results_categories = await db.fetch_all(query_categories, (f"%{search_text}%", f"%{search_text}%"))

        # query_categories = f'SELECT * FROM categories WHERE LOWER(category_name) LIKE LOWER({search_text}) OR LOWER(category_text) LIKE LOWER({search_text})'

        # results_categories = await db.fetch_all(query_categories)

        if not results_categories:
            await message.answer("Я ничего не нашел", reply_markup=back_buttons())

    except Exception as e:
        await message.answer("Произошла ошибка. Попробуйте позже", reply_markup=back_buttons())
        print(f"Ошибка поиска: {e}")
    