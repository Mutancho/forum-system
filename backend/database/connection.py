from mariadb import connect, Error
from mariadb.connections import Connection
from config.config import settings


def get_connection() -> Connection:
    try:
        connection = connect(
            user=settings.database_username,
            password=settings.database_password,
            host=settings.database_hostname,
            port=int(settings.database_port),
            database=settings.database_name
        )
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        raise
