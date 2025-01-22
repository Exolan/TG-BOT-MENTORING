from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import main_keyboard, back_button
from database import Database
from aiogram import Bot
from utils import delete_old_mes

back_router = Router()

@back_router.callback_query(lambda call: call.data == "back")
async def back_command(call: CallbackQuery, db: Database):
    await call.message.delete()
    await call.message.answer("Вы вернулись назад", reply_markup=await main_keyboard(db))