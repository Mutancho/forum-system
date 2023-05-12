from fastapi import APIRouter, Response, Header
from schemas.message import Message
from services import message_service, user_service
from utils import oauth2

router_message = APIRouter(prefix='/messages', tags=['Messages'])


@router_message.post('/')
async def create_message(message: Message, Authorization: str = Header()):
    token = Authorization[8:-1]
    message.sender_id = oauth2.get_current_user(token)
    if await user_service.exists_by_id(message.sender_id) and await user_service.exists_by_id(message.receiver_id):
        return await message_service.create(message)

    return Response(status_code=400, content="Sender or Receiver id doesn't match an existing user")


@router_message.get('/conversations')
async def get_conversations(Authorization: str = Header()):
    token = Authorization[8:-1]
    return await message_service.get_all_my_conversations(token)


@router_message.get('/conversations/{id}')
async def get_conversations_with(id: int, Authorization: str = Header()):
    token = Authorization[8:-1]
    if not await user_service.exists_by_id(id):
        return Response(status_code=404)

    return await message_service.get_all_my_conversations_with(token, id)
