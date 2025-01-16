from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import main_keyboard

start_router = Router()

@start_router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("<b>Уважаемый наставник, приветствуем!</b>")
    await message.answer("Данный чат-бот предназначен для помощи в Вашей работе с наставляемым")
    await message.answer("Выбрав соответствующее поле меню, а также сформировав интересующий запрос, вы сможете найти ответы на возникающие вопросы")
    await message.answer("Успешного и результативного наставничества!", reply_markup=await main_keyboard(db))
    