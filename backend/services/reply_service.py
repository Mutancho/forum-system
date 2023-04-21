from database.database_queries import read_query, insert_query, update_query
from services.validations import UpdateStatus
from schemas.reply import ReplyWithUserAndTopic, Vote
from utils import oauth2


def get_all(topic_id: int):
    query = read_query("SELECT * FROM reply where topic_id=?", (topic_id,))
    return [ReplyWithUserAndTopic(id=row[0], content=row[1], created_at=row[2], updated_at=row[3],
                                  user_id=row[4], topic_id=row[5]) for row in query]


def create():
    pass


def update_reply():
    pass


def reply_vote(id:int , vote: Vote,token):
    user_id = oauth2.get_current_user(token)
    reply_id = id
    vote_type = vote.vote.lower()
    insert_query('''INSERT INTO replyvote(reply_id,vote_type,user_id) VALUES (?,?,?)''',(reply_id,vote_type,user_id))
    vote.vote = vote_type.capitalize()
    return vote


def update_reply_vote(id:int , vote: Vote,token):
    user_id = oauth2.get_current_user(token)
    reply_id = id
    vote_type = vote.vote.lower()
    insert_query('''UPDATE replyvote SET vote_type = ? WHERE reply_id = ? and user_id = ? ''',
                 (vote_type,reply_id,user_id))
    vote.vote = vote_type.capitalize()
    return vote


def already_voted(reply_id: int,token):
    user_id = oauth2.get_current_user(token)
    data = read_query('''SELECT * FROM replyvote WHERE reply_id = ? and user_id = ?''',(reply_id,user_id))

    return len(data)>0

def set_best_reply():
    pass

def exists_by_id(id: int):
    data = read_query('''SELECT * FROM reply WHERE id = ?''',(id,))

    return len(data)>0
