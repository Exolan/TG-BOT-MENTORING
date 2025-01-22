from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import main_keyboard, back_button, select_theme_buttons
from database import Database
from aiogram import Bot
from utils import delete_old_mes

category_router = Router()

@category_router.callback_query(lambda call: call.data.startswith("select_category_"))
async def select_category(call: CallbackQuery, db: Database, bot: Bot):
    await call.message.delete()

    category_id = call.data.split("_")[2]

    themes = await db.fetch_all(f"SELECT * FROM themes WHERE category_id = {category_id}")

    if len(themes) == 0:
        await call.message.answer(f"В этой категории пока нет тем", reply_markup=back_button())
    elif len(themes) == 1:
        theme = themes[0]

        await call.message.answer(f"<b>{theme['theme_name']}</b>\n\n{theme['theme_text']}", reply_markup=back_button())        
    else:
        await call.message.answer("Выберите тему", reply_markup=select_theme_buttons(themes))