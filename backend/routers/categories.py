from fastapi import APIRouter, status, HTTPException
from services.category_service import get_all, create
from schemas.category import Category

router_category = APIRouter(prefix="/categories", tags=["Categories"])


@router_category.get("/")
def get_categories(search: str | None = None,
                   sort: str | None = None,
                   skip: int | None = None,
                   limit: int | None = None):
    data = get_all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if search:
        data = [item for item in data if search.lower() in item.name.lower()]

    if sort and (sort.lower().startswith("asc") or sort.lower().startswith("desc")):
        reverse = sort.lower().startswith("desc")
        data.sort(key=lambda x: x.name.lower(), reverse=reverse)

    if skip:
        data = data[skip:]

    if limit:
        data = data[:limit]

    return data



@router_category.get("/topics")
def get_categories_with_topics():
    pass


@router_category.post("/", status_code=status.HTTP_201_CREATED)
def create_category(category: Category):
    created_category = create(category)
    if created_category is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create category")
    return category
