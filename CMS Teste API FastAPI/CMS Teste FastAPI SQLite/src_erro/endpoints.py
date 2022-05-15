from fastapi import APIRouter, Depends, Response, status, HTTPException
# from typing import Optional,List
from dependency_injector.wiring import inject, Provide
from .containers import UserContainer
from .services import UserService
from .repositories import NotFoundError
# from .models import UserModel


router = APIRouter(prefix="/users")


@router.get("/", status_code=status.HTTP_200_OK)  # response_model=List[UserModel],
@inject
async def get_list(user_service: UserService = Depends(Provide[UserContainer.user_service])):
    try:
        return user_service.get_users()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))  # return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="ddddddddd")


@router.get("/{user_id}", status_code=status.HTTP_200_OK)  # response_model=UserModel,
@inject
async def get_by_id(user_id: int, user_service: UserService = Depends(Provide[UserContainer.user_service])):
    try:
        return await user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)  # response_model=UserModel,
@inject
async def add(user_service: UserService = Depends(Provide[UserContainer.user_service])):
    try:
        return await user_service.create_user()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{user_id}", status_code=status.HTTP_200_OK)  # response_model=models.UserModel,
@inject
async def update(user_id: int, user_service: UserService = Depends(Provide[UserContainer.user_service])):  # -> UserModel:
    try:
        return await user_service.update_user(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove(user_id: int, user_service: UserService = Depends(Provide[UserContainer.user_service])):
    try:
        await user_service.delete_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


'''


from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from .services import SearchService
from .containers import Container


class Gif(BaseModel):
    url: str


class Response(BaseModel):
    query: str
    limit: int
    gifs: List[Gif]


router = APIRouter()


@router.get("/", response_model=Response)
@inject
async def index(
        query: Optional[str] = None,
        limit: Optional[str] = None,
        default_query: str = Depends(Provide[Container.config.default.query]),
        default_limit: int = Depends(Provide[Container.config.default.limit.as_int()]),
        search_service: SearchService = Depends(Provide[Container.search_service]),
):
    query = query or default_query
    limit = limit or default_limit

    gifs = await search_service.search(query, limit)

    return {
        "query": query,
        "limit": limit,
        "gifs": gifs,
    }


--------------- 


from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from .containers import Container
from .services import UserService
from .repositories import NotFoundError

router = APIRouter()


@router.get("/users")
@inject
def get_list(
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.get_users()


@router.get("/users/{user_id}")
@inject
def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        return user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/users", status_code=status.HTTP_201_CREATED)
@inject
def add(
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.create_user()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        user_service.delete_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/status")
def get_status():
    return {"status": "OK"}



from datetime import timedelta
from typing import Any, List, Optional

from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.api import response
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app import schemas
from app.services import (
    authenticate_user,
    create_access_token,
    create_user,
    get_current_active_user,
    get_db,
    get_posts_by_userid,
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    get_users,
    update_user,
)
from app.services.security import ACCESS_TOKEN_EXPIRE_MINUTES

router: Any = APIRouter(
    tags=["users"],
    responses={404: {"Description": "Not found"}},
)


@router.post(
    "/users",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
)
def create_new_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> Any:
    db_username = get_user_by_username(db, username=user.username)
    db_email = get_user_by_email(db, email=user.email)
    if db_username:
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )
    elif db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@router.get(
    "/users",
    response_model=Page[schemas.Users],
    dependencies=[Depends(pagination_params)],
)
def list_users(db: Session = Depends(get_db)) -> List:
    """
    List all users
    """
    users = get_users(db=db)
    return paginate(users)


@router.get("/users/user", response_model=schemas.User)
def read_user(
    username: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get data about user
    """
    if username:
        db_user = get_user_by_username(db=db, username=username)
    elif user_id:
        db_user = get_user_by_id(db=db, user_id=user_id)
    else:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response = None,  # noqa
) -> Any:
    """
    Generate a token to access endpoints
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token_data = {"access_token": access_token, "token_type": "bearer"}
    response.set_cookie(
        key="token",
        value=access_token,
        max_age=access_token_expires.total_seconds(),
        httponly=True,
    )
    return token_data


@router.get(
    "/users/me/posts",
    response_model=Page[schemas.Posts],
    dependencies=[Depends(pagination_params)],
)
def read_own_posts(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> List:
    """
    Get own posts
    """
    user_id = current_user.id
    user_posts = get_posts_by_userid(db, user_id)
    return paginate(user_posts)


@router.put(
    "/users/{username}",
    response_model=schemas.User,
    response_model_exclude_none=True,
)
def update_user_data(
    username: str,
    user: schemas.user.UserUpdate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    The password field is optional
    """
    if username != current_user.username:
        raise HTTPException(status_code=403, detail="Don't have permission")

    result = update_user(db, user, username)

    return result

'''



'''
from http import HTTPStatus
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app import schemas
from app.services import (
    count_posts,
    create_post,
    delete_post,
    get_all_posts,
    get_current_active_user,
    get_db,
    get_post,
    get_posts_by_userid,
    get_user_by_id,
)
from app.services.posts import update_post

router: Any = APIRouter(
    tags=["posts"],
    responses={404: {"Description": "Not found"}},
)


@router.post(
    "/posts",
    response_model=schemas.PostInDB,
    status_code=status.HTTP_201_CREATED,
)
def create_user_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
) -> Any:
    """
    Create a post, needs the user is logged
    """
    result = create_post(db=db, post=post, current_user=current_user)
    return result


@router.get("/posts/{slug}", response_model=schemas.Posts)
def read_slug(slug: str, db: Session = Depends(get_db)) -> Any:
    """
    Get a post by slug
    """
    db_slug = get_post(db, slug)
    if db_slug is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_slug


@router.get(
    "/posts",
    response_model=Page[schemas.Posts],
    dependencies=[Depends(pagination_params)],
)
def list_posts(
    response: Response,
    db: Session = Depends(get_db),
    user_id: Optional[int] = None,
) -> Any:
    """
    List all post published
    """
    db_user = ""
    if user_id:
        db_user = get_user_by_id(db=db, user_id=user_id)
        print(db_user)
        if db_user:
            posts = get_posts_by_userid(db=db, user_id=user_id)
    else:
        posts = get_all_posts(db=db)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    total_posts = count_posts(db=db)
    response.headers["X-Total-Posts"] = str(total_posts)

    return paginate(posts)


@router.put("/posts/{slug}", response_model=schemas.PostInDB)
def update_user_post(
    slug: str,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
) -> Any:
    """
    Update a user Post if its owner
    """
    post_data = get_post(db, slug)
    if post_data is None:
        raise HTTPException(status_code=404, detail="Don't find post")
    elif post_data.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Don't have permission")
    req_post = update_post(db=db, slug=slug, post=post)
    return req_post


@router.delete("/posts/{slug}", status_code=HTTPStatus.NO_CONTENT)
def post_delete(
    slug: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
) -> Any:
    """
    Delete a user post if its owner
    """
    post_data = get_post(db, slug)
    if post_data is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post_data.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Don't have permission")
    delete_post(db, slug)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
'''