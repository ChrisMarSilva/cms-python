from typing import TypeVar, List, Optional
from mongoengine import Document, StringField, IntField, ListField, DateTimeField
from pydantic import BaseModel
import datetime as dt


T = TypeVar('T')


class BlogPost(Document):
    title = StringField(required=True, max_length=200)
    posted = DateTimeField(default=dt.datetime.utcnow)
    tags = ListField(StringField(max_length=50))
    meta = {'allow_inheritance': True, "collection": "blog-post"}
    # meta = {"db_alias": "dbworkouts"}


class TextPost(BlogPost):
    content = StringField(required=True)


class LinkPost(BlogPost):
    url = StringField(required=True)


class EmployeeIn(BaseModel):
    id: Optional[str] = None
    nome: str
    age: int
    teams: List[str] = []


class Employee(Document):
    nome: StringField(required=True, max_length=100) 
    age: IntField(default=0)
    teams: ListField(StringField(max_length=50))
    meta = {'allow_inheritance': True, "collection": "employee"}
    # meta = {"db_alias": "dbworkouts"}


class Response(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None
