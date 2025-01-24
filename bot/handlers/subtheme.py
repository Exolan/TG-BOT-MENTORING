from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import main_keyboard, back_buttons, select_buttons
from database import Database
from aiogram import Bot
from utils import delete_old_mes, create_file

subtheme_router = Router()

@subtheme_router.callback_query(lambda call: call.data.startswith("select_subtheme_"))
async def select_theme(call: CallbackQuery, db: Database, previous_callback_data: str):
    await call.message.delete()

    subtheme_id = call.data.split("_")[2]

    subtheme = await db.fetch_one(f"SELECT * FROM subthemes WHERE subtheme_id = {subtheme_id}")
    
    subtheme_name = subtheme["subtheme_name"]
    subtheme_text = subtheme["subtheme_text"]
    subtheme_file_url = subtheme["subtheme_file_url"]

    if subtheme_text:
        await call.message.answer(f"<b>{subtheme_name}</b>\n\n{subtheme_text}", reply_markup=back_buttons(previous_callback_data))

    if subtheme_file_url:
        await create_file(call.message, subtheme_file_url)