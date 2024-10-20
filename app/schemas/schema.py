import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class UserGet(BaseModel):
    id: int = ""
    gender: int = ""
    age: int = ""
    country: str = ""
    city: str = ""
    exp_group: int = ""
    os: str = ""
    source: str =  ""

    class Config:
        orm_mode = True


class PostGet(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True


class Response(BaseModel):
    exp_group: str
    recommendations: List[PostGet]

class FeedGet(BaseModel):
    user_id: int = ""
    post_id: int = ""
    action: str = ""
    time: datetime.datetime = ""
    user: UserGet
    post: PostGet

    class Config:
        orm_mode = True