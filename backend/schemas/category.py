from pydantic import BaseModel
from schemas.topic import BaseTopic


class Category(BaseModel):
    id: int | None
    name: str


class CategoryWithTopics(BaseModel):
    category: Category
    topics: list[BaseTopic]


class PrivilegedCategoryUsers(BaseModel):
    user_id: int
    read_access: bool
    write_access: bool

