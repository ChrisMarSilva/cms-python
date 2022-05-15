


#
# from datetime import datetime
# from typing import Any, Optional
#
# from pydantic import BaseModel, StrictBool, validator
#
#
# class PostBase(BaseModel):
#     title: str
#     body: str
#     summary: str
#
#
# class PostCreate(PostBase):
#     @validator("title")
#     def validate_title(cls: Any, title: str, **kwargs: Any) -> Any:
#         if len(title) == 0:
#             raise ValueError("Title can't be empty")
#         elif len(title) > 100:
#             raise ValueError("Title is too long")
#         return title
#
#     @validator("summary")
#     def validate_summary(cls: Any, summary: str, **kwargs: Any) -> Any:
#         if len(summary) == 0:
#             raise ValueError("Summary can't be empty")
#         elif len(summary) > 200:
#             raise ValueError("Summary is too long")
#         return summary
#
#     @validator("body")
#     def validate_body(cls: Any, body: str, **kwargs: Any):
#         if len(body) == 0:
#             raise ValueError("Body can't be empty")
#         return body
#
#
# class PostInDB(PostBase):
#     title: str
#     body: str
#     summary: str
#     id: Optional[int] = None
#     published_at: Optional[datetime] = None
#     slug: Optional[str] = None
#     author_id: Optional[str] = None
#
#     class Config:
#         orm_mode: bool = True
#
#
# class Posts(PostInDB):
#     pass
#
#
# class PostUpdate(PostBase):
#     # id: int
#     author_id: str
'''

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


# from typing import Any, Optional
#
# from pydantic import BaseModel, StrictBool, validator
#
# from app.db.session import Base
#
#
# class UserBase(BaseModel):
#     username: str
#     profile: str
#     email: str
#     disabled: StrictBool = False
#
#
# class UserCreate(UserBase):
#     password: str
#
#     @validator("username")
#     def validate_username(cls: Any, username: str, **kwargs: Any) -> Any:
#         if len(username) <= 4:
#             raise ValueError("Username can't be empty")
#         return username
#
#     @validator("email")
#     def validate_email(cls: Any, email: str, **kwargs: Any) -> Any:
#         if len(email) == 0:
#             raise ValueError("An email is required")
#         return email
#
#     @validator("profile")
#     def validate_profile(cls: any, profile: str, **kwargs: Any) -> Any:
#         if len(profile) == 0:
#             raise ValueError("A profile is required")
#         return profile
#
#
# class User(UserBase):
#     id: Optional[int] = None
#
#     class Config:
#         orm_mode: bool = True
#
#
# class UserInDB(User):
#     hashed_password: str
#
#
# class Users(User):
#     id: int
#
#
# class UserUpdate(UserBase):
#     password: Optional[str]
#
#     class Config:
#         orm_mode: bool = True
#
#
# class UserPassword(BaseModel):
#     password: Optional[str] = None
#     # pass

'''