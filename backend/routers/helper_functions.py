from enum import Enum
from services.validations import UpdateStatus
from fastapi import HTTPException, status


class Constants(Enum):
    CATEGORY = "Category"
    TOPIC = "Topic"
    REPLY = "Reply"
    READ = "read"
    WRITE = "write"
    GRANTED = 1
    REVOKED = 0


def query_filters(data, key: str, search: str | None = None, sort: str | None = None,
                  skip: int | None = None, limit: int | None = None):
    if not data:
        raise UpdateStatus.NOT_FOUND

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


def http_validations(data, info_type: Constants):
    if data == UpdateStatus.SUCCESS:
        return UpdateStatus.SUCCESS
    if data == UpdateStatus.NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{info_type} not found")
    if data == UpdateStatus.NO_CHANGE:
        return UpdateStatus.NO_CHANGE
    if data == UpdateStatus.LOCKED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{info_type} is locked")
    if data == UpdateStatus.NO_WRITE_ACCESS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{info_type} write access denied")
    if data == UpdateStatus.NO_READ_ACCESS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{info_type} read access denied")
    if data == UpdateStatus.BAD_REQUEST:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create {info_type}")
    if data == UpdateStatus.ADMIN_REQUIRED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=UpdateStatus.ADMIN_REQUIRED)
    if data == UpdateStatus.DUPLICATE_ENTRY:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Entry already exists")
    return data
