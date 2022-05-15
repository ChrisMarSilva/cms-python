import sqlalchemy.orm as _orm
import fastapi as _fastapi
from typing import Iterator
import src.models as _models
import src.schemas as _schemas
import src.repositories as _repositories
import src.services as _services


class PostService(_services.BaseService):

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def get_posts(cls, db: _orm.Session, skip: int = 0, limit: int = 100) -> Iterator[_models.PostModel]:
        #self.logger.debug("get_posts")
        return await _repositories.PostRepository.get_all(db, skip, limit)

    @classmethod
    async def get_post(cls, db: _orm.Session, post_id: int) -> _models.PostModel:
        #self.logger.debug("get_post")
        return await _repositories.PostRepository.get_by_id(db, post_id)

    @classmethod
    async def create_post(cls, db: _orm.Session, post: _schemas.PostCreate, user_id: int) -> _models.PostModel:
        #self.logger.debug("create_post")
        try:
            db_user = await _services.UserService.get_user(db=db, user_id=user_id)
            if db_user is None:
                raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail="sorry this user does not exist")
            new_post = _models.PostModel(title=post.title, content=post.content, owner_id=user_id)
            return await _repositories.PostRepository.create(db, new_post)
        except Exception as e:
            raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @classmethod
    async def update_post(cls, db: _orm.Session, post: _schemas.PostCreate, post_id: int) -> _models.PostModel:
        #self.logger.debug("update_post")
        db_post = await _repositories.PostRepository.get_by_id(db, post_id)
        db_post.title = post.title
        db_post.content = post.content
        return await _repositories.PostRepository.update(db, db_post)

    @classmethod
    async def delete_post(cls, db: _orm.Session, post_id: int) -> None:
        #self.logger.debug("delete_post")
        db_post = await _repositories.PostRepository.get_by_id(db, post_id)
        return await _repositories.PostRepository.delete_by_id(db, db_post)
