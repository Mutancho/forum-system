from fastapi import APIRouter, status, HTTPException
from services.category_service import (get_all, create, update, delete, get_category_by_id_with_topics,
                                       lock, unlock, make_private, make_non_private, view_privileged_users)
from schemas.category import Category
from routers.helper_functions import handle_category_updates

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


@router_category.get("/{category_id}")
def get_category_by_id(category_id: int):
    category_with_topics = get_category_by_id_with_topics(category_id)
    if not category_with_topics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category_with_topics


@router_category.get("/{category_id}/privileged_users")
def get_privileged_users(category_id: int):
    privileged_users = view_privileged_users(category_id)
    if not privileged_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return privileged_users


@router_category.post("/", status_code=status.HTTP_201_CREATED)
def create_category(category: Category):
    created_category = create(category)
    if created_category is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create category")
    return category


@router_category.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    deleted = delete(category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


@router_category.put("/{category_id}")
def update_category(category_id: int, category: Category):
    update_status = update(category_id, category)
    return handle_category_updates(update_status)


@router_category.put("/lock/{category_id}")
def lock_category(category_id: int):
    update_status = lock(category_id)
    return handle_category_updates(update_status)


@router_category.put("/unlock/{category_id}")
def unlock_category(category_id: int):
    update_status = unlock(category_id)
    return handle_category_updates(update_status)


@router_category.put("/private/{category_id}")
def make_category_private(category_id: int):
    update_status = make_private(category_id)
    return handle_category_updates(update_status)


@router_category.put("/non_private/{category_id}")
def make_category_non_private(category_id: int):
    update_status = make_non_private(category_id)
    return handle_category_updates(update_status)
