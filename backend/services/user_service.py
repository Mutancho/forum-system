from utils import oauth2
from schemas.user import User, EmailLogin, UsernameLogin, Member, RevokeMemberAccess, UpdateUser
from database.database_queries import insert_query, read_query, update_query
from utils.passwords import hash_password, verify_password


async def all():
    data = await read_query('''SELECT id, username, email, role, created_at FROM users''')

    return (User.from_query_result(*u) for u in data)


async def create(user: User):
    hashed = await hash_password(user.password)

    generate_id = await insert_query('''INSERT INTO users(username,email,password,role) VALUES (%s,%s,%s,%s)''',
                                     (user.username, user.email, hashed, user.role))
    user.id = generate_id
    created_at = await read_query('''SELECT created_at FROM users WHERE id = %s''', (generate_id,))
    user.created_at = created_at[0][0]
    return user


async def update(id: int, user: UpdateUser):
    password = await hash_password(user.password)
    await update_query('''UPDATE users SET username = %s, email = %s , password = %s WHERE id = %s  ''',
                       (user.username, user.email, password, id))

    return user


async def check_unique_update_email_password(id: int, user: UpdateUser):
    data = await read_query('''SELECT username,email FROM users WHERE (username = %s OR email = %s) AND id <> %s''',
                            (user.username, user.email, id))

    return len(data) > 0


async def delete(id: int):
    await update_query('''DELETE FROM users WHERE id = %s''', (id,))


async def get_by_id(id: int):
    data = await read_query('''SELECT id, username, email, role, created_at FROM users WHERE id = %s''',
                            (id,))
    return User.from_query_result(*data[0])


async def exists_by_username_email(user: User):
    data = await read_query('''SELECT username,email FROM users WHERE username =%s or email = %s''',
                            (user.username, user.email))

    return len(data) > 0


async def exists_by_id(id: int):
    data = await read_query('''SELECT id FROM users WHERE id = %s''',
                            (id,))

    return len(data) > 0


async def login(credentials: EmailLogin | UsernameLogin):
    if isinstance(credentials, EmailLogin):
        data = await read_query('''SELECT id,username,email,password FROM users WHERE email = %s''',
                                (credentials.email,))
    if isinstance(credentials, UsernameLogin):
        data = await read_query('''SELECT id,username,email,password FROM users WHERE username = %s''',
                                (credentials.username,))
    id = data[0][0]
    username = data[0][1]
    email = data[0][2]
    password = credentials.password

    return oauth2.create_access_token(id)


async def give_access(member_access: Member):
    read_access = int(member_access.read_access)
    write_access = int(member_access.write_access)
    if await user_has_permissions_for_category(member_access.user_id, member_access.category_id):
        await update_query(
            '''UPDATE categorymembers SET read_access = %s,write_access = %s  Where user_id = %s and category_id = %s''',
            (read_access, write_access, member_access.user_id, member_access.category_id))
    else:
        await insert_query(
            '''INSERT INTO categorymembers(user_id,category_id,read_access,write_access) VALUES (%s,%s,%s,%s)''',
            (member_access.user_id, member_access.category_id, read_access, write_access))


async def revoke_access(member_access: RevokeMemberAccess):
    read_access = 0
    write_access = 0
    await update_query(
        '''UPDATE categorymembers SET read_access = %s,write_access = %s  Where user_id = %s and category_id = %s''',
        (read_access, write_access, member_access.user_id, member_access.category_id))


async def user_has_permissions_for_category(user_id: int, category_id: int):
    data = await read_query('''SELECT * FROM categorymembers WHERE user_id = %s and category_id = %s''',
                            (user_id, category_id))

    return len(data) > 0


async def verify_credentials(credentials: EmailLogin | UsernameLogin):
    data = None
    if isinstance(credentials, EmailLogin):
        data = await read_query('''SELECT username,email,password FROM users WHERE email = %s''',
                                (credentials.email,))
    if isinstance(credentials, UsernameLogin):
        data = await read_query('''SELECT username,email,password FROM users WHERE username = %s''',
                                (credentials.username,))
    return len(data) > 0


async def is_user_authorized_to_get_delete(token: str, id: int):
    user_id = oauth2.get_current_user(token)
    data = await read_query('''SELECT role FROM users WHERE id = %s''',
                            (user_id,))
    role = data[0][0]
    return user_id == id or role.lower() == 'admin'


async def is_admin(token: str):
    user_id = oauth2.get_current_user(token)
    data = await read_query('''SELECT role FROM users WHERE id = %s''',
                            (user_id,))
    role = data[0][0]
    return role.lower() == 'admin'


async def valid_password(credentials: EmailLogin | UsernameLogin):
    actual_password = None
    if isinstance(credentials, EmailLogin):
        result = await read_query('''SELECT password FROM users WHERE  email = %s''', (credentials.email,))
        actual_password = result[0][0]
    elif isinstance(credentials, UsernameLogin):
        result = await read_query('''SELECT password FROM users WHERE username = %s ''', (credentials.username,))
        actual_password = result[0][0]

    return await verify_password(credentials.password, actual_password)
