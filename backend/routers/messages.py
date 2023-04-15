from fastapi import APIRouter, Response
from schemas.message import Message
from services import message_service,user_service

router_message = APIRouter(prefix='/messages',tags=['Messages'])

@router_message.post('/')
def create_message(message: Message):
    if user_service.exists_by_id(message.sender_id) and user_service.exists_by_id(message.reciever_id):
        return message_service.create(message)

    return Response(status_code=400,content="Sender or Receiver id doesn't match an existing user")



@router_message.get('/conversations/{id}')#За сега взима id след това като има auth user през неговото id ще връща хората с който е говорил
def get_conversations(id: int):

    return message_service.get_all_my_conversations(id)

@router_message.get('/conversation/{id}')#Взима id за receiver
def get_conversations_with(id: int):
    if not user_service.exists_by_id(id):
        return Response(status_code=404)
    auth_user_id = 1
    return message_service.get_all_my_conversations_with(auth_user_id,id)

