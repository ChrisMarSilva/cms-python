from typing import List
import inspect
import os
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import src.services as _services
import src.schemas as _schemas
import src.database as _database
import src.config.config_trace as _tracer
from sqlalchemy.ext.asyncio import AsyncSession


router = _fastapi.APIRouter(prefix="/users", tags=['users'])


@router.get("/", responses={_fastapi.status.HTTP_400_BAD_REQUEST: {'model': _schemas.ErrorOutput}})  # , response_model=List[_schemas.User]
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = _fastapi.Depends(_database.base.get_db_async)):  # _orm.Session # _database.SessionAsync # AsyncSession
    with _tracer.tracer.start_as_current_span(f"{str(os.path.basename(__file__).replace('.py', ''))}.{inspect.stack()[0][3]}") as span:
        span.set_attribute("parametro_skip", skip)
        span.set_attribute("parametro_limit", limit)
        _rows = await _services.UserService.get_users(db=db, skip=skip, limit=limit)
        return _schemas.ResponseSchema(status="Ok", code="200", message="Success fetch all data", result=_rows).dict(exclude_none=True, exclude_unset=True, exclude_defaults=True)


@router.get("/{user_id}", response_model=_schemas.User)
async def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    with _tracer.tracer.start_as_current_span(f"{str(os.path.basename(__file__).replace('.py', ''))}.{inspect.stack()[0][3]}") as span:
        span.set_attribute("parametro_user_id", user_id)
        return await _services.UserService.get_user(db=db, user_id=user_id)


@router.post("/", response_model=_schemas.User)
async def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    with _tracer.tracer.start_as_current_span(f"{str(os.path.basename(__file__).replace('.py', ''))}.{inspect.stack()[0][3]}") as span:
        span.set_attribute("parametro_user", user)
        return await _services.UserService.create_user(db=db, user=user)


@router.put("/", response_model=_schemas.User)
async def update_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    with _tracer.tracer.start_as_current_span(f"{str(os.path.basename(__file__).replace('.py', ''))}.{inspect.stack()[0][3]}") as span:
        span.set_attribute("parametro_user", user)
        return await _services.UserService.update_user(db=db, user=user)


@router.post("/{user_id}/posts/", response_model=_schemas.Post)
async def create_post(user_id: int, post: _schemas.PostCreate, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    with _tracer.tracer.start_as_current_span(f"{str(os.path.basename(__file__).replace('.py', ''))}.{inspect.stack()[0][3]}") as span:
        span.set_attribute("parametro_user_id", user_id)
        return await _services.PostService.create_post(db=db, post=post, user_id=user_id)


@router.delete("/{user_id}", status_code=_fastapi.status.HTTP_204_NO_CONTENT)
async def delete_post(user_id: int, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    with _tracer.tracer.start_as_current_span(f"{str(os.path.basename(__file__).replace('.py', ''))}.{inspect.stack()[0][3]}") as span:
        span.set_attribute("parametro_user_id", user_id)
        return await _services.UserService.delete_user(db=db, user_id=user_id)
