from aiogram import Bot
from aiogram.types import FSInputFile
import os
from config import DOWNLOADS_DIR

async def delete_old_mes(bot: Bot, chat_id: int, message_id: int):
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

async def create_file(theme_file_url: str):
    path = f'{DOWNLOADS_DIR}/{theme_file_url}'

    if os.path.exists(path):
        file = FSInputFile(path)

        return file