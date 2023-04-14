from backend.database.database_queries import read_query
from backend.schemas.category import Category


def get_all():
    data = read_query("SELECT id, name FROM forumproject.category")
    return (Category(id=id, name=name) for id, name in data)


def get_all_with_topics():
    pass
