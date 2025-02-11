import json
import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from aiogram import Router, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from database import Database
from keyboards import back_buttons

search_router = Router()

# Загружаем модель для векторизации текста
model = SentenceTransformer("all-MiniLM-L6-v2")

@search_router.message()
async def search_info(message: Message, bot: Bot, db: Database):
    search_text = message.text.strip()

    if len(search_text) < 5:
        await message.answer("Я вас не понимаю. Напишите более подробно", reply_markup=back_buttons())
        return

    # try:
    # Преобразуем запрос в вектор
    query_vector = model.encode(search_text).tolist()

    # Запрашиваем темы с векторными представлениями
    query_themes = "SELECT theme_id, theme_name, theme_vector FROM themes WHERE theme_vector IS NOT NULL"
    query_subthemes = "SELECT subtheme_id, subtheme_name, subtheme_vector FROM subthemes WHERE subtheme_vector IS NOT NULL"


    themes = await db.fetch_all(query_themes)
    subthemes = await db.fetch_all(query_subthemes)

    if not themes and not subthemes:
        await message.answer("Я ничего не нашел", reply_markup=back_buttons())
        return

        # Вычисляем косинусное сходство запроса с каждой темой
    similarities = []

    for theme in themes:
        theme_vector = json.loads(theme["theme_vector"])  # Декодируем JSON в массив
        similarity = 1 - cosine(query_vector, theme_vector)  # Косинусное сходство

        if similarity > 0.5:
            similarities.append((theme["theme_name"], similarity, f'select_theme_{theme["theme_id"]}'))  # Добавляем в список

    for subtheme in subthemes:
        subtheme_vector = json.loads(subtheme["subtheme_vector"])  # Декодируем JSON в массив
        similarity = 1 - cosine(query_vector, subtheme_vector)  # Косинусное сходство

        if similarity > 0.5:
            similarities.append((subtheme["subtheme_name"], similarity, f'select_subtheme_{subtheme["subtheme_id"]}'))  # Добавляем в список

    if len(similarities) == 0:
        await message.answer("Я ничего не нашел", reply_markup=back_buttons())
        return
    
    # Сортируем темы по убыванию схожести
    best_matches = sorted(similarities, key=lambda x: x[1], reverse=True)

    buttons = []

    for name, sim, call in best_matches:
        print(name, call)
        buttons.append([InlineKeyboardButton(text=name, callback_data=call)])

    buttons.append([InlineKeyboardButton(text="Главное меню", callback_data="menu")])

    await message.answer("🔎 Вот что я нашел", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

    # except Exception as e:
    #     await message.answer("Произошла ошибка. Попробуйте позже", reply_markup=back_buttons())
    #     print(f"Ошибка поиска: {e}")