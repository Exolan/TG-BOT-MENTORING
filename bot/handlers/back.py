from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import main_keyboard
from database import Database

menu_router = Router()

@menu_router.callback_query(lambda call: call.data.startswith("menu"))
async def back_command(call: CallbackQuery, state: FSMContext, db: Database):
    await state.clear()
    
    await call.message.delete()
    await call.message.answer("🏃 Вы вернулись назад", reply_markup=await main_keyboard(db))