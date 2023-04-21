from fastapi import APIRouter, status, HTTPException,Response,Header

from services import reply_service, category_service, topic_service
from services.reply_service import get_all
from schemas.reply import BaseReply, Vote, Reply
from routers.helper_functions import query_filters

router_reply = APIRouter(prefix="/categories/{category_id}/topics/{topic_id}/replies", tags=["Replies"])

@router_reply.get("/{id}")
def get_reply_by_id(category_id: int,topic_id: int,id: int,Authorization:str = Header()):
    token = Authorization[8:-1]
    if category_service.category_exists(category_id) == None:
        return Response(status_code=404, content="Category Not Found")
    if topic_service._get_topic_by_id(topic_id) == None:
        return Response(status_code=404, content="Topic Not Found")
    if not reply_service.exists_by_id(id):
        return Response(status_code=404, content='Reply Not Found')

    return reply_service.get_by_id(id)

@router_reply.post('/')
def create_reply(category_id: int,topic_id: int,reply: Reply,Authorization:str = Header()):
    token = Authorization[8:-1]
    if category_service.category_exists(category_id) == None:
        return Response(status_code=404, content="Category Not Found")
    if topic_service._get_topic_by_id(topic_id) == None:
        return Response(status_code=404, content="Topic Not Found")

    return reply_service.create(reply,topic_id,token)



@router_reply.get("/")
def get_all_replies_from_topic(topic_id: int, search: str | None = None, sort: str | None = None,
                               skip: int | None = None, limit: int | None = None):
    # todo: could sort by votes
    data = get_all(topic_id)
    return query_filters(data, key="content", search=search, sort=sort, skip=skip, limit=limit)

@router_reply.post('/{id}/vote')
def reply_vote(category_id: int,topic_id: int,id: int,vote: Vote,Authorization:str = Header()):
    token = Authorization[8:-1]
    if category_service.category_exists(category_id) == None:
        return Response(status_code=404, content="Category Not Found")
    if topic_service._get_topic_by_id(topic_id) == None:
        return Response(status_code=404, content="Topic Not Found")
    if not reply_service.exists_by_id(id):
        return Response(status_code=404,content='Reply Not Found')
    if reply_service.already_voted(id,token):
        return Response(status_code=400,content="You can only vote once per reply!")

    return reply_service.reply_vote(id,vote,token)


@router_reply.put('/{id}/vote')
def reply_vote(category_id: int,topic_id: int,id: int,vote: Vote,Authorization:str = Header()):
    token = Authorization[8:-1]
    if category_service.category_exists(category_id) == None:
        return Response(status_code=404, content="Category Not Found")
    if topic_service._get_topic_by_id(topic_id) == None:
        return Response(status_code=404, content="Topic Not Found")
    if not reply_service.exists_by_id(id):
        return Response(status_code=404,content='Reply Not Found')
    if not reply_service.already_voted(id, token):
        return Response(status_code=400, content="You haven't yet voted for this reply")

    return reply_service.update_reply_vote(id,vote,token)