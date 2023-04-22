from database.database_queries import read_query, insert_query, update_query
from schemas.category import Category, CategoryWithTopics, PrivilegedCategoryUsers
from schemas.topic import BaseTopic
from services.validations import UpdateStatus
from utils.oauth2 import get_current_user
from services.user_service import is_admin, exists_by_id


def get_all():
    query = read_query("SELECT id, name FROM categories")
    return [Category(id=id, name=name) for id, name in query]


def get_category_by_id_with_topics(token: str, category_id: int) -> CategoryWithTopics | UpdateStatus:
    user_id = get_current_user(token)
    category_data = category_exists(category_id)

    if not category_data:
        return UpdateStatus.NOT_FOUND

    if not is_admin(token):
        if is_category_private(category_id)[0][0] and not category_read_restriction_applies(user_id)[0][0]:
            return UpdateStatus.NO_READ_ACCESS

    topic_data = read_query("SELECT id, title, content FROM topics WHERE category_id = ?", (category_id,))
    topics = [BaseTopic(id=id, title=title, content=content) for id, title, content in topic_data]
    return CategoryWithTopics(category=category_data, topics=topics)


def create(token: str, category: Category):
    if is_admin(token):
        generated_id = insert_query("INSERT INTO categories (name) VALUES (?)", (category.name,))
        category.id = generated_id
        return category


def delete(token: str, category_id: int) -> bool:
    if is_admin(token):
        deleted_rows = update_query("DELETE FROM categories WHERE id = ?", (category_id,))
        return deleted_rows > 0


def update(token: str, category_id: int, category: Category) -> UpdateStatus:
    if is_admin(token):
        updated_rows = update_query("UPDATE categories SET name = ? WHERE id = ?", (category.name, category_id))
        return _update_helper(updated_rows, category_id)


def lock(token: str, category_id: int) -> UpdateStatus | None:
    if is_admin(token):
        updated_rows = update_query("UPDATE categories SET locked = 1 WHERE id = ?", (category_id,))
        return _update_helper(updated_rows, category_id)


def unlock(token: str, category_id: int) -> UpdateStatus:
    if is_admin(token):
        updated_rows = update_query("UPDATE categories SET locked = 0 WHERE id = ?", (category_id,))
        return _update_helper(updated_rows, category_id)


def make_private(token: str, category_id: int) -> UpdateStatus:
    if is_admin(token):
        updated_rows = update_query("UPDATE categories SET is_private = 1 WHERE id = ?", (category_id,))
        return _update_helper(updated_rows, category_id)


def make_non_private(token: str, category_id: int):
    if is_admin(token):
        updated_rows = update_query("UPDATE categories SET is_private = 0 WHERE id = ?", (category_id,))
        return _update_helper(updated_rows, category_id)


def view_privileged_users(token: str, category_id: int):
    if is_admin(token):
        privileged_users = read_query(
            "SELECT user_id, read_access, write_access from categorymembers where category_id =?",
            (category_id,))
        return [PrivilegedCategoryUsers(user_id=user_id, read_access=read_access, write_access=write_access) for
                user_id, read_access, write_access in privileged_users]


def add_user_as_private_member(token: str, category_id: int, user_id: int):
    if not (category_exists(category_id) and exists_by_id(user_id)):
        return UpdateStatus.NOT_FOUND
    if not is_admin(token):
        return UpdateStatus.ADMIN_REQUIRED

    existing_entry = read_query("SELECT * FROM categorymembers WHERE user_id = ? AND category_id = ?",
                                (user_id, category_id))
    if existing_entry:
        return UpdateStatus.DUPLICATE_ENTRY

    insert_query("INSERT INTO categorymembers (user_id, category_id, read_access) VALUES (?,?,?)",
                             (user_id, category_id, 1))

    return UpdateStatus.SUCCESS


def remove_user_as_private_member(token: str, category_id: int, user_id: int):
    if not (category_exists(category_id) and exists_by_id(user_id)):
        return UpdateStatus.NOT_FOUND
    if not is_admin(token):
        return UpdateStatus.ADMIN_REQUIRED
    affected_rows = update_query("DELETE FROM categorymembers WHERE user_id = ? and category_id = ?",
                                 (user_id, category_id))
    if affected_rows == 0:
        return UpdateStatus.NOT_FOUND
    return UpdateStatus.SUCCESS


def _update_helper(updated_rows: int, category_id: int) -> UpdateStatus:
    if updated_rows == 0:
        category = category_exists(category_id)
        if category is None:
            return UpdateStatus.NOT_FOUND
        else:
            return UpdateStatus.NO_CHANGE
    return UpdateStatus.SUCCESS


def category_exists(category_id: int) -> Category | None:
    data = read_query("SELECT id, name FROM categories WHERE id = ?", (category_id,))
    if not data:
        return None
    return Category(id=data[0][0], name=data[0][1])


def _check_duplicate_name(category_id: int, new_name: str) -> bool:
    # todo: double check if needed or if the database will have unique constraint for duplicates
    data = read_query("SELECT name FROM categories WHERE id = ?", (category_id,))
    if not data:
        return False
    return data[0][0].lower() == new_name.lower()


def is_category_private(category_id: int):
    return read_query("SELECT is_private FROM categories WHERE id = ?", (category_id,))


def category_read_restriction_applies(user_id: int):
    return read_query("SELECT read_access FROM categorymembers WHERE user_id = ?", (user_id,))


def category_write_restriction_applies(user_id: int):
    return read_query("SELECT write_access FROM categorymembers WHERE user_id = ?", (user_id,))


def is_category_locked(category_id: int):
    return read_query("SELECT locked FROM categories WHERE id = ?", (category_id,))
