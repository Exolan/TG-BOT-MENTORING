from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import MenuState
from keyboards import back_buttons
from database import Database
from utils import create_file

subtheme_router = Router()

@subtheme_router.callback_query(lambda call: call.data.startswith("select_subtheme_"))
async def select_theme(call: CallbackQuery, state: FSMContext, db: Database):
    await call.message.delete()

    data = await state.get_data()
    search_text = data.get("search_text")

    if search_text:
        pervios_callback = "search_results"
    else:
        await state.set_state(MenuState.select_theme)
        data = await state.get_data()
        pervios_callback = "select_theme_" + data.get("select_theme")

    subtheme_id = call.data.split("_")[2]

    subtheme = await db.fetch_one(f"SELECT * FROM subthemes WHERE subtheme_id = {subtheme_id}")
    
    subtheme_name = subtheme["subtheme_name"]
    subtheme_text = subtheme["subtheme_text"]
    subtheme_file_url = subtheme["subtheme_file_url"]

    if subtheme_file_url:
        file = await create_file(subtheme_file_url)

        if not file and not subtheme_text:
            await call.message.answer("⚠ Эта тема еще не загружена. Повторите попытку позже", reply_markup=back_buttons(pervios_callback))
            return
        
        await call.message.answer_document(file, caption=f"<b>{subtheme_name}</b>\n\n{subtheme_text[:800]}", reply_markup=back_buttons(pervios_callback))

        return
    
    if not subtheme_text:
        await call.message.answer("⚠ Эта тема еще не загружена. Повторите попытку позже", reply_markup=back_buttons(pervios_callback))
        return
    
    await call.message.answer(text=f"<b>{subtheme_name}</b>\n\n{subtheme_text[:4000]}", reply_markup=back_buttons(pervios_callback))

    