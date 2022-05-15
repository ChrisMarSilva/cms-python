from redis_om import JsonModel, HashModel, Migrator, Field
from config import redis_db


class Task(JsonModel):  # HashModel # JsonModel

    name: str = Field(index=True)
    description: str = Field(index=False)
    complete: bool = Field(index=False)

    class Meta: 
        database: redis_db

Migrator().run() # Create index # # Create a RediSearch index for instances of the Person model.
