from database.connection import get_connection


async def read_query(sql: str, sql_params=()) -> list:
    pool = await get_connection()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql, sql_params)
            result = await cur.fetchall()
    return result


async def insert_query(sql: str, sql_params=()) -> int:
    async with get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, sql_params)
            await conn.commit()
            return cursor.lastrowid


async def update_query(sql: str, sql_params=()) -> bool:
    async with get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, sql_params)
            await conn.commit()
            return cursor.rowcount
