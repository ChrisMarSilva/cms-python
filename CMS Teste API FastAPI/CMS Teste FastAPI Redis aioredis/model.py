from pydantic import BaseModel


class Item(BaseModel):
    name: str
    msg: str = None
