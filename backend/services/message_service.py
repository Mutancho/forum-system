import datetime
from schemas.message import Message
from database.database_queries import insert_query, read_query, update_query
from schemas.user import User,DisplayUser


def create(message: Message):
    generate_id = insert_query('''INSERT INTO message(content,sender_id,receiver_id) VALUES (?,?,?)''',(message.content,message.sender_id,message.reciever_id))

    message.id = generate_id
    message.created_at = read_query('''SELECT created_at FROM message WHERE id = ?''',(generate_id,))[0]

    return message

def get_all_my_conversations(id:int)->list[DisplayUser]:
    data = read_query('''SELECT receiver_id FROM message WHERE sender_id = ? ''',(id,))
    ids = ','.join(str(id[0]) for id in set(data))

    users = read_query(f'''SELECT * FROM user WHERE id in ({ids})''')

    return (DisplayUser.from_query_result(*u) for u in users)

def get_all_my_conversations_with(auth_user_id:int,receiver_id:int):#The formating needs to be fixed so JSON displayes it as intended
    data = read_query('''SELECT sender_id,content,created_at,receiver_id FROM message WHERE (sender_id=? and receiver_id = ?) or 
    (receiver_id = ? and sender_id = ?) ORDER BY created_at''',(auth_user_id,receiver_id,auth_user_id,receiver_id))
    converstion = ''
    for msg in data:
        if msg[0]== auth_user_id:
            converstion+= msg[1]+f' -{msg[2]}'+'\n'
        else:
            converstion += '   '+msg[1] +f' -{msg[2]}'+ '\n'
    # print(converstion)
    return converstion




