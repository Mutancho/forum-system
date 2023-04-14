from database.database_queries import read_query, insert_query, update_query
from schemas.category import Category
from services.validations import UpdateStatus


def get_all():
    query = read_query("SELECT id, name FROM category")
    return [Category(id=id, name=name) for id, name in query]


def create(category: Category):
    generated_id = insert_query("INSERT INTO category (name) VALUES (?)", (category.name,))
    category.id = generated_id
    return category


def update(category_id: int, category: Category) -> UpdateStatus:
    existing_category = _get_category_by_id(category_id)

    if not existing_category:
        return UpdateStatus.NOT_FOUND

    if _check_duplicate_name(category_id, category.name):
        return UpdateStatus.SAME_NAME

    update_query("UPDATE category SET name = ? WHERE id = ?", (category.name, category_id))

    category.id = category_id
    return UpdateStatus.SUCCESS


def delete():
    pass


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
