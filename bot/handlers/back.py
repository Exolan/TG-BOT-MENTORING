from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards import main_keyboard, back_buttons
from database import Database
from aiogram import Bot
from utils import delete_old_mes

menu_router = Router()

@menu_router.callback_query(lambda call: call.data.startswith("menu"))
async def back_command(call: CallbackQuery, db: Database):
    await call.message.delete()

    callback_data = call.data

    if callback_data == "back_to_menu":
        await call.message.answer("Выберите категорию", reply_markup=await main_keyboard(db))
    
    elif callback_data.startswith("back_to_themes_"):
        category_id = callback_data.split("_")[-1]
        themes = await db.fetch_all(f"SELECT * FROM themes WHERE category_id = {category_id}")
        await call.message.answer(
            "Выберите тему",
            reply_markup=select_buttons(themes, isTheme=True)
        )