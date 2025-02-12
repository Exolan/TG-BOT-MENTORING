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

async def update_vectors(pool, table_name, id_column, text_column, vector_column):
    """ Кодирует текст из БД и обновляет его векторное представление """
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT {id_column}, {text_column} FROM {table_name} WHERE {text_column} IS NOT NULL")
            rows = await cursor.fetchall()

            for row_id, text in rows:
                vector = model.encode(text).tolist()  # Кодируем текст в вектор
                vector_json = json.dumps(vector)  # Преобразуем в JSON

                await cursor.execute(f"UPDATE {table_name} SET {vector_column} = %s WHERE {id_column} = %s", (vector_json, row_id))
                print(f"✅ Обновлён {table_name}: ID {row_id}")

            await conn.commit()

async def main():
    print("⚡ Начинаем кодирование текстов...")

    pool = await aiomysql.create_pool(**DB_CONFIG)

    await update_vectors(pool, "themes", "theme_id", "theme_text", "theme_vector")
    await update_vectors(pool, "subthemes", "subtheme_id", "subtheme_text", "subtheme_vector")

    pool.close()
    await pool.wait_closed()

    print("🎉 Кодирование завершено!")

if __name__ == "__main__":
    asyncio.run(main())