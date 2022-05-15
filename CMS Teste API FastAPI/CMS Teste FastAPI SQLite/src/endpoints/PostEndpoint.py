from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import src.services as _services
import src.schemas as _schemas
import src.database as _database


router = _fastapi.APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[_schemas.Post])
async def read_posts(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        return await _services.PostService.get_posts(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{post_id}", response_model=_schemas.Post)
async def read_post(post_id: int, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        post = await _services.PostService.get_post(db=db, post_id=post_id)
        if post is None:
            raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail="sorry this post does not exist")
        return post
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{post_id}", status_code=_fastapi.status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        await _services.PostService.delete_post(db=db, post_id=post_id)
        return {"message": f"successfully deleted post with id: {post_id}"}
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{post_id}", response_model=_schemas.Post, status_code=_fastapi.status.HTTP_202_ACCEPTED)
async def update_post(post_id: int, post: _schemas.PostCreate, db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        return await _services.PostService.update_post(db=db, post=post, post_id=post_id)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
