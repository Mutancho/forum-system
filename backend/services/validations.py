from enum import Enum


class UpdateStatus(Enum):
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    SAME_NAME = "same_name"