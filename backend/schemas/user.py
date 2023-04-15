from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    id: int | None
    username: str
    email: str
    password: str
    role: str
    created_at: date | None

    @classmethod
    def from_query_result(cls, id, username, email, password, role,created_at):
        return cls(id=id,username=username,email=email,password=password,role=role,created_at=created_at)

class DisplayUser(BaseModel):
    id: int
    username: str
    email: str

    @classmethod
    def from_query_result(cls, id, username, email, password, role, created_at):
        return cls(id=id, username=username, email=email)