'''

import logging.config
import sqlite3

import boto3
from dependency_injector import containers, providers

from . import services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    # Gateways

    database_client = providers.Singleton(
        sqlite3.connect,
        config.database.dsn,
    )

    s3_client = providers.Singleton(
        boto3.client,
        service_name="s3",
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key,
    )

    # Services

    user_service = providers.Factory(
        services.UserService,
        db=database_client,
    )

    auth_service = providers.Factory(
        services.AuthService,
        db=database_client,
        token_ttl=config.auth.token_ttl.as_int(),
    )

    photo_service = providers.Factory(
        services.PhotoService,
        db=database_client,
        s3=s3_client,
    )
    

------------


import logging.config
import sqlite3

import boto3
from dependency_injector import containers, providers

from . import services


class Core(containers.DeclarativeContainer):

    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration()

    database_client = providers.Singleton(
        sqlite3.connect,
        config.database.dsn,
    )

    s3_client = providers.Singleton(
        boto3.client,
        service_name="s3",
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key,
    )


class Services(containers.DeclarativeContainer):

    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    user = providers.Factory(
        services.UserService,
        db=gateways.database_client,
    )

    auth = providers.Factory(
        services.AuthService,
        db=gateways.database_client,
        token_ttl=config.auth.token_ttl.as_int(),
    )

    photo = providers.Factory(
        services.PhotoService,
        db=gateways.database_client,
        s3=gateways.s3_client,
    )


class Application(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    core = providers.Container(
        Core,
        config=config.core,
    )

    gateways = providers.Container(
        Gateways,
        config=config.gateways,
    )

    services = providers.Container(
        Services,
        config=config.services,
        gateways=gateways,
    )

---------------

from dependency_injector import containers, providers

from . import giphy, services


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])

    giphy_client = providers.Factory(
        giphy.GiphyClient,
        api_key=config.giphy.api_key,
        timeout=config.giphy.request_timeout,
    )

    search_service = providers.Factory(
        services.SearchService,
        giphy_client=giphy_client,
    )
-----



from dependency_injector import containers, providers

from .database import Database
from .repositories import UserRepository
from .services import UserService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])

    db = providers.Singleton(Database, db_url=config.db.url)

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

'''