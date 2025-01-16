from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

help_router = Router()

@help_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Я еще не умею помогать")