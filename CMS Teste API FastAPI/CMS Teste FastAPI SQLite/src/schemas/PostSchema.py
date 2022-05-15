import datetime as _dt
import pydantic as _pydantic
from typing import Optional


class _PostBase(_pydantic.BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(_PostBase):
    pass


class Post(_PostBase):
    id_post: Optional[int] = _pydantic.Field(alias='id')
    owner_id: Optional[int] = None
    date_created: Optional[_dt.datetime] = None
    date_last_updated: Optional[_dt.datetime] = None
    class Config:
        orm_mode = True
