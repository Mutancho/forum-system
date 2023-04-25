import datetime

from database.database_queries import read_query, insert_query, update_query
from services.validations import UpdateStatus
from schemas.reply import ReplyWithUserAndTopic, Vote, Reply, UpdateReply
from utils import oauth2


def get_all(topic_id: int):
    query = read_query("SELECT * FROM replies where topic_id=?", (topic_id,))
    return [ReplyWithUserAndTopic(id=row[0], content=row[1], created_at=row[2], updated_at=row[3],
                                  user_id=row[4], topic_id=row[5]) for row in query]

def get_by_id(reply_id: int):
    data = read_query('''SELECT id, content, created_at, updated_at FROM replies WHERE id = ?''',(reply_id,))
    if data == []:
        return {}
    return {**dict(Reply.from_query_result(*data[0])),**get_votes_for_reply(reply_id)}


def create(reply: Reply,topic_id,token):
    user_id = oauth2.get_current_user(token)
    content = reply.content
    generate_id = insert_query('''INSERT INTO replies(content,user_id,topic_id) VALUES (?,?,?)''',(content,user_id,topic_id))
    reply.id = generate_id

    return {**{"id": reply.id, "content": content},**get_votes_for_reply(generate_id)}


def update_reply(reply_id: int,reply: UpdateReply):
    content = reply.content
    update_query('''UPDATE replies SET content = ? WHERE id = ?''',(content,reply_id))
    update_time = read_query('''SELECT updated_at FROM replies WHERE id = ?''',(reply_id,))

    return {**{"id": reply_id, "content": content, "update on": update_time[0][0].strftime("%d-%m-%Y %H:%M:%S")},**get_votes_for_reply(reply_id)}


def reply_vote(id:int , vote: Vote,token):
    user_id = oauth2.get_current_user(token)
    reply_id = id
    vote_type = vote.vote.lower()
    insert_query('''INSERT INTO replyvotes(reply_id,vote_type,user_id) VALUES (?,?,?)''',(reply_id,vote_type,user_id))
    vote.vote = vote_type.capitalize()
    return vote


def update_reply_vote(id:int , vote: Vote,token):
    user_id = oauth2.get_current_user(token)
    reply_id = id
    vote_type = vote.vote.lower()
    update_query('''UPDATE replyvotes SET vote_type = ? WHERE reply_id = ? and user_id = ? ''',
                 (vote_type,reply_id,user_id))
    vote.vote = vote_type.capitalize()
    return vote

def delete(id: int):
    update_query('''DELETE FROM replies WHERE id =? ''',(id,))

def already_voted(reply_id: int,token):
    user_id = oauth2.get_current_user(token)
    data = read_query('''SELECT * FROM replyvotes WHERE reply_id = ? and user_id = ?''',(reply_id,user_id))

    return len(data)>0

def get_votes_for_reply(reply_id: int):
    data = read_query('''SELECT vote_type FROM replyvotes WHERE reply_id = ? ''', (reply_id,))
    upvote = 0
    downvote = 0
    for vote in data:
        if vote[0] == 'upvote':
            upvote += 1
        elif vote[0] == 'downvote':
            downvote += 1
    return {'upvote': upvote,'downvote': downvote}
def is_reply_owner(reply_id,token):
    auth_user_id = oauth2.get_current_user(token)
    data = read_query('''SELECT user_id FROM replies WHERE id = ? ''',(reply_id,))
    user_id = data[0][0]
    return user_id == auth_user_id

def exists_by_id(id: int):
    data = read_query('''SELECT * FROM replies WHERE id = ?''',(id,))

    return len(data)>0
