from typing import  Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar('T')


class HTTPError(BaseModel):
    detail: str


class ResponseSchema(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
