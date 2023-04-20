from fastapi import APIRouter, Response,Header
from fastapi.security import OAuth2PasswordBearer
from schemas.user import User, EmailLogin, UsernameLogin, Member, RevokeMemberAccess
from services import user_service, category_service
from utils import oauth2

router_user = APIRouter(prefix='/users',tags=['Users'])
@router_user.get('/')
def get_all_users(Authorization:str = Header()):
    token = Authorization[8:-1]
    if not user_service.is_admin(token):
        return Response(status_code=403)
    return user_service.all()
@router_user.get('/{id}')
def get_user_bt_id(id:int , Authorization:str = Header()):
    token = Authorization[8:-1]
    if not user_service.exists_by_id(id):
        return Response(status_code=404)
    if not user_service.is_user_authorized_to_get_delete(token,id):
        return Response(status_code=403)
    return user_service.get_by_id(id)

@router_user.post('/', status_code=201)
def create_user(user: User):
    if user_service.exists_by_username_email(user):
        return Response(status_code= 400, content=f'A User with this username: {user.username} and email: {user.email} already exists!')

    return user_service.create(user)

@router_user.put('/{id}')
def update_user(id: int,user: User,Authorization:str = Header()):
    token = Authorization[8:-1]
    auth_user_id = oauth2.get_current_user(token)
    if not user_service.exists_by_id(id):
        return Response(status_code=404)
    if id != auth_user_id:
        return Response(status_code=403)
    if user_service.exists_by_username_email(user):
        return Response(status_code= 400, content=f'A User with this username: {user.username} and email: {user.email} already exists!')

    return user_service.update_query(id,user)

@router_user.delete('/{id}')
def delete_user(id:int,Authorization:str = Header()):
    token = Authorization[8:-1]
    if not user_service.exists_by_id(id):
        return Response(status_code=404)
    if not user_service.is_user_authorized_to_get_delete(token,id):
        return Response(status_code=403)
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

@router_user.post('/give_access')
def give_access(member_access: Member,Authorization:str = Header()):
    token = Authorization[8:-1]
    if not user_service.is_admin(token):
        return Response(status_code=403)
    if not user_service.exists_by_id(member_access.user_id):
        return Response(status_code=400,content=f'User with id: {member_access.user_id} does not exist!')
    if category_service.category_exists(member_access.category_id) == None:
        return Response(status_code=400,content=f'Category with id: {member_access.category_id} does not exist!')

    user_service.give_access(member_access)
    return Response(status_code=200)

@router_user.post('/revoke_access')
def revoke_access(member_access: RevokeMemberAccess,Authorization:str = Header()):
    token = Authorization[8:-1]
    if not user_service.is_admin(token):
        return Response(status_code=403)
    if not user_service.exists_by_id(member_access.user_id):
        return Response(status_code=400,content=f'User with id: {member_access.user_id} does not exist!')
    if not user_service.user_has_permissions_for_category(member_access.user_id,member_access.category_id):
        return Response(status_code=404)

    user_service.revoke_access(member_access)
    return Response(status_code=200)