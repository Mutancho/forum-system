import datetime
from backend.database.database_queries import read_query, insert_query, update_query
from backend.services.validations import UpdateStatus
from backend.schemas.reply import ReplyWithUserAndTopic, Vote, Reply, UpdateReply
from backend.utils import oauth2


async def get_by_id(reply_id: int):
    data = await read_query('''SELECT id, content, created_at, updated_at FROM replies WHERE id = %s''', (reply_id,))
    if not data:
        return {}
    votes_for_reply = await get_votes_for_reply(reply_id)  # await here
    return {**dict(Reply.from_query_result(*data[0])), **votes_for_reply}  # use the awaited result


async def create(reply: Reply, topic_id, token):
    user_id = oauth2.get_current_user(token)
    content = reply.content
    generate_id = await insert_query('''INSERT INTO replies(content,user_id,topic_id) VALUES (%s,%s,%s)''',
                               (content, user_id, topic_id))
    reply.id = generate_id
    votes_for_reply = await get_votes_for_reply(generate_id)
    return {**{"id": reply.id, "content": content}, **votes_for_reply}


async def update_reply(reply_id: int, reply: UpdateReply):
    content = reply.content
    await update_query('''UPDATE replies SET content = %s WHERE id = %s''', (content, reply_id))
    update_time = await read_query('''SELECT updated_at FROM replies WHERE id = %s''', (reply_id,))
    votes_for_reply = await get_votes_for_reply(reply_id)
    return {**{"id": reply_id, "content": content, "update on": update_time[0][0].strftime("%d-%m-%Y %H:%M:%S")},
            **votes_for_reply}


async def reply_vote(id: int, vote: Vote, token):
    user_id = oauth2.get_current_user(token)
    reply_id = id
    vote_type = vote.vote.lower()
    await insert_query('''INSERT INTO replyvotes(reply_id,vote_type,user_id) VALUES (%s,%s,%s)''',
                 (reply_id, vote_type, user_id))
    vote.vote = vote_type.capitalize()
    return vote


async def update_reply_vote(id: int, vote: Vote, token):
    user_id = oauth2.get_current_user(token)
    reply_id = id
    vote_type = vote.vote.lower()
    await update_query('''UPDATE replyvotes SET vote_type = %s WHERE reply_id = %s and user_id = %s ''',
                 (vote_type, reply_id, user_id))
    vote.vote = vote_type.capitalize()
    return vote


async def delete(id: int):
    await update_query('''DELETE FROM replies WHERE id =%s ''', (id,))


async def already_voted(reply_id: int, token):
    user_id = oauth2.get_current_user(token)
    data = await read_query('''SELECT * FROM replyvotes WHERE reply_id = %s and user_id = %s''', (reply_id, user_id))

    return len(data) > 0


async def get_votes_for_reply(reply_id: int):
    data = await read_query('''SELECT vote_type FROM replyvotes WHERE reply_id = %s ''', (reply_id,))
    upvote = 0
    downvote = 0
    for vote in data:
        if vote[0] == 'upvote':
            upvote += 1
        elif vote[0] == 'downvote':
            downvote += 1
    return {'upvote': upvote, 'downvote': downvote}


async def is_reply_owner(reply_id, token):
    auth_user_id = oauth2.get_current_user(token)
    data = await read_query('''SELECT user_id FROM replies WHERE id = %s ''', (reply_id,))
    user_id = data[0][0]
    return user_id == auth_user_id


async def exists_by_id(id: int):
    data = await read_query('''SELECT * FROM replies WHERE id = %s''', (id,))

    return len(data) > 0
