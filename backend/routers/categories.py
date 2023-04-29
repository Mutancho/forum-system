from fastapi import APIRouter, status, HTTPException, Header
from services.category_service import (get_all, create, update, delete, get_category_by_id_with_topics,
                                       lock, unlock, make_private, make_non_private, view_privileged_users,
                                       add_user_as_private_member, remove_user_as_private_member)
from schemas.category import Category
from routers.helper_functions import query_filters, http_validations, Constants

router_category = APIRouter(prefix="/categories", tags=["Categories"])


@router_category.get("/")
async def get_categories(search: str | None = None, sort: str | None = None,
                         skip: int | None = None, limit: int | None = None):
    data = await get_all()
    filtered_data = query_filters(data, key="name", search=search, sort=sort, skip=skip, limit=limit)
    return filtered_data


@router_category.get("/{category_id}")
async def get_category_by_id(category_id: int, search: str | None = None, sort: str | None = None,
                             skip: int | None = None, limit: int | None = None,
                             auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    category_with_topics = await get_category_by_id_with_topics(token, category_id)

    category_with_topics.topics = query_filters(category_with_topics.topics, key="title", search=search, sort=sort,
                                                skip=skip,
                                                limit=limit)
    return http_validations(category_with_topics, Constants.CATEGORY)


@router_category.get("/{category_id}/privileged_users")
async def get_privileged_users(category_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    privileged_users = await view_privileged_users(token, category_id)
    if not privileged_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return privileged_users


@router_category.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(category: Category, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    created_category = await create(token, category)
    if created_category is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create category")
    return category


@router_category.post("/{category_id}/private/add/{user_id}")
async def add_user_to_private_category(category_id: int, user_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    added_user = await add_user_as_private_member(token, category_id, user_id)
    return http_validations(added_user, Constants.CATEGORY)


@router_category.delete("/{category_id}/private/remove/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_from_private_category(category_id: int, user_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    removed_user = await remove_user_as_private_member(token, category_id, user_id)
    return http_validations(removed_user, Constants.CATEGORY)


@router_category.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    deleted = await delete(token, category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


@router_category.put("/{category_id}")
async def update_category(category_id: int, category: Category, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    update_status = await update(token, category_id, category)
    return http_validations(update_status, Constants.CATEGORY)


@router_category.put("/lock/{category_id}")
async def lock_category(category_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    update_status = await lock(token, category_id)
    return http_validations(update_status, Constants.CATEGORY)


@router_category.put("/unlock/{category_id}")
async def unlock_category(category_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    update_status = await unlock(token, category_id)
    return http_validations(update_status, Constants.CATEGORY)


@router_category.put("/private/{category_id}")
async def make_category_private(category_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    update_status = await make_private(token, category_id)
    return http_validations(update_status, Constants.CATEGORY)


@router_category.put("/non-private/{category_id}")
async def make_category_non_private(category_id: int, auth: str = Header(alias="Authorization")):
    token = auth[8:-1]
    update_status = await make_non_private(token, category_id)
    return http_validations(update_status, Constants.CATEGORY)
