from typing import Union
from pydantic import BaseModel, Field


class Item(BaseModel):
    title: str
    description: Union[str, None] = None


class UserBase(BaseModel):
    email: str = Field(pattern=r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$', examples=["joe@example.com"])


class UserCreate(UserBase):
    password: str = Field(examples=["secret"])


class User(UserBase):
    key: str
    items: list[Item] = []


class UserList(BaseModel):
    users: list[User] = []
    last: Union[str, None] = None
