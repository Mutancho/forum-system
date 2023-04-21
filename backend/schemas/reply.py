from pydantic import BaseModel, constr
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

class Vote(BaseModel):
    vote: constr(regex='(?i)^(upvote|downvote)$')
