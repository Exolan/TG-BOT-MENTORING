import aiomysql
from typing import Any, Dict, List, Optional #Для указания типов

class Database:
    def __init__(self, host: str, port: int, user: str, password: str, db: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        
        self.pool = None
    
    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            autocommit=True
        )
    
    async def disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def execute(self, query: str, params: Optional[tuple] = None) -> int:
        """Выполнение запросов INSERT, UPDATE, DELETE"""
        async with self.pool.acquire() as conn: #Берет соединение из pool
            async with conn.cursor() as cursor: #Создает курсор для выполнения запроса
                await cursor.execute(query, params or ())
                return cursor.rowcount
            
    async def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """Выполнение SELECT одной строки"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor: #DictCursor - курсор, возвращает результат в виде словаря
                await cursor.execute(query, params or ())
                return await cursor.fetchone()
            
    async def fetch_all(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Выполнение SELECT нескольких строк"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params or ())
                return await cursor.fetchall()
    