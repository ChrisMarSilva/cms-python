from typing import Iterator
import inspect
import sqlalchemy.orm as _orm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import text
import src.models as _models
import src.config.config_trace as _tracer


class UserRepository:

    # def __init__(self) -> None:
    #     ...

    @classmethod
    async def get_all(cls, db: AsyncSession, skip: int, limit: int):  # -> Iterator[_models.UserModel]:  # _orm.Session
        with _tracer.tracer.start_as_current_span(f"{cls.__name__}.{inspect.stack()[0][3]}") as span:
            span.set_attribute("parametro_skip", skip)
            span.set_attribute("parametro_limit", limit)

            # Sync
            # user_bd = db.query(_models.UserModel).order_by(_models.UserModel.id).offset(skip).limit(limit).all()
            # user_bd = db.query(_models.UserModel, _models.PostModel).join(_models.PostModel, _models.UserModel.id == _models.PostModel.owner_id, isouter=True).offset(skip).limit(limit).all()
            # user_bd = db.query(_models.UserModel, _models.UserModel.id.label("id"), _models.UserModel.email.label("email"), _models.UserModel.hashed_password.label("hashed_password"), _models.UserModel.is_active.label("is_active"),  _models.PostModel, _models.PostModel.id.label("id_post"), _models.PostModel.title.label("title"), _models.PostModel.content.label("content"),  _models.PostModel.owner_id.label("owner_id"), _models.PostModel.date_created.label("date_created"), _models.PostModel.date_last_updated.label("date_last_updated")).select_from(_orm.outerjoin(_models.UserModel, _models.PostModel)).offset(skip).limit(limit).all()

            # Async
            # result = await db.execute(select(_models.UserModel, _models.PostModel).join(_models.PostModel, _models.UserModel.id == _models.PostModel.owner_id, isouter=True).order_by(_models.UserModel.id).offset(skip).limit(limit))
            # user_bd = result.scalars().all()

            #stmt = select(_models.UserModel, _models.PostModel).join(_models.PostModel, _models.UserModel.id == _models.PostModel.owner_id, isouter=True).order_by(_models.UserModel.id).offset(skip).limit(limit).options(_orm.selectinload(_models.UserModel.posts))
            # stmt = select(_models.UserModel, _models.PostModel).join(_models.PostModel, isouter=True).order_by(_models.UserModel.id).offset(skip).limit(limit)
            # result = await db.execute(statement=stmt, params=None)
            # user_bd = result.scalars().all()

            #stmt = text('SELECT COUNT(1) AS QTDE, MAX(id) AS MAXIMO, MIN(id) AS MINIMO FROM users')
            stmt = text('SELECT users.id, users.email, users.hashed_password, users.is_active, posts.id AS id_post, posts.title, posts.content, posts.owner_id, posts.date_created, posts.date_last_updated FROM users LEFT JOIN posts ON (users.id = posts.owner_id) ORDER BY users.id LIMIT 100 OFFSET 0')
            result = await db.execute(statement=stmt)
            rows = result.fetchall()
            result.close()

            return rows

    @classmethod
    async def get_by_id(cls, db: _orm.Session, user_id: int) -> _models.UserModel:
        return db.query(_models.UserModel).filter(_models.UserModel.id == user_id).first()

    @classmethod
    async def get_by_email(cls, db: _orm.Session, email: str) -> _models.UserModel:
        return db.query(_models.UserModel).filter(_models.UserModel.email == email).first()

    @classmethod
    async def count(cls, db: _orm.Session) -> int:
        return db.query(_models.UserModel).count()

    @classmethod
    async def create(cls, db: _orm.Session, user: _models.UserModel) -> _models.UserModel:
        db.add(user)
        db.commit()
        db.refresh(user)
        # db.add(user)
        # await db.flush()
        return user

    @classmethod
    async def update(cls, db: _orm.Session, user: _models.UserModel) -> _models.UserModel:
        db.commit()
        db.refresh(user)
        # q = update(_models.UserModel).where(_models.UserModel.id == user.id)
        # if name: q = q.values(name=user.name)
        # q.execution_options(synchronize_session="fetch")
        # await  self.db_session.execute(q)
        return user

    @classmethod
    async def delete_by_id(cls, db: _orm.Session, user: _models.UserModel) -> None:
        db.delete(user)
        # db.query(_models.PostModel).filter(_models.UserModel.id == user.id).delete()
        db.commit()
