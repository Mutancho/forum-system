from datetime import date
from pydantic import BaseModel


class Message(BaseModel):
    id: int | None
    content: str
    created_at: date | None
    sender_id: int | None
    receiver_id: int
