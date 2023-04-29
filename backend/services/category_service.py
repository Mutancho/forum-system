from database.database_queries import read_query, insert_query, update_query
from schemas.category import Category, CategoryWithTopics, PrivilegedCategoryUsers, CategoryOut
from schemas.topic import BaseTopic
from services.validations import UpdateStatus
from utils.oauth2 import get_current_user
from services.user_service import is_admin, exists_by_id


async def get_all():
    query = await read_query("SELECT * FROM categories")
    return [CategoryOut(id=category_id, name=name, private=private, locked=locked) for
            category_id, name, private, locked in
            query]


async def get_category_by_id_with_topics(token: str, category_id: int):
    user_id = get_current_user(token)
    category_data = await category_exists(category_id)

    if not category_data:
        return UpdateStatus.NOT_FOUND

    if not await is_admin(token):
        is_private = await is_category_private(category_id)
        read_restriction = await category_read_restriction_applies(user_id)
        if is_private[0][0] and not read_restriction[0][0]:
            return UpdateStatus.NO_READ_ACCESS

    topic_data = await read_query("SELECT id, title FROM topics WHERE category_id = %s", (category_id,))
    topics = [BaseTopic(id=id, title=title) for id, title in topic_data]
    return CategoryWithTopics(category=category_data, topics=topics)


async def create(token: str, category: Category):
    if await is_admin(token):
        generated_id = await insert_query("INSERT INTO categories (name) VALUES (%s)", (category.name,))
        category.id = generated_id
        return category


async def delete(token: str, category_id: int) -> bool:
    if await is_admin(token):
        deleted_rows = await update_query("DELETE FROM categories WHERE id = %s", (category_id,))
        return deleted_rows > 0


async def update(token: str, category_id: int, category: Category) -> UpdateStatus:
    if await is_admin(token):
        updated_rows = await update_query("UPDATE categories SET name = %s WHERE id = %s", (category.name, category_id))
        return _update_helper(updated_rows, category_id)


async def lock(token: str, category_id: int) -> UpdateStatus | None:
    if await is_admin(token):
        updated_rows = await update_query("UPDATE categories SET locked = 1 WHERE id = %s", (category_id,))
        return _update_helper(updated_rows, category_id)


async def unlock(token: str, category_id: int) -> UpdateStatus:
    if await is_admin(token):
        updated_rows = await update_query("UPDATE categories SET locked = 0 WHERE id = %s", (category_id,))
        return _update_helper(updated_rows, category_id)


async def make_private(token: str, category_id: int) -> UpdateStatus:
    if await is_admin(token):
        updated_rows = await update_query("UPDATE categories SET is_private = 1 WHERE id = %s", (category_id,))
        return _update_helper(updated_rows, category_id)


async def make_non_private(token: str, category_id: int):
    if await is_admin(token):
        updated_rows = await update_query("UPDATE categories SET is_private = 0 WHERE id = %s", (category_id,))
        return _update_helper(updated_rows, category_id)


async def view_privileged_users(token: str, category_id: int):
    if await is_admin(token):
        privileged_users = await read_query(
            "SELECT user_id, read_access, write_access from categorymembers where category_id =%s",
            (category_id,))
        return [PrivilegedCategoryUsers(user_id=user_id, read_access=read_access, write_access=write_access) for
                user_id, read_access, write_access in privileged_users]


async def add_user_as_private_member(token: str, category_id: int, user_id: int):
    does_category_exist = await category_exists(category_id)
    does_user_exist = await exists_by_id(user_id)
    if not (does_category_exist and does_user_exist):
        return UpdateStatus.NOT_FOUND
    if not is_admin(token):
        return UpdateStatus.ADMIN_REQUIRED

    existing_entry = await read_query("SELECT * FROM categorymembers WHERE user_id = %s AND category_id = %s",
                                      (user_id, category_id))
    if existing_entry:
        return UpdateStatus.DUPLICATE_ENTRY

    await insert_query("INSERT INTO categorymembers (user_id, category_id, read_access) VALUES (%s,%s,%s)",
                       (user_id, category_id, 1))

    return UpdateStatus.SUCCESS


async def remove_user_as_private_member(token: str, category_id: int, user_id: int):
    if not (await category_exists(category_id) and await exists_by_id(user_id)):
        return UpdateStatus.NOT_FOUND
    if not is_admin(token):
        return UpdateStatus.ADMIN_REQUIRED
    affected_rows = await update_query("DELETE FROM categorymembers WHERE user_id = %s and category_id = %s",
                                       (user_id, category_id))
    if affected_rows == 0:
        return UpdateStatus.NOT_FOUND
    return UpdateStatus.SUCCESS


def _update_helper(updated_rows: int, category_id: int) -> UpdateStatus:
    if updated_rows == 0:
        category = await category_exists(category_id)
        if category is None:
            return UpdateStatus.NOT_FOUND
        else:
            return UpdateStatus.NO_CHANGE
    return UpdateStatus.SUCCESS


async def category_exists(category_id: int) -> Category | None:
    data = await read_query("SELECT * FROM categories WHERE id = %s", (category_id,))
    if not data:
        return None
    return CategoryOut(id=data[0][0], name=data[0][1], private=data[0][2], locked=data[0][3])


async def is_category_private(category_id: int):
    return await read_query("SELECT is_private FROM categories WHERE id = %s", (category_id,))


async def category_read_restriction_applies(user_id: int):
    return await read_query("SELECT read_access FROM categorymembers WHERE user_id = %s", (user_id,))


async def category_write_restriction_applies(user_id: int):
    return await read_query("SELECT write_access FROM categorymembers WHERE user_id = %s", (user_id,))


async def is_category_locked(category_id: int):
    return await read_query("SELECT locked FROM categories WHERE id = %s", (category_id,))
