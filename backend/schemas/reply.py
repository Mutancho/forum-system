from pydantic import BaseModel, constr
from datetime import date

class Reply(BaseModel):
    id: int | None
    content: str
    created_at: date | None
    updated_at: date | None

    @classmethod
    def from_query_result(cls, id, content, created_at, updated_at):
        return cls(id=id, content=content, updated_at=updated_at, created_at=created_at)

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
