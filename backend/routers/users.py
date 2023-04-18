from fastapi import APIRouter, Response,Header
from fastapi.security import OAuth2PasswordBearer
from schemas.user import User,EmailLogin,UsernameLogin
from services import user_service
from utils import oauth2

router_user = APIRouter(prefix='/users',tags=['Users'])

@router_user.post('/', status_code=201)
def create_user(user: User):
    if user_service.exists_by_username_email(user):
        return Response(status_code= 400, content=f'A User with this username: {user.username} and email: {user.email} already exists!')

    return user_service.create(user)

@router_user.delete('/{id}')
def delete_user(id:int,Authorization:str = Header()):
    token = Authorization[8:-1]
    if not user_service.exists_by_id(id):
        return Response(status_code=404)
    if not user_service.is_user_authorized_to_delete(token,id):
        return Response(status_code=401)
    user_service.delete(id)
    return Response(status_code=204)

@router_user.post('/login')
def login(credentials: EmailLogin | UsernameLogin):

    if not user_service.verify_credentials(credentials):
        if isinstance(credentials, EmailLogin):
            return Response(status_code=401,content=f"User with this email: {credentials.email} doesn't exist!")
        if isinstance(credentials, UsernameLogin):
            return Response(status_code=401,content=f"User with this username: {credentials.username} doesn't exist!")
    if not user_service.valid_password(credentials):
        return Response(status_code=401,content='Invalid password.')

    return user_service.login(credentials)

