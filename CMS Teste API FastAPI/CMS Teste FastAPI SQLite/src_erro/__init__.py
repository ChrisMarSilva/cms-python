from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .containers.UserContainer import UserContainer
# from .endpoints.UserEndpoint import router as UserEndpoint
from . import containers
from . import endpoints

def create_app() -> FastAPI:

    container = containers.UserContainer()
    #container.wire(modules=[endpoints.router])

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    app.add_middleware(CORSMiddleware, allow_origins=["http://localhost.tiangolo.com", "https://localhost.tiangolo.com", "http://localhost", "http://localhost:5001", ], allow_credentials=True, allow_methods=["*"], allow_headers=["*"], )
    app.include_router(endpoints.router)

    @app.get("/", status_code=200)
    async def root():
        return {"status": "OK"}

    return app


'''

import sys

from dependency_injector.wiring import Provide, inject

from .services import UserService, AuthService, PhotoService
from .containers import Container


@inject
def main(
        email: str,
        password: str,
        photo: str,
        user_service: UserService = Provide[Container.user_service],
        auth_service: AuthService = Provide[Container.auth_service],
        photo_service: PhotoService = Provide[Container.photo_service],
) -> None:
    user = user_service.get_user(email)
    auth_service.authenticate(user, password)
    photo_service.upload_photo(user, photo)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(*sys.argv[1:])


-------------


import sys

from dependency_injector.wiring import Provide, inject

from .services import UserService, AuthService, PhotoService
from .containers import Application


@inject
def main(
        email: str,
        password: str,
        photo: str,
        user_service: UserService = Provide[Application.services.user],
        auth_service: AuthService = Provide[Application.services.auth],
        photo_service: PhotoService = Provide[Application.services.photo],
) -> None:
    user = user_service.get_user(email)
    auth_service.authenticate(user, password)
    photo_service.upload_photo(user, photo)


if __name__ == "__main__":
    application = Application()
    application.core.init_resources()
    application.wire(modules=[__name__])

    main(*sys.argv[1:])

---------------

from fastapi import FastAPI

from .containers import Container
from . import endpoints


def create_app() -> FastAPI:
    container = Container()
    container.config.giphy.api_key.from_env("GIPHY_API_KEY")

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()



-----


from fastapi import FastAPI

from .containers import Container
from . import endpoints


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()
    
'''