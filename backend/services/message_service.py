from schemas.message import Message
from database.database_queries import insert_query, read_query
from schemas.user import DisplayUser
from utils import oauth2


async def create(message: Message):
    generate_id = await insert_query('''INSERT INTO messages(content,sender_id,receiver_id) VALUES (%s,%s,%s)''',
                                     (message.content, message.sender_id, message.receiver_id))

    message.id = generate_id
    created_at = await read_query('''SELECT created_at FROM messages WHERE id = %s''', (generate_id,))
    message.created_at = created_at[0]
    return message


async def get_all_my_conversations(token: str) -> list[DisplayUser]:
    id = oauth2.get_current_user(token)
    data = await read_query('''SELECT receiver_id FROM messages WHERE sender_id = %s ''', (id,))
    data += await read_query('''SELECT sender_id FROM messages WHERE receiver_id  = %s ''', (id,))
    ids = ','.join(str(identifire[0]) for identifire in set(data))

    users = await read_query(f'''SELECT id, username, email, password, role, created_at FROM users WHERE id in ('{ids}')''')
    return [DisplayUser.from_query_result(*u) for u in users]


async def get_all_my_conversations_with(token: str,
                                        receiver_id: int):  # The formating needs to be fixed so JSON displayes it as intended
    auth_user_id = oauth2.get_current_user(token)
    data = await read_query('''SELECT sender_id,content,created_at,receiver_id FROM messages WHERE (sender_id=%s and receiver_id = %s) or 
    (receiver_id = %s and sender_id = %s) ORDER BY created_at''',
                            (auth_user_id, receiver_id, auth_user_id, receiver_id))
    conversation = {}
    for msg in data:
        if msg[0] == auth_user_id:
            conversation[msg[2].strftime("%m/%d/%Y, %H:%M:%S")] = msg[1]
        else:
            conversation[msg[2].strftime("%m/%d/%Y, %H:%M:%S")] = '         ' + msg[1]

    return conversation
