from fastapi import APIRouter, Response
from schemas.user import User
from services import user_service

router_user = APIRouter(prefix='/users',tags=['Users'])

@router_user.post('/', status_code=201)
def create_user(user: User):
    if user_service.exists_by_username_email(user):
        return Response(status_code= 400, content=f'A User with this username: {user.username} and email: {user.email} already exists!')

    return user_service.create(user)

@router_user.delete('/{id}')
def delete_user(id:int):
    if not user_service.exists_by_id(id):
        return Response(status_code=404)
    user_service.delete(id)
    return Response(status_code=204)
