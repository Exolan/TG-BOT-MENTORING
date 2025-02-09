import json
import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from aiogram import Router, Bot
from aiogram.types import Message
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

    try:
        # Преобразуем запрос в вектор
        query_vector = model.encode(search_text).tolist()

        # Запрашиваем темы с векторными представлениями
        query = "SELECT theme_id, theme_name, theme_vector FROM themes WHERE theme_vector IS NOT NULL"
        themes = await db.fetch_all(query)

        if not themes:
            await message.answer("Я ничего не нашел", reply_markup=back_buttons())
            return

         # Вычисляем косинусное сходство запроса с каждой темой
        similarities = []
        for theme in themes:
            theme_vector = json.loads(theme["theme_vector"])  # Декодируем JSON в массив
            similarity = 1 - cosine(query_vector, theme_vector)  # Косинусное сходство

            similarities.append((theme["theme_name"], similarity))  # Добавляем в список

        # Сортируем темы по убыванию схожести
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Берем топ-3 самых похожих темы
        top_n = 3
        best_matches = similarities[:top_n]

        # Формируем сообщение с результатами
        response = "🔎 Вот что я нашел:\n\n"
        for name, sim in best_matches:
            response += f"✅ <b>{name}</b> ({sim:.2%} совпадение)\n"

        await message.answer(response, parse_mode="HTML")

    except Exception as e:
        await message.answer("Произошла ошибка. Попробуйте позже", reply_markup=back_buttons())
        print(f"Ошибка поиска: {e}")