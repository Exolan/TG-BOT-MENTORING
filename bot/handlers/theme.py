from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import back_buttons, select_buttons
from database import Database
from utils import create_file
from states import MenuState

theme_router = Router()

@theme_router.callback_query(lambda call: call.data.startswith("select_theme_"))
async def select_theme(call: CallbackQuery, state: FSMContext, db: Database):
    await call.message.delete()

    theme_id = call.data.split("_")[2]

    data = await state.get_data()
    search_text = data.get("search_text")

    if search_text:
        pervios_callback = "search_results"
    else:
        await state.set_state(MenuState.select_category)

        category = data.get('select_category')

        if category:
            await state.update_data(select_theme = theme_id)
            pervios_callback = "select_category_" + category
        else:
            pervios_callback = None


    theme = await db.fetch_one(f"SELECT * FROM themes WHERE theme_id = {theme_id}")

    subtheme = await db.fetch_all(f"SELECT * FROM subthemes WHERE theme_id = {theme_id}")
    
    theme_name = theme["theme_name"]
    theme_text = theme["theme_text"]
    theme_file_url = theme["theme_file_url"]

    if subtheme:
        await call.message.answer("Выберите подтему", reply_markup=select_buttons(subtheme, False, pervios_callback))
        return

    if theme_file_url:
        file = await create_file(theme_file_url)

        if not file or not theme_text:
            await call.message.answer("Произошла ошибка. Повторите попытку позже", reply_markup=back_buttons(pervios_callback))
            return
        
        await call.message.answer_document(file, caption=f"<b>{theme_name}</b>\n\n{f'{theme_text[:800]}...'}\n\n<b>Подробнее в прикрепленом файле</b>", reply_markup=back_buttons(pervios_callback))
        return

    if not theme_text:
        await call.message.answer("Произошла ошибка. Повторите попытку позже", reply_markup=back_buttons(pervios_callback))
        return
    
    await call.message.answer(text=f"<b>{theme_name}</b>\n\n{theme_text[:4000]}", reply_markup=back_buttons(pervios_callback))

