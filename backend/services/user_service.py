import datetime
from fastapi import Response
from schemas.user import User,EmailLogin,UsernameLogin
from database.database_queries import insert_query, read_query, update_query
import bcrypt



def create(user: User):

    hashed = _hash_password(user.password)

    generate_id = insert_query('''INSERT INTO user(username,email,password,role) VALUES (?,?,?,?)''',
                               (user.username, user.email, hashed, user.role))
    user.id = generate_id
    user.created_at = read_query('''SELECT created_at FROM user WHERE id = ?''',(generate_id,))[0][0]
    return user

def delete(id:int):
    data = update_query('''DELETE FROM user WHERE id = ?''',(id,))


def exists_by_username_email(user: User):
    data = read_query('''SELECT username,email FROM user WHERE username =? and email = ?''',
                      (user.username, user.email))

    return len(data) > 0

def exists_by_id(id:int):
    data = read_query('''SELECT id FROM user WHERE id = ?''',
                      (id,))

    return len(data) > 0

def email_login(credentials:EmailLogin):
    data = read_query('''SELECT username,email,password FROM user WHERE email = ?''',
                      (credentials.email,))
    if len(data) == 0:
        return Response(status_code=400,content=f"User with this email: {credentials.email} doesn't exist!")
    username = data[0][0]
    email = data[0][1]
    password=credentials.password
    if not valid_password(username,email,password):
        return Response(status_code=400,content='Invalid password.')
    return Response(status_code=200)
def username_login(credentials: UsernameLogin):
    data = read_query('''SELECT username,email,password FROM user WHERE username = ?''',
                      (credentials.username,))
    if len(data) == 0:
        return Response(status_code=400,content=f"User with this username: {credentials.username} doesn't exist!")
    username = data[0][0]
    email = data[0][1]
    password=credentials.password
    if not valid_password(username,email,password):
        return Response(status_code=400,content='Invalid password.')
    return Response(status_code=200)

def _hash_password(password: str):
    salt = b'$2b$12$V0NmXBYEU2o0x3nbxOPouu'
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def valid_password(username: str,email: str,password: str):
    hashed = _hash_password(password)
    actual_password = read_query('''SELECT password FROM user WHERE username = ? and email = ?''',(username,email))[0][0]

    return hashed.decode() == actual_password