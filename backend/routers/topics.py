from fastapi import APIRouter, HTTPException, status
from services.topic_service import create, get_all, lock, unlock
from schemas.topic import TopicWithUserAndCategory, BaseTopic
from routers.helper_functions import query_filters, handle_updates, TOPIC

router_topic = APIRouter(prefix="/categories/{category_id}/topics", tags=["Topics"])


@router_topic.get("/")
def get_all_topics_from_categories(category_id: int, search: str | None = None, sort: str | None = None,
                                   skip: int | None = None, limit: int | None = None):
    data = get_all(category_id)
    return query_filters(data, key="title", search=search, sort=sort, skip=skip, limit=limit)


@router_topic.post("/")
def create_topic(category_id: int, topic: TopicWithUserAndCategory):
    created_topic = create(category_id, topic)
    if created_topic is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create topic")
    return created_topic


@router_topic.put("/lock/{topic_id}")
def lock_category(topic_id: int):
    update_status = lock(topic_id)
    return handle_updates(update_status, TOPIC)


@router_topic.put("/unlock/{topic_id}")
def unlock_category(topic_id: int):
    update_status = unlock(topic_id)
    return handle_updates(update_status, TOPIC)
