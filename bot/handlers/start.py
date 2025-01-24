from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import main_keyboard
from database import Database
from utils import delete_old_mes

start_router = Router()

@start_router.message(Command("start"))
async def start_command(message: Message, db: Database, bot: Bot):
    await delete_old_mes(bot, message.chat.id, message.message_id)

    await message.answer("<b>Уважаемый наставник, приветствуем!</b>\n\n"\
                        "Данный чат-бот предназначен для помощи в Вашей работе с наставляемым\n"\
                        "Выбрав соответствующее поле меню, а также сформировав интересующий запрос, вы сможете найти ответы на возникающие вопросы\n\n"\
                        "Успешного и результативного наставничества!", reply_markup=await main_keyboard(db))
