from database.database_queries import read_query, insert_query, update_query
from services.validations import UpdateStatus
from schemas.reply import ReplyWithUserAndTopic


def get_all(topic_id: int):
    query = read_query("SELECT * FROM reply where topic_id=?", (topic_id,))
    return [ReplyWithUserAndTopic(id=row[0], content=row[1], created_at=row[2], updated_at=row[3],
                                  user_id=row[4], topic_id=row[5]) for row in query]


def create():
    pass


def update_reply():
    pass


def upvote_reply():
    pass


def down_vote_reply():
    pass


def set_best_reply():
    pass
