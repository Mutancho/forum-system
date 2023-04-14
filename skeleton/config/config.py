import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


settings = Settings()
