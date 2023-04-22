from database.database_queries import read_query, insert_query, update_query
from schemas.topic import TopicWithUserAndCategory, BaseTopic, TopicWithReplies, TopicBestReply
from schemas.reply import BaseReply
from services.user_service import is_admin
from services.validations import UpdateStatus
from services.reply_service import exists_by_id
from utils.oauth2 import get_current_user
from services.category_service import is_category_private, category_read_restriction_applies, category_exists, \
    category_write_restriction_applies, is_category_locked


def get_topic_by_id_with_replies(token: str, category_id: int, topic_id: int) -> TopicWithReplies | UpdateStatus:
    user_id = get_current_user(token)
    topic_data = topic_exists(topic_id)
    if not topic_data:
        return UpdateStatus.NOT_FOUND

    if not is_admin(token):
        if not category_exists(category_id):
            return UpdateStatus.NOT_FOUND
        if is_category_private(category_id)[0][0] and not category_read_restriction_applies(user_id)[0][0]:
            return UpdateStatus.NO_READ_ACCESS

    replies_data = read_query("SELECT id, content FROM reply WHERE topic_id = ?", (topic_id,))
    replies = [BaseReply(id=id, content=content) for id, content in replies_data]
    return TopicWithReplies(topic=topic_data, replies=replies)


def create(token: str, category_id: int, topic: TopicWithUserAndCategory):
    user_id = get_current_user(token)
    if not is_admin(token):
        if is_category_private(category_id)[0][0] and not category_write_restriction_applies(user_id)[0][0]:
            return UpdateStatus.NO_WRITE_ACCESS
        if is_category_locked(category_id)[0][0]:
            return UpdateStatus.LOCKED

    is_locked = read_query("SELECT locked FROM category WHERE id = ?", (category_id,))[0][0]
    category = read_query("SELECT id FROM category where id = ?", (category_id,))
    if is_locked:
        return UpdateStatus.LOCKED
    if category_id != category[0][0]:
        return UpdateStatus.BAD_REQUEST
    generated_id = insert_query("INSERT INTO topic(title, content, user_id, category_id) VALUES(?,?,?, ?)",
                                (topic.title, topic.content, user_id, category_id))
    topic.id = generated_id
    topic.category_id = category_id
    topic.user_id = user_id
    return topic


def delete(token: str, topic_id: int) -> UpdateStatus:
    if not topic_exists(topic_id):
        return UpdateStatus.NOT_FOUND
    if get_current_user(token) or is_admin(token):
        update_query("DELETE FROM topic WHERE id = ?", (topic_id,))
        return UpdateStatus.SUCCESS
    return UpdateStatus.BAD_REQUEST


def update(token: str, topic_id: int, topic: BaseTopic) -> UpdateStatus:
    user_id = get_current_user(token)
    updated_rows = update_query("UPDATE topic SET title = ?, content = ? WHERE id = ? AND user_id = ?",
                                (topic.title, topic.content, topic_id, user_id))

    if updated_rows == 0:
        return UpdateStatus.NOT_FOUND
    return UpdateStatus.SUCCESS


def set_best_reply(token: str, topic_id: int, topic: TopicBestReply):
    if not exists_by_id(topic.best_reply_id):
        return UpdateStatus.NOT_FOUND
    user_id = get_current_user(token)
    updated_rows = update_query("UPDATE topic SET best_reply_id = ? WHERE id = ? AND user_id = ?",
                                (topic.best_reply_id, topic_id, user_id))
    if updated_rows == 0:
        return UpdateStatus.NOT_FOUND
    return UpdateStatus.SUCCESS


def lock(token: str, topic_id: int) -> UpdateStatus | None:
    if is_admin(token):
        updated_rows = update_query("UPDATE topic SET locked = 1 WHERE id = ?", (topic_id,))
        return _update_helper(updated_rows, topic_id)


def unlock(token: str, topic_id: int) -> UpdateStatus | None:
    if is_admin(token):
        updated_rows = update_query("UPDATE topic SET locked = 0 WHERE id = ?", (topic_id,))
        return _update_helper(updated_rows, topic_id)


def topic_exists(topic_id: int) -> BaseTopic | None:
    data = read_query("SELECT id, title, content FROM topic where id = ?", (topic_id,))
    if not data:
        return None
    return BaseTopic(id=data[0][0], title=data[0][1], content=data[0][2])


def _update_helper(updated_rows: int, topic_id: int) -> UpdateStatus:
    if updated_rows == 0:
        category = get_topic_by_id(topic_id)
        if category is None:
            return UpdateStatus.NOT_FOUND
        else:
            return UpdateStatus.NO_CHANGE
    return UpdateStatus.SUCCESS


def get_topic_by_id(topic_id: int) -> BaseTopic | None:
    data = read_query("SELECT id, title, content FROM topic WHERE id = ?", (topic_id,))
    if not data:
        return None
    return BaseTopic(id=data[0][0], title=data[0][1], content=data[0][2])

def is_topic_owner(topic_id,token):
    auth_user_id = get_current_user(token)
    data = read_query('''SELECT user_id FROM topic WHERE id = ? ''',(topic_id,))
    user_id = data[0][0]
    return user_id == auth_user_id


def is_topic_locked(topic_id: int):
    return read_query("SELECT locked FROM topic WHERE id = ?", (topic_id,))
