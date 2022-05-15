from fastapi import APIRouter
from schema import Task
from redis_om.model import NotFoundError
import json
from types import SimpleNamespace


router = APIRouter(prefix="/task", tags=['task'])


@router.get("/")
async def get_all():
    try:

        # Task(name='name 1', description='description 1', complete=True).save()
        # jsonData = {'name': 'name 1', 'description': 'description 1', 'complete': True}
        # Task(**jsonData).save()
        # Task(**json.loads(jsonData)).save()
        # x = json.loads(jsonData, object_hook=lambda d: SimpleNamespace(**d))
        # Task(x).save()
        # print(type(jsonData))
        # print(type(json.dumps(jsonData)))
        # print(type(json.loads(json.dumps(jsonData))))

        response= [Task.get(pk=pk).dict() for pk in Task.all_pks()]
        # tasks = Task.find(Task.name == '').all()
        # response = [task.dict() for task in tasks]
        return response
    except Exception as e:
        return f"Erro: {e}"


@router.get("/{pk}")
async def get_id(pk: str): 
    try:
        task = Task.get(pk=pk)  # 01G1EFR8D5Q18539KZA4QQANNA
        return task.dict()
    except NotFoundError:
        return {}


@router.post("/")
async def create(task: Task):
    try:
        task.save()
        return task.pk
    except Exception as e:
        return f"Erro: {e}"

@router.put("/{pk}")
async def update(pk: str, task: Task):
    _task = Task.get(pk=pk)
    _task.name = task.name
    _task.description = task.description
    return _task.save()


@router.delete('/{pk}')
async def delete(pk: str):
    _task = Task.get(pk=pk)
    return _task.delete()
