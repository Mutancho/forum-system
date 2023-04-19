from pydantic import BaseModel
from datetime import date


class BaseReply(BaseModel):
    id: int | None
    content: str


class ReplyTimeStamps(BaseReply):
    created_at: date
    updated_at: date


class ReplyWithUserAndTopic(ReplyTimeStamps):
    user_id: int
    topic_id: int
