import sqlalchemy.orm as _orm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Iterator
import fastapi as _fastapi
import inspect
import logging
import src.models as _models
import src.schemas as _schemas
import src.repositories as _repositories
import src.services as _services
import src.config.config_trace as _tracer
from src.config.config_hashing import Hash
import src.config.config_logging as _logger


class UserService(_services.BaseService):
    logger: logging.Logger = _logger.get_logger()

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def get_users(cls, db: AsyncSession, skip: int = 0, limit: int = 100):  # -> Iterator[_schemas.User]:  # _orm.Session
        cls.logger.info(msg="get_users")
        with _tracer.tracer.start_as_current_span(f"{cls.__name__}.{inspect.stack()[0][3]}") as span:
            span.set_attribute("parametro_skip", skip)
            span.set_attribute("parametro_limit", limit)
            try:

                span.add_event("parametro_UserRepository.ini")
                rows = await _repositories.UserRepository.get_all(db=db, skip=skip, limit=limit)
                span.add_event("parametro_UserRepository.fim")

                users = []
                posts = []
                ult_id_user = ""
                user = None

                for row in rows:

                    span.add_event("row", {"id": row["id"]})

                    if ult_id_user == "":
                        ult_id_user = row["id"]

                    if ult_id_user != row["id"]:
                        users.append(user)
                        ult_id_user = row["id"]
                        posts = []

                    if row["id_post"]:
                        post = _schemas.Post(id_post=int(row["id_post"]), owner_id=int(row["owner_id"]), title=str(row["title"]), content=str(row["content"]))
                        posts.append(post)

                    user = _schemas.User(id=int(row["id"]), email=str(row["email"]), is_active=True if row["is_active"] else False, posts=posts)

                users.append(user)

                # users = [Song(name=song.name, artist=song.artist, id=song.id) for song in songs]

                return users

            except Exception as e:
                span.record_exception(e)
                raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def get_user(cls, db: _orm.Session, user_id: int) -> _models.UserModel:
        with _tracer.tracer.start_as_current_span(f"{cls.__name__}.{inspect.stack()[0][3]}") as span:
            span.set_attribute("parametro_user_id", user_id)
            try:
                db_user = await _repositories.UserRepository.get_by_id(db, user_id)
                if db_user is None:
                    raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail="sorry this user does not exist")
                return db_user
            except Exception as e:
                span.record_exception(e)
                raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def get_user_by_email(cls, db: _orm.Session, email: str) -> _models.UserModel:
        with _tracer.tracer.start_as_current_span(f"{cls.__name__}.{inspect.stack()[0][3]}") as span:
            span.set_attribute("parametro_email", email)
            try:
                return await _repositories.UserRepository.get_by_email(db, email)
            except Exception as e:
                span.record_exception(e)
                raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def create_user(cls, db: _orm.Session, user: _schemas.UserCreate) -> _models.UserModel:
        with _tracer.tracer.start_as_current_span(f"{cls.__name__}.{inspect.stack()[0][3]}") as span:
            span.set_attribute("parametro_user", user)
            try:
                db_user = await _services.UserService.get_user_by_email(db=db, email=user.email)
                if db_user:
                    raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail="woops the email is in use")
                new_user = _models.UserModel(email=user.email, hashed_password=Hash.bcrypt(user.password))
                return await _repositories.UserRepository.create(db, new_user)
            except Exception as e:
                span.record_exception(e)
                raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def update_user(cls, db: _orm.Session, user: _schemas.UserCreate, user_id: int) -> _models.UserModel:
        with _tracer.tracer.start_as_current_span(f"{cls.__name__}.{inspect.stack()[0][3]}") as span:
            span.set_attribute("parametro_user_id", user_id)
            span.set_attribute("parametro_user", user)
            try:
                db_user = await _repositories.UserRepository.get_by_id(db, user_id)
                if user.email:
                    db_user.email = user.email
                if user.password:
                    db_user.hashed_password = Hash.bcrypt(user.password)
                return await _repositories.UserRepository.update(db, db_user)
            except Exception as e:
                span.record_exception(e)
                raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def delete_user(cls, db: _orm.Session, user_id: int):  # -> dict[str, str]:
        with _tracer.tracer.start_as_current_span(f"{cls.__name__}.{inspect.stack()[0][3]}") as span:
            span.set_attribute("parametro_user_id", user_id)
            try:
                db_user = await _repositories.UserRepository.get_by_id(db, user_id)
                if db_user is None:
                    raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
                await _repositories.UserRepository.delete_by_id(db, db_user)
                # return {"message": f"successfully deleted user with id: {user_id}"}
                return _schemas.StandardOutput(message=f"successfully deleted user with id: {user_id}")
            except Exception as e:
                span.record_exception(e)
                raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
