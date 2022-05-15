from fastapi import APIRouter, status 
from repository import BookRepo
from models import Book, Response


router = APIRouter(prefix="/book", tags=['book'])


@router.get("/")
async def get_all():
    book_list = await BookRepo.get_all()
    result = Response(code=status.HTTP_200_OK, status="Ok", message="Success retrieve all data", result=book_list)
    return result.dict(exclude_none=True)


@router.get("/{id}")
async def get_id(id: str):
    _book = await BookRepo.get_id(id=id)
    result = Response(code=status.HTTP_200_OK, status="Ok", message="Success retrieve data", result=_book)
    return result.dict(exclude_none=True)


@router.post("/create")
async def create(book: Book):
    result = await BookRepo.insert(book=book)
    book.id = result
    print('router.create', book)
    result = Response(code=status.HTTP_201_CREATED, status="Ok", message="Success save data", result=book)
    return result.dict(exclude_none=True)


@router.post("/update")
async def update(book: Book):
    await BookRepo.update(id=book.id, book=book)
    result = Response(code=status.HTTP_200_OK, status="Ok", message="Success update data")
    return result.dict(exclude_none=True)


@router.delete("/{id}")
async def delete(id: str):
    await BookRepo.delete(id=id)
    result = Response(code=status.HTTP_204_NO_CONTENT, status="Ok", message="Success delete data")
    return result.dict(exclude_none=True)
