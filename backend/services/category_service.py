from database.database_queries import read_query, insert_query, update_query
from schemas.category import Category, CategoryWithTopics, PrivilegedCategoryUsers
from schemas.topic import BaseTopic
from services.validations import UpdateStatus


def get_all():
    query = read_query("SELECT id, name FROM category")
    return [Category(id=id, name=name) for id, name in query]


def get_category_by_id_with_topics(category_id: int) -> CategoryWithTopics | None:
    category_data = _get_category_by_id(category_id)
    if not category_data:
        return None
    topic_data = read_query("SELECT id, title, content FROM topic WHERE category_id = ?", (category_id,))
    topics = [BaseTopic(id=id, title=title, content=content) for id, title, content in topic_data]
    return CategoryWithTopics(category=category_data, topics=topics)


def create(category: Category):
    generated_id = insert_query("INSERT INTO category (name) VALUES (?)", (category.name,))
    category.id = generated_id
    return category


def delete(category_id: int) -> bool:
    deleted_rows = update_query("DELETE FROM category WHERE id = ?", (category_id,))
    return deleted_rows > 0


def update(category_id: int, category: Category) -> UpdateStatus:
    updated_rows = update_query("UPDATE category SET name = ? WHERE id = ?", (category.name, category_id))
    return _update_helper(updated_rows, category_id)


def lock(category_id: int) -> UpdateStatus | None:
    updated_rows = update_query("UPDATE category SET locked = 1 WHERE id = ?", (category_id,))
    return _update_helper(updated_rows, category_id)


def unlock(category_id: int) -> UpdateStatus:
    updated_rows = update_query("UPDATE category SET locked = 0 WHERE id = ?", (category_id,))
    return _update_helper(updated_rows, category_id)


def make_private(category_id: int) -> UpdateStatus:
    updated_rows = update_query("UPDATE category SET is_private = 1 WHERE id = ?", (category_id,))
    return _update_helper(updated_rows, category_id)


def make_non_private(category_id: int):
    updated_rows = update_query("UPDATE category SET is_private = 0 WHERE id = ?", (category_id,))
    return _update_helper(updated_rows, category_id)


def view_privileged_users(category_id: int):
    privileged_users = read_query("SELECT user_id, read_access, write_access from categorymember where category_id =?",
                                  (category_id,))
    return [PrivilegedCategoryUsers(user_id=user_id, read_access=read_access, write_access=write_access) for
            user_id, read_access, write_access in privileged_users]


def _update_helper(updated_rows: int, category_id: int) -> UpdateStatus:
    if updated_rows == 0:
        category = _get_category_by_id(category_id)
        if category is None:
            return UpdateStatus.NOT_FOUND
        else:
            return UpdateStatus.NO_CHANGE
    return UpdateStatus.SUCCESS


def _get_category_by_id(category_id: int) -> Category | None:
    data = read_query("SELECT id, name FROM category WHERE id = ?", (category_id,))
    if not data:
        return None
    return Category(id=data[0][0], name=data[0][1])


def _check_duplicate_name(category_id: int, new_name: str) -> bool:
    data = read_query("SELECT name FROM category WHERE id = ?", (category_id,))
    if not data:
        return False
    return data[0][0].lower() == new_name.lower()
