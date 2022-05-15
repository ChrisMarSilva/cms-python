from redis_om import EmbeddedJsonModel, Field, JsonModel, Migrator, HashModel
from pydantic import PositiveInt
from typing import Optional, List
from config import redis_db


class Customer(HashModel):
    first_name: str
    last_name: str
    age: int


class Address(EmbeddedJsonModel):
    street_number: PositiveInt = Field(index=True)
    unit: Optional[str] = Field(index=False)
    street_name: str = Field(index=True)
    city: str = Field(index=True)
    state: str = Field(index=True)
    postal_code: str = Field(index=True)
    country: str = Field(index=True, default="United Kingdom")
    class Meta: 
        database: redis_db


class Person(JsonModel):  # HashModel  # JsonModel
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    age: PositiveInt = Field(index=True)
    address: Address
    skills: List[str] = Field(index=True)
    personal_statement: str = Field(index=True, full_text_search=True)
    class Meta: 
        database: redis_db


Migrator().run() # Create a RediSearch index for instances of the Person model. # Create index # # Create a RediSearch index for instances of the Person model.


# redis_db.set("hello", "world")
# redis_db.sadd("myset", "a", "b", "c", "d")
# print(redis_db.sismember("myset", "e"))
# print(redis_db.sismember("myset", "b"))

andrew = Customer(first_name="Andrew", last_name="Brookins", age=38,)
# print(andrew.pk)
andrew.save()

#address = Address(street_number=9, street_name="Main Street", city="Sheffield", state="South Yorkshire", country="United Kingdom", postal_code="S12 2MX")
# address = Address({'street_number': 9, 'street_name': "Main Street", 'city': "Sheffield", 'state': "South Yorkshire", 'country': "United Kingdom", 'postal_code': "S12 2MX"})
# person1 = Person(first_name="Andrew", last_name="Brookins", age=38, address=address, skills=["guitar", "piano", "trombone"], personal_statement="My name is Robert, I love meeting new people and enjoy music, coding and walking my dog.")
# person1.save()
