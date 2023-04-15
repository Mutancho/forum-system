import datetime

from schemas.user import User
from database.database_queries import insert_query, read_query, update_query
import bcrypt


def create(user: User):
    salt = b'$2b$12$V0NmXBYEU2o0x3nbxOPouu'
    hashed = bcrypt.hashpw((user.password).encode('utf-8'), salt)

    generate_id = insert_query('''INSERT INTO user(username,email,password,role) VALUES (?,?,?,?)''',
                               (user.username, user.email, hashed, user.role))
    user.id = generate_id
    user.created_at = read_query('''SELECT created_at FROM user WHERE id = ?''',(generate_id,))
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