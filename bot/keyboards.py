from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
from database import Database

async def main_keyboard(db: Database):
    categories = await db.fetch_all('SELECT * FROM categories')

    buttons = []

    if categories:
        for category in categories:
            category_id = category['category_id']
            category_text = category['category_name']

            buttons.append([InlineKeyboardButton(text=category_text, callback_data=f'select_category_{category_id}')])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_button():
    button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data='back')]])
    return button

def select_theme_buttons(themes):
    buttons = []

    if themes:
        for theme in themes:
            theme_id = theme['theme_id']
            theme_name = theme['theme_name']

            buttons.append([InlineKeyboardButton(text=theme_name, callback_data=f'select_theme_{theme_id}')])
    
    buttons.append([InlineKeyboardButton(text="Назад", callback_data='back')])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)