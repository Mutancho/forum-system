from enum import Enum


class UpdateStatus(Enum):
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    NO_CHANGE = "no_change"
