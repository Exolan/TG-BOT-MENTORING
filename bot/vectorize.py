import json
import asyncio
import aiomysql
from sentence_transformers import SentenceTransformer
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

# Загружаем модель
model = SentenceTransformer("all-MiniLM-L6-v2")

# Подключение к БД
DB_CONFIG = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "db": DB_NAME,
}

async def update_vectors(pool, table_name, id_column, name_column, text_column, vector_column, exclude_names=None):
    """ Кодирует объединённый текст (name + text) из БД и обновляет его векторное представление """
    exclude_names = exclude_names or []
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            # Формируем SQL-запрос с исключением определённых имён
            query = f"SELECT {id_column}, {name_column}, {text_column} FROM {table_name} WHERE {text_column} IS NOT NULL"
            if exclude_names:
                placeholders = ', '.join(['%s'] * len(exclude_names))
                query += f" AND {name_column} NOT IN ({placeholders})"

            await cursor.execute(query, exclude_names)
            rows = await cursor.fetchall()

            for row_id, name, text in rows:
                full_text = f"{name}. {text}" if name else text  # Объединяем имя и текст
                vector = model.encode(full_text).tolist()  # Кодируем текст в вектор
                vector_json = json.dumps(vector)  # Преобразуем в JSON

                await cursor.execute(
                    f"UPDATE {table_name} SET {vector_column} = %s WHERE {id_column} = %s",
                    (vector_json, row_id)
                )
                print(f"✅ Обновлён {table_name}: ID {row_id}")

            await conn.commit()

async def main():
    print("⚡ Начинаем кодирование текстов...")

    pool = await aiomysql.create_pool(**DB_CONFIG)

    # Исключаем определённые темы
    exclude_themes = ["Полезная литература", "Электронные курсы для наставников", "Первые шаги"]

    await update_vectors(pool, "themes", "theme_id", "theme_name", "theme_text", "theme_vector", exclude_names=exclude_themes)
    await update_vectors(pool, "subthemes", "subtheme_id", "subtheme_name", "subtheme_text", "subtheme_vector")

    pool.close()
    await pool.wait_closed()

    print("🎉 Кодирование завершено!")

if __name__ == "__main__":
    asyncio.run(main())
