from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import main_keyboard, back_button, select_theme_buttons
from database import Database
from aiogram import Bot
from utils import delete_old_mes, create_file

theme_router = Router()

@theme_router.callback_query(lambda call: call.data.startswith("select_theme_"))
async def select_theme(call: CallbackQuery, db: Database):
    await call.message.delete()

    theme_id = call.data.split("_")[2]

    theme = await db.fetch_one(f"SELECT * FROM themes WHERE theme_id = {theme_id}")

    subtheme = await db.fetch_all(f"SELECT * FROM subthemes WHERE theme_id = {theme_id}")
    
    theme_name = theme["theme_name"]
    theme_text = theme["theme_text"]
    theme_file_url = theme["theme_file_url"]

    if subtheme:
        print(subtheme)

    if theme_text:
        await call.message.answer(f"<b>{theme_name}</b>\n\n{theme_text}", reply_markup=back_button())

    if theme_file_url:
        await create_file(call.message, theme_file_url)