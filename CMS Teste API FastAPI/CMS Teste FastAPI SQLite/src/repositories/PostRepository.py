from typing import Iterator
import inspect
import sqlalchemy.orm as _orm
import src.models as _models
import src.config.config_trace as _tracer


class PostRepository:

    # def __init__(self) -> None:
    #     ...

    @classmethod
    async def get_all(cls, db: _orm.Session, skip: int, limit: int) -> Iterator[_models.PostModel]:
        with _tracer.tracer.start_as_current_span(f"{cls.__name__}.{inspect.stack()[0][3]}") as span:
            span.set_attribute("parametro_skip", skip)
            span.set_attribute("parametro_limit", limit)
            return db.query(_models.PostModel).offset(skip).limit(limit).all()

    @classmethod
    async def get_by_id(cls, db: _orm.Session, post_id: int) -> _models.PostModel:
        with _tracer.tracer.start_as_current_span(f"{__name__}.{cls.__class__.__name__}") as span:
            span.set_attribute("post_id", post_id)
            return db.query(_models.PostModel).filter(_models.PostModel.id == post_id).first()

    @classmethod
    async def create(cls, db: _orm.Session, post: _models.PostModel) -> _models.PostModel:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @classmethod
    async def update(cls, db: _orm.Session, post: _models.PostModel) -> _models.PostModel:
        db.commit()
        db.refresh(post)
        return post

    @classmethod
    async def delete_by_id(cls, db: _orm.Session, post: _models.PostModel) -> None:
        db.delete(post)
        db.commit()
