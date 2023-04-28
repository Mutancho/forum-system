from mariadb import connect, Error
from mariadb.connections import Connection
from config.config import settings
import time


def get_connection(max_retries=5, delay=5) -> Connection:
    for _ in range(max_retries):
        try:
            connection = connect(
                user=settings.database_username,
                password=settings.database_password,
                host=settings.database_hostname,
                port=settings.database_port,
                database=settings.database_name
            )
            return connection
        except Error as e:
            print(f"Error connecting to the database: {e}")
            time.sleep(delay)
    raise Exception("Could not connect to the database after max retries")

