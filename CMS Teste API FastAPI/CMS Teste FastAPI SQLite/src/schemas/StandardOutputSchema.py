from pydantic import BaseModel


class StandardOutput(BaseModel):
    message: str
