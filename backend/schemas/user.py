from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    id: int | None
    username: str
    email: str
    password: str
    role: str
    created_at: date | None