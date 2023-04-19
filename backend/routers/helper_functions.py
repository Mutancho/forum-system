from services.validations import UpdateStatus
from fastapi import HTTPException, status

CATEGORY = "Category"
TOPIC = "Topic"
REPLIES = "Reply"


def handle_updates(update_status: UpdateStatus, info_type: str):
    if update_status == UpdateStatus.NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{info_type} not found")
    elif update_status == UpdateStatus.NO_CHANGE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{info_type} already in the desired state")
    return update_status


def query_filters(data, key: str, search: str | None = None, sort: str | None = None,
                  skip: int | None = None, limit: int | None = None):
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if search:
        data = [item for item in data if search.lower() in getattr(item, key).lower()]

    if sort and (sort.lower().startswith("asc") or sort.lower().startswith("desc")):
        reverse = sort.lower().startswith("desc")
        data.sort(key=lambda x: getattr(x, key).lower(), reverse=reverse)

    if skip:
        data = data[skip:]

    if limit:
        data = data[:limit]
    return data
