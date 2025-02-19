from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import TelegramBadRequest
import os
from config import DOWNLOADS_DIR, IMAGES_DIR

async def delete_old_mes(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id-1)
    except TelegramBadRequest as e:
        if "message to delete not found" in str(e):
            # Просто игнорируем ошибку, если сообщение не найдено
            print(f"Сообщение {message_id-1} не найдено, пропускаем удаление")
        else:
            raise


async def create_file(theme_file_url: str):
    path = f'{DOWNLOADS_DIR}/{theme_file_url}'

    if os.path.exists(path):
        file = FSInputFile(path)

        return file
    
async def open_image(image_name: str):
    path = f'{IMAGES_DIR}/{image_name}.png'

    if os.path.exists(path):
        image = FSInputFile(path)

        return image

    