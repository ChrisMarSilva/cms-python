import os
from dependency_injector import containers, providers
from .database import Database
from .repositories import UserRepository
from .services import UserService

class UserContainer(containers.DeclarativeContainer):

    #wiring_config = containers.WiringConfiguration(modules=["..endpoints"])

    # config = providers.Configuration(yaml_files=["config.yml"])
    # db = providers.Singleton(Database, db_url=config.db.url)

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    conn_str = 'sqlite:///' + os.path.join(BASE_DIR, 'books.db')

    SQLALCHEMY_DATABASE_URL = "sqlite:///./webapp.db"  # "sqlite:///./webapp.db"
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

    config = providers.Configuration()
    db = providers.Singleton(Database, db_url=SQLALCHEMY_DATABASE_URL)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    user_service = providers.Factory(UserService, user_repository=user_repository)


# https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi-sqlalchemy/webapp/containers.py