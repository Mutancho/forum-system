from services.validations import UpdateStatus
from fastapi import HTTPException, status


def handle_category_updates(update_status: UpdateStatus):
    if update_status == UpdateStatus.NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    elif update_status == UpdateStatus.NO_CHANGE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already in the desired state")
    return update_status
