from mariadb import connect
from mariadb.connections import Connection
from skeleton.config.config import settings


def _get_connection() -> Connection:
    return connect(
        user=settings.database_username,
        password=settings.database_password,
        host=settings.database_hostname,
        port=int(settings.database_port),
        database=settings.database_name
    )


def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount

