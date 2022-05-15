#Dependencies
from controller import *
from model import Item
from fastapi import APIRouter


router = APIRouter(prefix="/api", tags=['api'])


@router.get('/')
def api_get():
    return get()


@router.post('/', status_code=201) #, response_model=Item
def api_post(item: Item):
    item_dict = item.dict()
    return post(item_dict)


@router.delete('/{cache_key}')
def api_delete(cache_key):
    return delete(cache_key)   
