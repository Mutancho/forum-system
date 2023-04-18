from database.database_queries import read_query, insert_query, update_query
from schemas.topic import TopicWithUserAndCategory, TopicsOut, BaseTopic
from services.validations import UpdateStatus


def get_all(category_id: int):
    query = read_query("SELECT * FROM topic where category_id=?", (category_id,))
    print(query[3])
    return [TopicsOut(id=row[0], title=row[1], content=row[2],
                      user_id=row[6], category_id=row[6], created_at=row[3],
                      updated_at=row[4], locked=row[7], best_reply=row[8])
            for row in query]


def create(category_id_url: int, topic: TopicWithUserAndCategory):
    category = read_query("SELECT id FROM category where id = ?", (topic.category_id,))
    if category_id_url != category[0][0]:
        return None
    generated_id = insert_query("INSERT INTO topic(title, content,user_id, category_id) VALUES(?,?,?,?)",
                                (topic.title, topic.content, topic.user_id, topic.category_id))
    topic.id = generated_id
    return topic


def lock(topic_id: int) -> UpdateStatus | None:
    updated_rows = update_query("UPDATE topic SET locked = 1 WHERE id = ?", (topic_id,))
    return _update_helper(updated_rows, topic_id)


def unlock(topic_id: int) -> UpdateStatus:
    updated_rows = update_query("UPDATE topic SET locked = 0 WHERE id = ?", (topic_id,))
    return _update_helper(updated_rows, topic_id)


def best_reply():
    pass


def _update_helper(updated_rows: int, topic_id: int) -> UpdateStatus:
    if updated_rows == 0:
        category = _get_topic_by_id(topic_id)
        if category is None:
            return UpdateStatus.NOT_FOUND
        else:
            return UpdateStatus.NO_CHANGE
    return UpdateStatus.SUCCESS


def _get_topic_by_id(topic_id: int) -> BaseTopic | None:
    data = read_query("SELECT id, title, content FROM topic WHERE id = ?", (topic_id,))
    if not data:
        return None
    return BaseTopic(id=data[0][0], title=data[0][1], content=data[0][2])
