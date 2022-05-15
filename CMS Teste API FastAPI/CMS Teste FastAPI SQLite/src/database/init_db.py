from asyncio import run
from src.database.session import engine, Base

async def create_database():
    #return Base.metadata.create_all(bind=engine)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
