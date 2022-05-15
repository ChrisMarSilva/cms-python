from models import Employee, EmployeeIn, TextPost, LinkPost
import uuid, json
from mongoengine.queryset.visitor import Q


class EmployeeRepo():

    @staticmethod
    async def get_all():
        try:

            # post1 = TextPost(title='Using MongoEngine', content='See the tutorial')
            # post1.tags = ['mongodb', 'mongoengine']
            # post1.save()

            # post2 = LinkPost(title='MongoEngine Docs', url='hmarr.com/mongoengine')
            # post2.tags = ['mongoengine', 'documentation']
            # post2.save()

            # employee = Employee(nome="Simple todo A 1", age=20)
            # employee.teams = ["12345678910", "12345678910"]
            # employee.save()

            #Employee(nome="Simple todo A 1", age=20, teams=["12345678910", "12345678910"]).save()
            #Employee(nome="Simple todo A 2", age=20, teams=["12345678910", "12345678910"]).save()
            #Employee(nome="Simple todo A 3", age=20, teams=["12345678910", "12345678910"]).save()
            
            employees = Employee.objects().to_json()
            return json.loads(employees)
        except Exception as e:
            return str(e)


    @staticmethod
    async def get_id(id: str):
        employee = Employee.objects().get(pk=id)
        return {"id_": employee.pk, "nome": employee.nome, "age": employee.age, "teams": employee.teams}


    @staticmethod
    async def get_search(nome: str, age: str):
        employee = Employee.objects().filter(Q(nome=id) | Q(age=id)).to_json()
        return json.loads(employee)


    @staticmethod
    async def insert(row: EmployeeIn):
        employee = Employee(pk=str(uuid.uuid4()), nome=row.nome, age=row.age, teams=row.teams)
        employee.save()
        return employee.pk

    # @staticmethod
    # async def update(id: str, book: Employee):
    #     _book = await EmployeeRepo.get_id(id=id)
    #     _book["title"] = book.title
    #     _book["description"] = book.description
    #     await database.get_collection('book').update_one({"_id": id}, {"$set": _book})

    # @staticmethod
    # async def delete(id: str):
    #     await database.get_collection('book').delete_one({"_id": id})
