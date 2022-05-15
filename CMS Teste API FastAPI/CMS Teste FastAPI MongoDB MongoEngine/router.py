from fastapi import APIRouter, status 
from repository import EmployeeRepo
from models import EmployeeIn, Response


router = APIRouter(prefix="/employee", tags=['employee'])


@router.get("/")
async def get_all():
    employees = await EmployeeRepo.get_all()
    result = Response(code=status.HTTP_200_OK, status="Ok", message="Success retrieve all data", result=employees)
    return result.dict(exclude_none=True)


@router.get("/{id}")
async def get_id(id: str):
    employee = await EmployeeRepo.get_id(id=id)
    result = Response(code=status.HTTP_200_OK, status="Ok", message="Success retrieve data", result=employee)
    return result.dict(exclude_none=True)


@router.get("/search")
async def get_search(nome: str, age: str):
    employee = await EmployeeRepo.get_search(nome=nome, age=age)
    result = Response(code=status.HTTP_200_OK, status="Ok", message="Success retrieve data", result=employee)
    return result.dict(exclude_none=True)


@router.post("/")
async def create(employee: EmployeeIn):
    result = await EmployeeRepo.insert(row=employee)
    employee.id = result
    result = Response(code=status.HTTP_201_CREATED, status="Ok", message="Success save data", result=employee)
    return result.dict(exclude_none=True)


# @router.post("/update")
# async def update(book: Employee):
#     await EmployeeRepo.update(id=book.id, book=book)
#     result = Response(code=status.HTTP_200_OK, status="Ok", message="Success update data")
#     return result.dict(exclude_none=True)


# @router.delete("/{id}")
# async def delete(id: str):
#     await EmployeeRepo.delete(id=id)
#     result = Response(code=status.HTTP_204_NO_CONTENT, status="Ok", message="Success delete data")
#     return result.dict(exclude_none=True)
