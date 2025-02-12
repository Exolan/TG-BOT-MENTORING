from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram import Bot

class BotMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot

        super().__init__()

    async def __call__(self, handler, event: TelegramObject, data: dict):
        # Добавляем bot в контекст
        data['bot'] = self.bot
        return await handler(event, data)
    
class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db
        super().__init__()

    async def __call__(self, handler, event: TelegramObject, data: dict):
        # Добавляем объект базы данных в данные хендлера
        data['db'] = self.db
        return await handler(event, data)