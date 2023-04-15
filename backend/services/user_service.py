from schemas.user import User
from database.database_queries import insert_query, read_query, update_query
import bcrypt


def create(user: User):
    salt = b'$2b$12$V0NmXBYEU2o0x3nbxOPouu'
    hashed = bcrypt.hashpw((user.password).encode('utf-8'), salt)

    generate_id = insert_query('''INSERT INTO user(username,email,password,role) VALUES (?,?,?,?)''',
                               (user.username, user.email, hashed, user.role))
    user.id = generate_id
    return user


def exists_by_username_email(user: User):
    data = read_query('''SELECT username,email FROM user WHERE username =? and email = ?''',
                      (user.username, user.email))

    return len(data) > 0

def exists_by_id(id:int):
    data = read_query('''SELECT * FROM user WHERE id = ?''',
                      (id,))

    return len(data) > 0