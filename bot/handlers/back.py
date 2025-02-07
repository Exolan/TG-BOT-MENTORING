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
    await call.message.answer("Вы вернулись назад", reply_markup=await main_keyboard(db))