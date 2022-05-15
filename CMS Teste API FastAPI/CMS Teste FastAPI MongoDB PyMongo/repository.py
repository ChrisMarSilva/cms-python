from fastapi.encoders import jsonable_encoder
import uuid
from models import Book
from config import database


class BookRepo():

    @staticmethod
    async def get_all():
        _book = []
        try:
            collection = database.book.find() 
            for book in collection: 
                _book.append(book)
        except Exception as e:
            print('Erro', e)
        return _book

    @staticmethod
    async def get_id(id: str):
        return database.book.find_one({"_id": id})

    @staticmethod
    async def insert(book: Book):
        _book = {"_id": str(uuid.uuid4()), "title": book.title, "description": book.description}
        result = database.book.insert_one(jsonable_encoder(_book)) 
        return result.inserted_id

    @staticmethod
    async def update(id: str, book: Book):
        _book = await BookRepo.get_id(id=id) 
        _book["title"] = book.title
        _book["description"] = book.description
        database.book.update_one({"_id": id}, {"$set": _book})

    @staticmethod
    async def delete(id: str):
        database.book.delete_one({"_id": id})
