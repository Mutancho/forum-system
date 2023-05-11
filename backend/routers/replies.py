from fastapi import APIRouter, status, HTTPException, Response, Header
from backend.services import reply_service, category_service, topic_service, user_service
from backend.schemas.reply import BaseReply, Vote, Reply, UpdateReply
from backend.routers.helper_functions import query_filters

router_reply = APIRouter(prefix="/categories/{category_id}/topics/{topic_id}/replies", tags=["Replies"])


@router_reply.get("/{id}")
async def get_reply_by_id(category_id: int, topic_id: int, id: int, Authorization: str = Header()):
    token = Authorization[8:-1]
    if await category_service.category_exists(category_id) is None:
        return Response(status_code=404, content="Category Not Found")
    if await topic_service.get_topic_by_id(topic_id) is None:
        return Response(status_code=404, content="Topic Not Found")
    if not await reply_service.exists_by_id(id):
        return Response(status_code=404, content='Reply Not Found')

    return await reply_service.get_by_id(id)


@router_reply.post('/')
async def create_reply(category_id: int, topic_id: int, reply: Reply, Authorization: str = Header()):
    token = Authorization[8:-1]
    if await category_service.category_exists(category_id) is None:
        return Response(status_code=404, content="Category Not Found")
    if await topic_service.get_topic_by_id(topic_id) is None:
        return Response(status_code=404, content="Topic Not Found")

    return await reply_service.create(reply, topic_id, token)


@router_reply.put('/{id}')
async def update_reply(category_id: int, topic_id: int, id: int, reply: UpdateReply, Authorization: str = Header()):
    token = Authorization[8:-1]
    if await category_service.category_exists(category_id) is None:
        return Response(status_code=404, content="Category Not Found")
    if await topic_service.get_topic_by_id(topic_id) is None:
        return Response(status_code=404, content="Topic Not Found")
    if not await reply_service.exists_by_id(id):
        return Response(status_code=404, content='Reply Not Found')

    return await reply_service.update_reply(id, reply)


@router_reply.delete('/{id}')
async def delete_reply(category_id: int, topic_id: int, id: int, Authorization: str = Header()):
    token = Authorization[8:-1]
    if await category_service.category_exists(category_id) is None:
        return Response(status_code=404, content="Category Not Found")
    if await topic_service.get_topic_by_id(topic_id) is None:
        return Response(status_code=404, content="Topic Not Found")
    if not await reply_service.exists_by_id(id):
        return Response(status_code=404, content='Reply Not Found')
    if await reply_service.is_reply_owner(id, token) or \
            await topic_service.is_topic_owner(topic_id, token) or await user_service.is_admin(token):
        await topic_service.delete_topic_has_best_reply(topic_id)
        await reply_service.delete(id)
        return Response(status_code=204)
    else:
        return Response(status_code=403)


@router_reply.post('/{id}/vote')
async def reply_vote(category_id: int, topic_id: int, id: int, vote: Vote, Authorization: str = Header()):
    token = Authorization[8:-1]
    if await category_service.category_exists(category_id) is None:
        return Response(status_code=404, content="Category Not Found")
    if await topic_service.get_topic_by_id(topic_id) is None:
        return Response(status_code=404, content="Topic Not Found")
    if not await reply_service.exists_by_id(id):
        return Response(status_code=404, content='Reply Not Found')
    if await reply_service.already_voted(id, token):
        return Response(status_code=400, content="You can only vote once per reply!")

    return await reply_service.reply_vote(id, vote, token)


@router_reply.put('/{id}/vote')
async def reply_vote(category_id: int, topic_id: int, id: int, vote: Vote, Authorization: str = Header()):
    token = Authorization[8:-1]
    if await category_service.category_exists(category_id) is None:
        return Response(status_code=404, content="Category Not Found")
    if await topic_service.get_topic_by_id(topic_id) is None:
        return Response(status_code=404, content="Topic Not Found")
    if not await reply_service.exists_by_id(id):
        return Response(status_code=404, content='Reply Not Found')
    if not await reply_service.already_voted(id, token):
        return Response(status_code=400, content="You haven't yet voted for this reply")

    return await reply_service.update_reply_vote(id, vote, token)
