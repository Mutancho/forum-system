from enum import Enum


class UpdateStatus(Enum):
    DUPLICATE_ENTRY = "Already Exists"
    SUCCESS = "Success"
    NOT_FOUND = "Not found"
    NO_CHANGE = "No change"
    LOCKED = "Locked"
    NO_WRITE_ACCESS = "No write access"
    NO_READ_ACCESS = "No read access"
    BAD_REQUEST = "Bad request"
    ADMIN_REQUIRED = "Requires Admin Access!"
