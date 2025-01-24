from aiogram import Bot
from aiogram.types import Message, FSInputFile
from keyboards import back_buttons
import os

async def delete_old_mes(bot: Bot, chat_id: int, message_id: int):
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

async def create_file(message: Message, theme_file_url: str):
    if os.path.exists(theme_file_url):
        file = FSInputFile(theme_file_url)
        
        await message.answer_document(file, caption="Подробнее в этом файле", reply_markup=back_buttons())

    else:
        await message.answer(f"Произошла ошибка. Повторите попытку позже", reply_markup=back_buttons())