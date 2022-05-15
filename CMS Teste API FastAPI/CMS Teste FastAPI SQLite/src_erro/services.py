from uuid import uuid4
from typing import Iterator
from .repositories import UserRepository
from .models import UserModel


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    async def get_users(self) -> Iterator[UserModel]:
        return await self._repository.get_all()

    async def get_user_by_id(self, user_id: int) -> UserModel:
        return await self._repository.get_by_id(user_id)

    async def create_user(self) -> UserModel:
        uid = uuid4()
        return await self._repository.add(email=f"{uid}@email.com", password="pwd")

    async def update_user(self, user_id: int) -> UserModel:
        user = await self._repository.get_by_id(user_id)
        user.email = "novo@email.com"
        return await self._repository.update(user=user)

    async def delete_user_by_id(self, user_id: int) -> None:
        return await self._repository.delete_by_id(user_id)



    # with _orm.Session(bind=db.bind) as session:
    #     b1 = session.query(_models.UserModel, _models.PostModel).join(_models.PostModel, _models.UserModel.id == _models.PostModel.owner_id, isouter=True).offset(skip).limit(limit).all()
    # print("b1", b1)
    # b1_schema = _schemas.User.from_orm(b1)
    # print("b1_schema", b1_schema.json())
    # b1_lista = list(map(_schemas.User.from_orm, b1))
    # print("b1_lista", b1_lista)
    # db_user = await _repositories.UserRepository.get_all(db, skip, limit)
    # schema_user = _schemas.User.from_orm(db_user)
    # list(schema_user)  # schema_user.json()  # schema_user.dict()
    # db_user = await _repositories.UserRepository.get_all(db, skip, limit)
    # print("db_user", db_user)
    # schema_user = _schemas.User.from_orm(db_user)
    # print("schema_user", schema_user)
    # try:
    #     print("schema_user.json", schema_user.json())
    # except:
    #     print("schema_user.json erro")
    # try:
    #     print("schema_user.dict", schema_user.dict())
    # except:
    #     print("schema_user.dict erro")
    # lista_user = list(map(_schemas.User.from_orm, db_user))
    # print("lista_user", lista_user)


'''

import logging

import sqlite3
from typing import Dict

from mypy_boto3_s3 import S3Client


class BaseService:

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )


class UserService(BaseService):

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        super().__init__()

    def get_user(self, email: str) -> Dict[str, str]:
        self.logger.debug("User %s has been found in database", email)
        return {"email": email, "password_hash": "..."}


class AuthService(BaseService):

    def __init__(self, db: sqlite3.Connection, token_ttl: int) -> None:
        self.db = db
        self.token_ttl = token_ttl
        super().__init__()

    def authenticate(self, user: Dict[str, str], password: str) -> None:
        assert password is not None
        self.logger.debug(
            "User %s has been successfully authenticated",
            user["email"],
        )


class PhotoService(BaseService):

    def __init__(self, db: sqlite3.Connection, s3: S3Client) -> None:
        self.db = db
        self.s3 = s3
        super().__init__()

    def upload_photo(self, user: Dict[str, str], photo_path: str) -> None:
        self.logger.debug(
            "Photo %s has been successfully uploaded by user %s",
            photo_path,
            user["email"],
        )

-------------

import logging
import sqlite3
from typing import Dict

from mypy_boto3_s3 import S3Client


class BaseService:

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )


class UserService(BaseService):

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db
        super().__init__()

    def get_user(self, email: str) -> Dict[str, str]:
        self.logger.debug("User %s has been found in database", email)
        return {"email": email, "password_hash": "..."}


class AuthService(BaseService):

    def __init__(self, db: sqlite3.Connection, token_ttl: int) -> None:
        self.db = db
        self.token_ttl = token_ttl
        super().__init__()

    def authenticate(self, user: Dict[str, str], password: str) -> None:
        assert password is not None
        self.logger.debug(
            "User %s has been successfully authenticated",
            user["email"],
        )


class PhotoService(BaseService):

    def __init__(self, db: sqlite3.Connection, s3: S3Client) -> None:
        self.db = db
        self.s3 = s3
        super().__init__()

    def upload_photo(self, user: Dict[str, str], photo_path: str) -> None:
        self.logger.debug(
            "Photo %s has been successfully uploaded by user %s",
            photo_path,
            user["email"],
        )


-----------

from uuid import uuid4
from typing import Iterator

from .repositories import UserRepository
from .models import User


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self) -> Iterator[User]:
        return self._repository.get_all()

    def get_user_by_id(self, user_id: int) -> User:
        return self._repository.get_by_id(user_id)

    def create_user(self) -> User:
        uid = uuid4()
        return self._repository.add(email=f"{uid}@email.com", password="pwd")

    def delete_user_by_id(self, user_id: int) -> None:
        return self._repository.delete_by_id(user_id)

'''