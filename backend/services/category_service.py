from database.database_queries import read_query, insert_query
from schemas.category import Category


def get_all():
    query = read_query("SELECT id, name FROM category")
    return [Category(id=id, name=name) for id, name in query]


def create(category: Category):
    generated_id = insert_query("INSERT INTO category (name) VALUES (?)", (category.name,))
    category.id = generated_id
    return category
