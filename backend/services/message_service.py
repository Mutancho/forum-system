import datetime
from schemas.message import Message
from database.database_queries import insert_query, read_query, update_query
from schemas.user import User,DisplayUser
from utils import oauth2


def create(message: Message):
    generate_id = insert_query('''INSERT INTO messages(content,sender_id,receiver_id) VALUES (?,?,?)''',(message.content,message.sender_id,message.reciever_id))

    message.id = generate_id
    message.created_at = read_query('''SELECT created_at FROM message WHERE id = ?''',(generate_id,))[0]

    return message

def get_all_my_conversations(token:str)->list[DisplayUser]:
    id = oauth2.get_current_user(token)
    data = read_query('''SELECT receiver_id FROM messages WHERE sender_id = ? ''',(id,))
    data += read_query('''SELECT sender_id FROM messages WHERE receiver_id  = ? ''', (id,))
    ids = ','.join(str(id[0]) for id in set(data))

    users = read_query(f'''SELECT * FROM users WHERE id in ({ids})''')

    return (DisplayUser.from_query_result(*u) for u in users)

def get_all_my_conversations_with(token:str,receiver_id:int):#The formating needs to be fixed so JSON displayes it as intended
    auth_user_id = oauth2.get_current_user(token)
    data = read_query('''SELECT sender_id,content,created_at,receiver_id FROM messages WHERE (sender_id=? and receiver_id = ?) or 
    (receiver_id = ? and sender_id = ?) ORDER BY created_at''',(auth_user_id,receiver_id,auth_user_id,receiver_id))
    converstion = {}
    for msg in data:
        if msg[0]== auth_user_id:
            converstion[msg[2].strftime("%m/%d/%Y, %H:%M:%S")]= msg[1]
        else:
            converstion[msg[2].strftime("%m/%d/%Y, %H:%M:%S")] = '         '+msg[1]

    return converstion
