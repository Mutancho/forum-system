from fastapi import APIRouter, status, HTTPException, Response
from backend.services.category_service import get_all


router_category = APIRouter(prefix="/categories", tags=["Categories"])


@router_category.get("/")
def get_categories():
    data = get_all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return data


@router_category.get("/topics")
def get_categories_with_topics():
    pass
