from pydantic import BaseModel
from datetime import date
from schemas.reply import BaseReply


class BaseTopic(BaseModel):
    id: int | None
    title: str


class TopicWithContent(BaseTopic):
    content: str


class TopicsTimeStamps(BaseTopic):
    created_at: date
    updated_at: date


class TopicWithUserAndCategoryWithContent(TopicWithContent):
    user_id: int | None
    category_id: int | None


# class TopicsOut(TopicsTimeStamps, TopicWithUserAndCategory):
#     locked: bool
#     best_reply_id: str | None

class TopicBestReply(BaseModel):
    best_reply_id: int


class TopicWithReplies(BaseModel):
    topic: TopicWithContent
    replies: list[BaseReply]
