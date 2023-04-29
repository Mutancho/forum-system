from fastapi import APIRouter, Header
from services.topic_service import create, lock, unlock, get_topic_by_id_with_replies, delete, update, set_best_reply, \
    get_all
from schemas.topic import TopicWithUserAndCategoryWithContent, TopicWithContent, TopicBestReply
from routers.helper_functions import http_validations, Constants as C, query_filters
from utils.oauth2 import get_current_user

router_topic = APIRouter(prefix="/categories/{category_id}/topics", tags=["Topics"])
router_all_topics = APIRouter(tags=["Topics"])


@router_all_topics.get("/topics")
async def get_all_topics(search: str | None = None, sort: str | None = None,
                         skip: int | None = None, limit: int | None = None):
    data = await get_all()
    filtered_data = query_filters(data, key="title", search=search, sort=sort, skip=skip, limit=limit)
    return filtered_data


@router_topic.get("/{topic_id}")
async def get_by_id_with_replies(category_id: int, topic_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    topics_with_replies = await get_topic_by_id_with_replies(token, category_id, topic_id)
    return http_validations(topics_with_replies, C.TOPIC)


@router_topic.post("/")
async def create_topic(category_id: int, topic: TopicWithUserAndCategoryWithContent,
                 auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    created_topic = await create(token, category_id, topic)
    topic.user_id = get_current_user(token)
    return http_validations(created_topic, C.CATEGORY)


@router_topic.delete("/{topic_id}")
async def delete_topic(topic_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    removed_topic = await delete(token, topic_id)
    return http_validations(removed_topic, C.TOPIC)


@router_topic.put("/{topic_id}")
async def topic_update(topic_id: int, topic: TopicWithContent, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    updated_topic = await update(token, topic_id, topic)
    return http_validations(updated_topic, C.TOPIC)


@router_topic.put("/best_reply/{topic_id}")
async def best_reply(topic_id: int, topic: TopicBestReply, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    updated_topic = await set_best_reply(token, topic_id, topic)
    return http_validations(updated_topic, C.TOPIC)


@router_topic.put("/lock/{topic_id}")
async def lock_topic(topic_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    update_status = await lock(token, topic_id)
    return http_validations(update_status, C.TOPIC)


@router_topic.put("/unlock/{topic_id}")
async def unlock_topic(topic_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    update_status = await unlock(token, topic_id)
    return http_validations(update_status, C.TOPIC)
