from typing import List, Optional
import pydantic as _pydantic
from src.schemas.PostSchema import Post


class _UserBase(_pydantic.BaseModel):
    email: Optional[str] = None


class UserCreate(_UserBase):
    password: Optional[str] = None


class User(_UserBase):
    username: Optional[str] = None
    id: Optional[int] = None
    is_active: Optional[bool] = None
    posts: Optional[List[Post]] = []
    disabled: bool | None = None

    class Config:
        orm_mode = True


class Login(_pydantic.BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "username",
                "password": "password",
            }
        }

class UserInDB(User):
    hashed_password: str
