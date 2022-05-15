from models import Book
from config import database
import uuid
from fastapi.encoders import jsonable_encoder


class BookRepo():

    @staticmethod
    async def get_all():
        _book = []
        try:
            collection = database["book"].find() # collection = await database.get_collection('book').find()
            async for book in collection: 
                _book.append(book)
        except Exception as e:
            print('  == 05: erro', e)
        return _book

    @staticmethod
    async def get_id(id: str):
        return await database.get_collection('book').find_one({"_id": id})

    @staticmethod
    async def insert(book: Book):
        _book = {"_id": str(uuid.uuid4()), "title": book.title, "description": book.description}
        _book = jsonable_encoder(_book)
        result = await database["book"].insert_one(_book)  # database.get_collection('book').insert_one(_book)
        return result.inserted_id

    @staticmethod
    async def update(id: str, book: Book):
        _book = await BookRepo.get_id(id=id)  # await database.get_collection('book').find_one({"_id": id})
        _book["title"] = book.title
        _book["description"] = book.description
        await database.get_collection('book').update_one({"_id": id}, {"$set": _book})

    @staticmethod
    async def delete(id: str):
        await database.get_collection('book').delete_one({"_id": id})
