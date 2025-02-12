from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import back_buttons, select_buttons
from database import Database
from states import MenuState

category_router = Router()

@category_router.callback_query(lambda call: call.data.startswith("select_category_"))
async def select_category(call: CallbackQuery, db: Database, state: FSMContext,):
    await call.message.delete()
    await state.set_state(MenuState.select_category)
    await state.clear()

    callback_data = call.data

    category_id = callback_data.split("_")[2]

    await state.update_data(select_category = category_id)

    try:
        themes = await db.fetch_all(f"SELECT * FROM themes WHERE category_id = {category_id}")

        if themes:
            await call.message.answer("Выберите тему", reply_markup=select_buttons(list=themes, isTheme=True))
        else:
            await call.message.answer(f"В этой категории пока нет тем", reply_markup=back_buttons())
    
    except ValueError as e:
        await call.message.answer(f"Ошибка обработки данных. Попробуйте позже", reply_markup=back_buttons())
        print(f"Ошибка обработки данных: {e}")

    except Exception as e:
        await call.message.answer(f"Произошла ошибка. Попробуйте позже", reply_markup=back_buttons())
        print(f"Ошибка: {e}")