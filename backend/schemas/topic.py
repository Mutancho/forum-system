from pydantic import BaseModel
from datetime import date
from schemas.reply import BaseReply


class BaseTopic(BaseModel):
    id: int | None
    title: str


class TopicWithContent(BaseTopic):
    content: str


class TopicWithBestReply(TopicWithContent):
    best_reply_id: int | None
    locked: bool


class TopicsTimeStamps(BaseTopic):
    created_at: date
    updated_at: date


class TopicWithUserAndCategoryWithContent(TopicWithContent):
    user_id: int | None
    category_id: int | None


class TopicBestReply(BaseModel):
    best_reply_id: int


class TopicWithReplies(BaseModel):
    topic: TopicWithContent
    replies: list[BaseReply]
