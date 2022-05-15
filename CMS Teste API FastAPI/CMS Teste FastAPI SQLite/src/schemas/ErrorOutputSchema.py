from pydantic import BaseModel


class ErrorOutput(BaseModel):
    detail: str
