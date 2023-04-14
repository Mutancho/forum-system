from fastapi import APIRouter, Response
from database.models import User
from services import user_service

user_router = APIRouter(prefix='/users')

@user_router.post('/', status_code=201)
def create_user(user: User):
    if user_service.exists(user):
        return Response(status_code= 400, content=f'A User with this username: {user.username} and email: {user.email} already exists!')

    return user_service.create(user)