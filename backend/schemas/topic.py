from pydantic import BaseModel
from datetime import date
from schemas.reply import BaseReply


class BaseTopic(BaseModel):
    id: int | None
    title: str
    content: str


class TopicsTimeStamps(BaseModel):
    created_at: date
    updated_at: date


class TopicWithUserAndCategory(BaseTopic):
    user_id: int | None
    category_id: int


class TopicsOut(TopicsTimeStamps, TopicWithUserAndCategory):
    locked: bool
    best_reply: str | None


class TopicWithReplies(BaseModel):
    topic: BaseTopic
    replies: list[BaseReply]
