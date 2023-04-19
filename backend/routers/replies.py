from fastapi import APIRouter, status, HTTPException
from services.reply_service import get_all
from schemas.reply import BaseReply
from routers.helper_functions import handle_updates, query_filters, REPLY

router_reply = APIRouter(prefix="/categories/{category_id}/topics/{topic_id}/replies", tags=["Replies"])


@router_reply.get("/")
def get_all_replies_from_topic(topic_id: int, search: str | None = None, sort: str | None = None,
                               skip: int | None = None, limit: int | None = None):
    # todo: could sort by votes
    data = get_all(topic_id)
    return query_filters(data, key="content", search=search, sort=sort, skip=skip, limit=limit)