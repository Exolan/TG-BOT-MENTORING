from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import main_keyboard
from database import Database
from utils import delete_old_mes

help_router = Router()

@help_router.message(Command("help"))
async def help_command(message: Message, db: Database, bot: Bot):
    await message.answer("Я еще не умею помогать", reply_markup=await main_keyboard(db))