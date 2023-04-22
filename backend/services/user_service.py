import datetime
from utils import oauth2
from schemas.user import User, EmailLogin, UsernameLogin, Member, RevokeMemberAccess, UpdateUser
from database.database_queries import insert_query, read_query, update_query
import bcrypt


def all():
    data = read_query('''SELECT id, username, email, role, created_at FROM users''')

    return (User.from_query_result(*u) for u in data)

def create(user: User):

    hashed = _hash_password(user.password)

    generate_id = insert_query('''INSERT INTO users(username,email,password,role) VALUES (?,?,?,?)''',
                               (user.username, user.email, hashed, user.role))
    user.id = generate_id
    user.created_at = read_query('''SELECT created_at FROM users WHERE id = ?''',(generate_id,))[0][0]
    return user

def update(id: int,user: UpdateUser):
    password = _hash_password(user.password)
    update_query('''UPDATE users SET username = ?, email = ? , password = ? WHERE id = ?  ''',
                 (user.username,user.email,password,id))

    return user

def check_unique_update_email_password(id: int,user: UpdateUser):
    data = read_query('''SELECT username,email FROM users WHERE (username = ? OR email = ?) AND id <> ?''',
                      (user.username, user.email,id))

    return len(data) > 0


def delete(id:int):
    data = update_query('''DELETE FROM users WHERE id = ?''',(id,))

def get_by_id(id: int):
    data = read_query('''SELECT id, username, email, role, created_at FROM users WHERE id = ?''',
                      (id,))
    return User.from_query_result(*data[0])
def exists_by_username_email(user: User):
    data = read_query('''SELECT username,email FROM users WHERE username =? or email = ?''',
                      (user.username, user.email))

    return len(data) > 0

def exists_by_id(id:int):
    data = read_query('''SELECT id FROM users WHERE id = ?''',
                      (id,))

    return len(data) > 0

def login(credentials: EmailLogin | UsernameLogin):
    if isinstance(credentials, EmailLogin):
        data = read_query('''SELECT id,username,email,password FROM users WHERE email = ?''',
                          (credentials.email,))
    if isinstance(credentials, UsernameLogin):
        data = read_query('''SELECT id,username,email,password FROM users WHERE username = ?''',
                          (credentials.username,))
    id = data[0][0]
    username = data[0][1]
    email = data[0][2]
    password=credentials.password

    return oauth2.create_access_token(id)

def give_access(member_access: Member):
    read_access = int(member_access.read_access)
    write_access = int(member_access.write_access)
    if user_has_permissions_for_category(member_access.user_id,member_access.category_id):
        update_query('''UPDATE categorymembers SET read_access = ?,write_access = ?  Where user_id = ? and category_id = ?''',
                     (read_access,write_access,member_access.user_id,member_access.category_id))
    else:
        insert_query('''INSERT INTO categorymembers(user_id,category_id,read_access,write_access) VALUES (?,?,?,?)''',
                     (member_access.user_id,member_access.category_id,read_access,write_access))

def revoke_access(member_access: RevokeMemberAccess):
    read_access = 0
    write_access = 0
    update_query(
        '''UPDATE categorymembers SET read_access = ?,write_access = ?  Where user_id = ? and category_id = ?''',
        (read_access, write_access, member_access.user_id, member_access.category_id))

def user_has_permissions_for_category(user_id: int,category_id: int):
    data = read_query('''SELECT * FROM categorymembers WHERE user_id = ? and category_id = ?''',(user_id,category_id))

    return len(data)>0

def verify_credentials(credentials: EmailLogin | UsernameLogin):
    if isinstance(credentials,EmailLogin):
        data = read_query('''SELECT username,email,password FROM users WHERE email = ?''',
                          (credentials.email,))
    if isinstance(credentials,UsernameLogin):
        data = read_query('''SELECT username,email,password FROM users WHERE username = ?''',
                          (credentials.username,))
    return len(data)>0
def is_user_authorized_to_get_delete(token:str,id:int):
    user_id = oauth2.get_current_user(token)
    data = read_query('''SELECT role FROM users WHERE id = ?''',
               (user_id,))
    role = data[0][0]
    return user_id==id or role.lower()=='admin'

def is_admin(token:str):
    user_id = oauth2.get_current_user(token)
    data = read_query('''SELECT role FROM users WHERE id = ?''',
                      (user_id,))
    role = data[0][0]
    return role.lower() == 'admin'

def _hash_password(password: str):
    salt = b'$2b$12$V0NmXBYEU2o0x3nbxOPouu'
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def valid_password(credentials: EmailLogin | UsernameLogin):
    hashed = _hash_password(credentials.password)
    if isinstance(credentials,EmailLogin):
        actual_password = read_query('''SELECT password FROM users WHERE  email = ?''',(credentials.email,))[0][0]
    if isinstance(credentials,UsernameLogin):
        actual_password = read_query('''SELECT password FROM users WHERE username = ? ''',(credentials.username,))[0][0]

    return hashed.decode() == actual_password