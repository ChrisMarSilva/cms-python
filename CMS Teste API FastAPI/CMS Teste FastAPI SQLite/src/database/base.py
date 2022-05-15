from typing import Generator
from src.database.session import SessionLocal, SessionAsync
from sqlalchemy.ext.asyncio import AsyncSession


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_db_async() -> AsyncSession:
    async with SessionAsync() as session:
    # async with session.begin():
        yield session
        
'''
from typing import Generator  # AsyncGenerator
from src.database.session import SessionLocal  # , SessionAsync
# from sqlalchemy.ext.asyncio import AsyncSession




# async def get_db_async() -> AsyncGenerator[AsyncSession, None]:  # -> AsyncSession:
#     async with async_session_maker() as session:
#         yield session
#     async with SessionAsync() as session:
#         # async with session.begin():
#         yield session

#
# class DBContext:
#
#     def __init__(self):
#         self.db = db_session()
#
#     def __enter__(self):
#         return self.db
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         self.db.close()
#
#
# def get_db():
#     """ Returns the current db connection """
#     with DBContext() as db:
#         yield db
# © 2022 GitHub, Inc.


'''