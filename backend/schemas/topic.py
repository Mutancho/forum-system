from pydantic import BaseModel


class BaseTopic(BaseModel):
    id: int
    title: str
    content: str


class TopicWithForeignKeys(BaseTopic):
    user_id: int
    category_id: int
