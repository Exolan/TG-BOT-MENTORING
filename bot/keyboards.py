from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import Database

async def main_keyboard(db: Database):
    categories = await db.fetch_all('SELECT * FROM categories')

    buttons = []

    if categories:
        for category in categories:
            category_id = category['category_id']
            category_text = f"📂 {category['category_name']}"

            themes = await db.fetch_all(f"SELECT * FROM themes WHERE category_id = {category_id}")

            callback = f'select_category_{category_id}'

            if len(themes) == 1:
                callback = f'select_theme_{themes[0]["theme_id"]}'

            buttons.append([InlineKeyboardButton(text=category_text, callback_data=callback)])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_buttons(callback_data: str = None):
    buttons = []

    if callback_data:
        buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=callback_data))

    buttons.append(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])

def select_buttons(list: list, isTheme: bool, pervios_callback: str = None):
    buttons = []

    if list:
        if isTheme:
            for element in list:
                element_id = element['theme_id']
                element_name = f"📌 {element['theme_name']}"

                buttons.append([InlineKeyboardButton(text=element_name, callback_data=f'select_theme_{element_id}')])
        else:
            for element in list:
                element_id = element['subtheme_id']
                element_name = f"🔹 {element['subtheme_name']}"

                buttons.append([InlineKeyboardButton(text=element_name, callback_data=f'select_subtheme_{element_id}')])

    back_buttons = []

    if pervios_callback:
        back_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=pervios_callback))
    back_buttons.append(InlineKeyboardButton(text="🏠 Главное меню", callback_data='menu'))

    buttons.append(back_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)