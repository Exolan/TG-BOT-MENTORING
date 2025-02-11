from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram.filters import Command
from keyboards import back_buttons
from database import Database
from config import IMAGES_DIR

help_router = Router()

@help_router.message(Command("help"))
async def help_command(message: Message, db: Database, bot: Bot):
    chat_id = message.chat.id

    path = f"{IMAGES_DIR}test.jpg"

    photo = FSInputFile(path)

    await bot.send_photo(chat_id=chat_id,  photo=photo, caption = 'text', reply_markup=back_buttons())