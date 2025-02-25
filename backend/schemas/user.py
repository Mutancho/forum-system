from datetime import date
from pydantic import BaseModel, constr, EmailStr


class User(BaseModel):
    id: int | None = None
    username: str
    email: EmailStr
    password: constr(min_length=6)
    role: str
    created_at: date | None = None

    @classmethod
    def from_query_result(cls, id, username, email, role, created_at, password='*********'):
        return cls(id=id, username=username, email=email, password=password, role=role, created_at=created_at)


class UpdateUser(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=6)


class DisplayUser(BaseModel):
    id: int
    username: str
    email: str

    @classmethod
    def from_query_result(cls, id, username, email, password, role, created_at):
        return cls(id=id, username=username, email=email)


class UsernameLogin(BaseModel):
    username: str
    password: str


class EmailLogin(BaseModel):
    email: EmailStr
    password: str


class Member(BaseModel):
    user_id: int
    category_id: int
    read_access: bool
    write_access: bool


class RevokeMemberAccess(BaseModel):
    user_id: int
    category_id: int
