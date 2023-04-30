from database.database_queries import read_query, insert_query, update_query
from schemas.topic import TopicWithUserAndCategoryWithContent, TopicWithContent, TopicWithReplies, TopicBestReply, \
    TopicsTimeStamps, TopicWithBestReply
from schemas.reply import BaseReply
from services.user_service import is_admin
from services.validations import UpdateStatus
from services.reply_service import exists_by_id
from utils.oauth2 import get_current_user
from services.category_service import is_category_private, category_read_restriction_applies, category_exists, \
    category_write_restriction_applies, is_category_locked


async def get_all():
    query = await read_query("SELECT id, title, created_at, updated_at from topics")
    return [TopicsTimeStamps(id=topic_id, title=title, created_at=created_at, updated_at=updated_at) for
            topic_id, title, created_at, updated_at in query]


async def get_topic_by_id_with_replies(token: str, category_id: int, topic_id: int) -> TopicWithReplies | UpdateStatus:
    user_id = get_current_user(token)
    topic_data = await topic_exists(topic_id)
    if not topic_data:
        return UpdateStatus.NOT_FOUND
    if_exists = await category_exists(category_id)
    if not await is_admin(token):
        if not if_exists:
            return UpdateStatus.NOT_FOUND
        if_private = await is_category_private(category_id)
        if_read_restrictions = await category_read_restriction_applies(user_id)
        if if_private[0][0] and not if_read_restrictions[0][0]:
            return UpdateStatus.NO_READ_ACCESS

    replies_data = await read_query("SELECT id, content FROM replies WHERE topic_id = %s", (topic_id,))
    replies = [BaseReply(id=reply_id, content=content) for reply_id, content in replies_data]
    return TopicWithReplies(topic=topic_data, replies=replies)


async def create(token: str, category_id: int, topic: TopicWithUserAndCategoryWithContent):
    user_id = get_current_user(token)
    if not await is_admin(token):
        if_private = await is_category_private(category_id)
        write_restrictions = await category_write_restriction_applies(user_id)
        if_locked = await is_category_locked(category_id)
        if if_private[0][0] and not await write_restrictions[0][0]:
            return UpdateStatus.NO_WRITE_ACCESS
        if if_locked[0][0]:
            return UpdateStatus.LOCKED

    is_locked = await read_query("SELECT locked FROM categories WHERE id = %s", (category_id,))
    category = await read_query("SELECT id FROM categories where id = %s", (category_id,))
    if is_locked[0][0]:
        return UpdateStatus.LOCKED
    if category_id != category[0][0]:
        return UpdateStatus.BAD_REQUEST
    generated_id = await insert_query("INSERT INTO topics(title, content, user_id, category_id) VALUES(%s,%s,%s,%s)",
                                      (topic.title, topic.content, user_id, category_id))
    topic.id = generated_id
    topic.category_id = category_id
    topic.user_id = user_id
    return topic


async def delete(token: str, topic_id: int) -> UpdateStatus:
    if not await topic_exists(topic_id):
        return UpdateStatus.NOT_FOUND
    if get_current_user(token) or await is_admin(token):
        await update_query("DELETE FROM topics WHERE id = %s", (topic_id,))
        return UpdateStatus.SUCCESS
    return UpdateStatus.BAD_REQUEST


async def update(token: str, topic_id: int, topic: TopicWithContent) -> UpdateStatus:
    user_id = get_current_user(token)
    if_admin = await is_admin(token)
    if if_admin:
        updated_rows = await update_query(
            "UPDATE topics SET title = %s, content = %s WHERE id = %s",
            (topic.title, topic.content, topic_id)
        )
    else:
        updated_rows = await update_query(
            "UPDATE topics SET title = %s, content = %s WHERE id = %s AND user_id = %s",
            (topic.title, topic.content, topic_id, user_id)
        )
    if updated_rows == 0:
        return UpdateStatus.NO_CHANGE

    return UpdateStatus.SUCCESS


async def set_best_reply(token: str, topic_id: int, topic: TopicBestReply) -> UpdateStatus:
    exists = await exists_by_id(topic.best_reply_id)
    if not exists:
        return UpdateStatus.NOT_FOUND
    user_id = get_current_user(token)
    if_admin = await is_admin(token)

    if if_admin:
        updated_rows = await update_query(
            "UPDATE topics SET best_reply_id = %s WHERE id = %s",
            (topic.best_reply_id, topic_id)
        )
    else:
        updated_rows = await update_query(
            "UPDATE topics SET best_reply_id = %s WHERE id = %s AND user_id = %s",
            (topic.best_reply_id, topic_id, user_id)
        )

    if updated_rows == 0:
        return UpdateStatus.NO_CHANGE
    return UpdateStatus.SUCCESS


async def lock(token: str, topic_id: int) -> UpdateStatus | None:
    if await is_admin(token):
        updated_rows = await update_query("UPDATE topics SET locked = 1 WHERE id = %s", (topic_id,))
        return _update_helper(updated_rows, topic_id)


async def unlock(token: str, topic_id: int) -> UpdateStatus | None:
    if await is_admin(token):
        updated_rows = await update_query("UPDATE topics SET locked = 0 WHERE id = %s", (topic_id,))
        return _update_helper(updated_rows, topic_id)


async def topic_exists(topic_id: int) -> TopicWithBestReply | None:
    data = await read_query("SELECT id, title, content, best_reply_id, locked FROM topics where id = %s", (topic_id,))
    if not data:
        return None
    return TopicWithBestReply(id=data[0][0], title=data[0][1], content=data[0][2], best_reply_id=data[0][3],
                              locked=data[0][4])


def _update_helper(updated_rows: int, topic_id: int) -> UpdateStatus:
    if updated_rows == 0:
        category = get_topic_by_id(topic_id)
        if category is None:
            return UpdateStatus.NOT_FOUND
        else:
            return UpdateStatus.NO_CHANGE
    return UpdateStatus.SUCCESS


async def get_topic_by_id(topic_id: int) -> TopicWithContent | None:
    data = await read_query("SELECT id, title, content FROM topics WHERE id = %s", (topic_id,))
    if not data:
        return None
    return TopicWithContent(id=data[0][0], title=data[0][1], content=data[0][2])


async def is_topic_owner(topic_id, token):
    auth_user_id = get_current_user(token)
    data = await read_query('''SELECT user_id FROM topics WHERE id = %s ''', (topic_id,))
    user_id = data[0][0]
    return user_id == auth_user_id


async def is_topic_locked(topic_id: int):
    return await read_query("SELECT locked FROM topics WHERE id = %s", (topic_id,))


async def delete_topic_has_best_reply(topic_id: int):
    if await read_query("SELECT best_reply_id FROM topics where id = %s", (topic_id,)):
        return await update_query("UPDATE topics SET best_reply_id = NULL where id = %s", (topic_id,))
