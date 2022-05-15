from loguru import logger
import time
import datetime as dt
import uuid
import json
import pymongo
from pymongo import MongoClient
from pymongo import InsertOne, DeleteOne, DeleteMany, ReplaceOne, UpdateOne
from pymongo.errors import BulkWriteError
from pymongo.collation import Collation
from bson.objectid import ObjectId
from bson.son import SON
from decimal import Decimal
from bson.decimal128 import Decimal128
from dotenv import load_dotenv


def insert(collection: Collation, **args):
    return collection.insert(args)


def update(collection: pymongo.collection.Collection):
    return collection.update(query={'idade': 18}, update={'$set': {'idade': 'dezoito'}}) 


def delete(collection: pymongo.collection.Collection):
    return collection.remove({'idade': {'$lt': 18}})


def read(collection: pymongo.collection.Collection, **args):
    return collection.find({})


def busca_por_id(collection: pymongo.collection.Collection, post_id: str):
    return collection.find_one({'_id': ObjectId(post_id)})


def busca_por_idade(collection: pymongo.collection.Collection, field, op, value):
    return collection.find_many({field: {op: value}})


def teste_pymongo_client() -> pymongo.MongoClient: 
    uri = 'mongodb://root:example@localhost:27017/?maxPoolSize=20&retryWrites=true&w=majority&authSource=admin'
    logger.info(f'{uri=}')
    client = MongoClient(uri)
    return client


def teste_pymongo_database(client: pymongo.MongoClient) -> pymongo.database.Database: 
    db = client['test-database-py']  # client['test-database-py'] # client.database_name # test-database-py # test_database_py # db = get_database() # db # database
    return db


def teste_pymongo_collection_posts(db: pymongo.database.Database) -> pymongo.collection.Collection: 
    posts = db.posts # db['posts'] # collection # collection_posts # posts # db.posts 
    return posts


def teste_pymongo_schema_validations(db: pymongo.database.Database) -> None:
    result = db.create_collection("my_coll_with_schema", validator={
        '$jsonSchema': {
            "title": "Main Table for Customers",
			"description": "This document records the details of an customer and demographics",
            'bsonType': 'object',
            'additionalProperties': True, 
            'required': ["component", "path", "CustomerID","FirstName", "LastName" ,"address"], 
            'properties': {
                'component': {'bsonType': 'string'},
                'path': {'bsonType': 'string', 'description': 'Set to default value'},
                "CustomerID": { "bsonType": "int", "description": "must be a Integer and is required" },
                "FirstName": { "bsonType": "string", "description": "must be a string and is required" },
                "LastName": { "bsonType": "string", "description": "must be a string and is required" },
                "MiddleName": { "bsonType": "string", "description": "must be a string and is required" },
                "year": { "bsonType": "int", "minimum": 2017, "maximum": 3017, "exclusiveMaximum": False, "description": "must be an integer in [ 2017, 3017 ] and is required" },
                "major": { "enum": [ "Math", "English", "Computer Science", "History", None ], "description": "can only be one of the enum values and is required" },
                "address": { 
                    "bsonType": "array",
                    "required": [ "addresstype","address1", "city", "state", "zipcode" ],
                    "properties": {
                        "addresstype": { "bsonType": "string" },
                        "address1": { "bsonType": "string" },
                        "address2": { "bsonType": "string" },
                        "address3": { "bsonType": "string" },
                        "city": { "bsonType": "string" },
                        "state": { "bsonType": "string" },
                        "zipcode": { "bsonType": "string" },
                    }
                }
            }
        }
    })
    logger.info(f'{result=}') 

    # db.createCollection("my_coll_with_validator", {"validator": {"$jsonSchema": {"properties": {"count": {"bsonType": "int"}}}}})

def teste_pymongo_create_index(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Create Index')
    result = posts.create_index('author')
    # result = posts.create_index([('_id', pymongo.ASCENDING)], unique=True)
    # result = posts.create_index([("mike", pymongo.DESCENDING), ("eliot", pymongo.ASCENDING)])
    logger.info(f'{result=}')  # result='author_1'


def teste_pymongo_get_all_databases(client: pymongo.MongoClient) -> None:
    logger.info(f'Teste Get All Databases') 
    for database in client.list_databases():  # list_databases # list_database_names
        logger.info(f'{database=}') 


def teste_pymongo_get_all_collections(db: pymongo.database.Database) -> None:
    logger.info(f'Teste Get All Collection') 
    collections = db.list_collection_names()
    logger.info(f'{collections=}') 


def teste_pymongo_get_all_indexes(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Get All Indexes') 
    indexes = posts.index_information()
    logger.info(f'indexes={sorted(list(indexes))}')


def teste_pymongo_insert_one(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Insert One') 
    post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"], "date": dt.datetime.utcnow()}
    result = posts.insert_one(post)
    # post = {"author": "Chris MarSil", "text": "Nao tem texto", "tags": ["python"], "date": dt.datetime.now()}
    # result = posts.insert_one(post)
    # post = {"author": "Silva", "text": "Nao tem texto", "tags": ["python"], "date": dt.datetime.now()}
    # result = posts.insert_one(post)
    logger.info(f'{result.inserted_id=}') 
    logger.info(f'') 


def teste_pymongo_insert_many(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Insert Many') 
    new_posts = [{"author": "Mike", "text": "Another post!", "tags": ["bulk", "insert"], "date": dt.datetime(2009, 11, 12, 11, 14)},{"author": "Eliot", "title": "MongoDB is fun", "text": "and pretty easy too!", "date": dt.datetime(2009, 11, 10, 10, 45)}]
    result = posts.insert_many(new_posts)
    # new_posts = [{"_id": 1, "author": "Mike 1", "text": "Another post!", "tags": ["bulk", "insert"], "date": dt.datetime(2009, 11, 12, 11, 14)},{"_id": 2, "author": "Eliot 2", "title": "MongoDB is fun", "text": "and pretty easy too!", "date": dt.datetime(2009, 11, 10, 10, 45)}]
    # result = posts.insert_many(new_posts)
    # result = posts.insert_many([{'author': f"Mike #{i}", "text": "Another post! #{i}", "tags": ["bulk", "insert"], "date": dt.datetime(2009, 11, 12, 11, 14) } for i in range(10_000)]).inserted_ids
    logger.info(f'{result.inserted_ids=}') 
    logger.info(f'') 


def teste_pymongo_bulk_write(posts: pymongo.collection.Collection) -> None:

    logger.info(f'Teste Bulk Write') 
    result = posts.bulk_write([
        DeleteMany({}),  # Remove all documents from the previous example.
        InsertOne({'_id': 1}),
        InsertOne({'_id': 2}),
        InsertOne({'_id': 3}),
        UpdateOne({'_id': 1}, {'$set': {'foo': 'bar'}}),
        UpdateOne({'_id': 4}, {'$inc': {'j': 1}}, upsert=True),
        ReplaceOne({'j': 1}, {'j': 2})]
    )
    logger.info(f'{result.bulk_api_result=}') 
    logger.info(f'{result.inserted_count=}') 
    logger.info(f'{result.deleted_count=}') 
    logger.info(f'{result.modified_count=}') 
    logger.info(f'{result.upserted_ids=}') 
    logger.info(f'') 
    requests = [
        ReplaceOne({'j': 2}, {'i': 5}),
        InsertOne({'_id': 4}),  # Violates the unique key constraint on _id.
        DeleteOne({'i': 5})]
    try:
        posts.bulk_write(requests)
    except BulkWriteError as bwe:
        logger.error(bwe.details)


def teste_pymongo_update_one(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Update One') 
    myquery = {"author": "Silva" }
    newvalues = {"$set": {"author": "Silva 123"}}
    # newvalues = {"$set": {"author": "Silva 123"}, "$inc": {"age": 1}, "$rename": {"first_name": "first", "last_name": "last"}}
    # newvalues = {"$unset": {"author": ""}} # remover field
    # newvalues = {"$addToSet": {"addresses": address}} # add another object
    result = posts.update_one(myquery, newvalues)
    # posts.update_one({ "audit" : "seats"}, { "$inc" : { "count" : 1}}, upsert=True)
    logger.info(f'{result.matched_count=}') 
    logger.info(f'{result.modified_count=}') 


def teste_pymongo_update_many(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Update Many') 
    myquery = {"author": { "$regex": "^M" }}
    newvalues = {"$set":{ "author": "Mike Novo"}}
    result = posts.update_many(myquery, newvalues)
    logger.info(f'{result.matched_count=}') 
    logger.info(f'{result.modified_count=}') 


def teste_pymongo_delete_one(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Delete One') 
    result = posts.delete_one({ "author": "Mike Novo" })
    logger.info(f'{result.deleted_count=}')


def teste_pymongo_delete_many(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Delete Many') 
    result = posts.delete_many({ "author": {"$regex": "^M"} })
    # result = posts.delete_many({})
    logger.info(f'{result.deleted_count=}') 


def teste_pymongo_count(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Count') 
    result = posts.count_documents({})
    # result = posts.count_documents({"author": "Mike"})
    logger.info(f'{result=}') 


def teste_pymongo_max(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Max') 

    result = posts.find({}).sort("author", -1).limit(1)  # max
    logger.info(f'{result=}') 

    result = posts.find_one(filter={}, sort=[("author", -1)], limit=1)  # max
    logger.info(f'{result=}') 
    
def teste_pymongo_max(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Min') 

    result = posts.find({}).sort("author", 1).limit(1)  # min
    logger.info(f'{result=}') 

    result = posts.find_one(filter={}, sort=[("author", 1)], limit=1)  # min
    logger.info(f'{result=}') 

def teste_pymongo_distinct(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Distinct') 
    result = posts.distinct(key='author', filter={})
    logger.info(f'{result=}') 
    logger.info(f'{len(result)=}')


def teste_pymongo_group(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Group') 
    # result = posts.aggregate([{"$group": {"_id": "$date" }}, {"$group": {"_id": 1, "count": {"$sum" : 1 }}}])
    # result = posts.aggregate([{"$group": {"_id": "$country", "count":{"$sum": 1}}}])
    result = posts.aggregate([{"$group": {"_id": "author", "count": {"$sum": 1}}}])
    logger.info(f'{result=}') 
    for row in result:
        logger.info(f'{row=}')  # result["_id"], result["count"]


def teste_pymongo_find_one(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Find One') 
    post = posts.find_one()
    # post = posts.find_one({"author": "Eliot"})
    # post = posts.find_one({"_id": "62642ec04dd956c721a7ccec"})  # erro, nao vai encontrar o registro
    # post = posts.find_one({"_id": ObjectId("62642ec04dd956c721a7ccec")})
    # post = posts.find_one({"email": 'chris,bla,bla'})
    logger.info(f'{post=}') 
    logger.info(f'') 


def teste_pymongo_find(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Find') 
    # posts_list = posts.find()
    # posts_list = posts.find({"author": "Mike"})
    # posts_list = posts.find({"date": {"$lt": dt.datetime(year=2009, month=11, day=12, hour=12)}}).sort("author")
    # posts_list = posts.find({"date": {"$lt": dt.datetime(year=2009, month=11, day=12, hour=12)}}).sort([["author", 1], ["date", 1]])
    # posts_list = posts.find({},{ "_id": "0", "author": "Chris MarSil", "text": "Nao tem texto" })
    # posts_list = posts.find({ "author": { "$gt": "S" } })
    # posts_list = posts.find({ "author": { "$regex": "^M" } }) # 0.04s - 0:00:00.038160 # sem index # 0.02s - 0:00:00.017510 # com index
    # posts_list = posts.find().sort("author")
    # posts_list = posts.find().sort("author", -1)
    posts_list = posts.find().limit(2)
    for idx, post in enumerate(posts_list): 
        logger.info(f'#{idx+1} - {post["_id"]} - {post["author"]}') 
    logger.info(f'') 


def teste_pymongo_drop_collection(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Drop Collection') 
    posts.drop()


def teste_pymongo_convert_valor_decimal(posts: pymongo.collection.Collection) -> None:
    logger.info(f'Teste Convert Valor Decimal') 
    
    def convert_decimal(dict_item):
        # This function iterates a dictionary looking for types of Decimal and converts them to Decimal128
        # Embedded dictionaries and lists are called recursively.
        if dict_item is None: return None

        for k, v in list(dict_item.items()):
            if isinstance(v, dict):
                convert_decimal(v)
            elif isinstance(v, list):
                for l in v:
                    convert_decimal(l)
            elif isinstance(v, Decimal):
                dict_item[k] = Decimal128(str(v))

        return dict_item
        
    # lista = [convert_decimal(row) for row in result]  # lista = [row for row in result] 

    # client = get_client(mongo_uri=mongo_uri)
    # db = get_database(client=client)
    # collection =db.teste 
    # collection.delete_many({})
    # collection.insert_one({'nome': 'Teste #1', 'valor': 0.0})
    # #  collection.insert_one({'nome': 'Teste #2', 'valor': Decimal('0.00')})  # "cannot encode object: Decimal('0.00'), of type: <class 'decimal.Decimal'>"
    # collection.insert_one({'nome': 'Teste #3', 'valor': Decimal128(str(Decimal('0.00')))})

    



def teste_pymongo_cms(client: pymongo.MongoClient, db: pymongo.database.Database) -> None:
    try:

        logger.info(f'Teste CMS') 

        def get_collection_people(db):
            return db.people

        def get_collection_address(db):
            return db.address

        pessoas = get_collection_people(db=db) # db.people
        enderecos = get_collection_address(db=db) # db.address

        # session = None

        wc_majority = pymongo.WriteConcern("majority", wtimeout=1000)

        logger.info(f'start_session')
        with client.start_session() as session:  # client.start_session(causal_consistency=True) # client.start_session(snapshot=True)
            
            # session.with_transaction(callback, read_concern=ReadConcern("local"), write_concern=wc_majority, read_preference=ReadPreference.PRIMARY)
            # session.with_transaction(write_concern=wc_majority)

            # logger.info(f'start_transaction')
            # with session.start_transaction():
            # session.start_transaction(read_concern=pymongo.read_concern.ReadConcern("local"), write_concern=wc_majority)

            # errmsg: Transaction numbers are only allowed on a replica set member or mongos
            # code: 20
            # codeName: 'IllegalOperation'

            logger.info(f'delete_many')
            pessoas.delete_many({}, session=session)
            enderecos.delete_many({}, session=session)

            ins_pes_1 = pessoas.insert_one({"nome": "Pessoa 1", "date": dt.datetime.now()}, session=session)
            ins_pes_2 = pessoas.insert_one({"nome": "Pessoa 2", "date": dt.datetime.now()}, session=session)
            ins_pes_3 = pessoas.insert_one({"nome": "Pessoa 3", "date": dt.datetime.now()}, session=session)
            
            ins_end_1 = enderecos.insert_one({"logradouro": "Rua 1 - Pessoa 1"}, session=session)
            ins_end_2 = enderecos.insert_one({"logradouro": "Rua 2 - Pessoa 2"}, session=session)
            ins_end_3 = enderecos.insert_one({"logradouro": "Rua 3 - Pessoa 2"}, session=session)
            ins_end_4 = enderecos.insert_one({"logradouro": "Rua 4 - Pessoa 3"}, session=session)
            ins_end_5 = enderecos.insert_one({"logradouro": "Rua 5 - Pessoa 3"}, session=session)
            ins_end_6 = enderecos.insert_one({"logradouro": "Rua 6 - Pessoa 3"}, session=session)

            pessoas.update_one({"_id": ins_pes_1.inserted_id}, {"$set": {"address": [ins_end_1.inserted_id]}}, session=session)
            pessoas.update_one({"_id": ins_pes_2.inserted_id}, {"$set": {"address": [ins_end_2.inserted_id, ins_end_3.inserted_id]}}, session=session)
            pessoas.update_one({"_id": ins_pes_3.inserted_id}, {"$set": {"address": [ins_end_4.inserted_id, ins_end_5.inserted_id, ins_end_6.inserted_id]}}, session=session)

            # logger.info(f'commit_transaction')
            # session.commit_transaction()
            # session.abort_transaction()

        # logger.info(f'Pessoas') 
        # result = pessoas.find()
        # for idx, pessoa in enumerate(result): 
        #     try:
        #         logger.info(f'#{idx+1} {pessoa["_id"]} {pessoa["nome"]} {pessoa["address"]}') 
        #     except:
        #         logger.info(f'#{idx+1} {pessoa["_id"]} {pessoa["nome"]} VAZIO') 

        # logger.info(f'Enderecos') 
        # result = enderecos.find()
        # for idx, endereco in enumerate(result):  
        #     logger.info(f'#{idx+1} {endereco["_id"]} {endereco["logradouro"]}') 

        logger.info(f'Pessoas e Enderecos') 
        result = pessoas.aggregate(
            [
                {'$lookup': {'from': 'address','localField': 'address','foreignField': '_id','as': 'addresses' }},  # addresses # results
                {'$match': {'nome' : 'Pessoa 2', 'addresses.logradouro' : 'Rua 3 - Pessoa 2'}},
            ]
        )
        for idx_pessoa, pessoa in enumerate(result): 
            logger.info(f'#{idx_pessoa+1} {pessoa["_id"]} {pessoa["nome"]}') 
            for idx_endereco, endereco in enumerate(pessoa["addresses"]):  # addresses # results
                logger.info(f'    #{idx_endereco+1} {endereco["_id"]} {endereco["logradouro"]}')


        # rows = collection.aggregate(
        #     [
        #         {'$match': {'IDUSUARIODSST' : int(id_usuario), "SITUACAO": 'P'}},
        #         # {'$lookup': {'from': 'usuarios', 'localField': 'IDUSUARIODSST', 'foreignField': 'ID', 'as': 'USERDSST' }}, 
        #         # {'$set': { "USERDSST": { '$arrayElemAt': ["$USERDSST", 0] } } },
        #         # {'$unwind': "$USERDSST" }, 
        #         # {'$unwind': { 'path': "$USERDSST", 'preserveNullAndEmptyArrays': True }},
        #         {'$lookup': {'from': 'usuarios', 'localField': 'IDUSUARIOORIG', 'foreignField': 'ID', 'as': 'USERORIG' }}, 
        #         # {'$set': { "USERORIG": { '$arrayElemAt': ["$USERORIG", 0] } } },
        #         # {'$unwind': "$USERORIG" },
        #         {'$unwind': { 'path': "$USERORIG", 'preserveNullAndEmptyArrays': True }},
        #         # {'$project': { '_id' : 0, 'IDUSUARIOORIG' : 1, 'IDUSUARIODSST' : 1, 'SITUACAO' : 1, 'NOMEUSERORIG' : "$USERORIG.NOME", 'NOMEUSERDSST' : "$USERDSST.NOME" }},
        #         {'$project': { '_id' : 0, 'IDUSUARIOORIG' : 1, 'IDUSUARIODSST' : 1, 'SITUACAO' : 1, 'NMUSUARIOORIGEM' : "$USERORIG.NOME", 'FTUSUARIOORIGEM' : "$USERORIG.FOTO" }},
        #         {'$sort': {"DTHR": -1}},
        #         {'$limit': 3},
        #     ]
        # )


        logger.info(f'uuid={uuid.uuid4().hex}')

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def teste_mongoengine_cms() -> None:

    from mongoengine import connect, Document, StringField, IntField, ReferenceField, DateTimeField, DynamicDocument, ListField, EmbeddedDocumentField, EmbeddedDocument, CASCADE
    import datetime


    # 'mongodb://root:example@localhost:27017/?maxPoolSize=20&retryWrites=true&w=majority'
    connect(host="mongodb://root:example@localhost:27017/test-database-py-fastapi?authSource=admin")

    class User(Document):
        email = StringField(required=True)
        first_name = StringField(max_length=50)
        last_name = StringField(max_length=50)

        def json(self):
            result_dict = {'email': self.email, 'first_name': self.first_name, 'last_name': self.last_name}
            return json.dumps(result_dict)

        meta = {'indexes': ['email', 'first_name'], 'ordering' : ['-first_name']}

    class Comment(EmbeddedDocument):
        content = StringField()
        name = StringField(max_length=120)

        def json(self):
            result_dict = {'content': self.content, 'name': self.name}
            return json.dumps(result_dict)

    class Post(Document):
        title = StringField(max_length=120, required=True)
        author = ReferenceField(User, reverse_delete_rule=CASCADE)
        tags = ListField(StringField(max_length=30))
        comments = ListField(EmbeddedDocumentField(Comment))
        meta = {'allow_inheritance': True}

        def json(self):
            result_dict = {'title': self.title, 'author': self.User.json(), 'comments': self.comments.json()}
            return json.dumps(result_dict)

    class TextPost(Post):
        content = StringField()

        def json(self):
            result_dict = {'content': self.content}
            return json.dumps(result_dict)

    class ImagePost(Post):
        image_path = StringField()

        def json(self):
            result_dict = {'image_path': self.image_path}
            return json.dumps(result_dict)

    class LinkPost(Post):
        link_url = StringField()

        def json(self):
            result_dict = {'link_url': self.link_url}
            return json.dumps(result_dict)
        
    john = User(email='john@example.com', first_name='John', last_name='Lawley').save()

    ross = User(email='ross@example.com')
    ross.first_name = 'Ross'
    ross.last_name = 'Lawley'
    ross.save()

    post1 = TextPost(title='Fun with MongoEngine', author=john)
    post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
    post1.tags = ['mongodb', 'mongoengine']
    post1.save()

    post2 = LinkPost(title='MongoEngine Documentation', author=ross)
    post2.link_url = 'http://docs.mongoengine.com/'
    post2.tags = ['mongoengine']
    post2.save()

    logger.info(f'Post')
    for post in Post.objects:
        logger.info(f'{post.title}')

    logger.info(f'TextPost')
    for post in TextPost.objects:
        logger.info(f'{post.content}')

    logger.info(f'Post.objects')
    for post in Post.objects:
        logger.info(post.title)
        logger.info('=' * len(post.title))

        if isinstance(post, TextPost):
            logger.info(post.content)

        if isinstance(post, LinkPost):
            logger.info('Link: {}'.format(post.link_url))

    logger.info(f'Searching ')
    for post in Post.objects(tags='mongodb', content='Took a look at MongoEngine today, looks pretty cool.'):
        logger.info(post.title)

    num_posts = Post.objects(tags='mongodb').count()
    logger.info('Found {} posts with tag "mongodb"'.format(num_posts))

        
    class Page(Document):
        title = StringField(max_length=200, required=True)
        date_modified = DateTimeField(default=datetime.datetime.utcnow)

        def json(self):
            result_dict = {'title': self.title, 'date_modified': self.date_modified}
            return json.dumps(result_dict)

    class Page(DynamicDocument):
        title = StringField(max_length=200, required=True)

        def json(self):
            result_dict = {'title': self.title}
            return json.dumps(result_dict)

    page = Page(title='Using MongoEngine')
    page.tags = ['mongodb', 'mongoengine']
    page.save()

    logger.info(Page.objects(tags='mongoengine').count())

    class ExampleFirst(Document):
        # Default an empty list
        values = ListField(IntField(), default=list)

    class ExampleSecond(Document):
        # Default a set of values
        values = ListField(IntField(), default=lambda: [1,2,3])

    class ExampleDangerous(Document):
        # This can make an .append call to  add values to the default (and all the following objects),
        # instead to just an object
        values = ListField(IntField(), default=[1,2,3])

        
def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        client = teste_pymongo_client()
        db = teste_pymongo_database(client=client)

        teste_pymongo_schema_validations(db=db)
        # posts = teste_pymongo_collection_posts(db=db)

        # teste_pymongo_create_index(posts=posts)
        
        teste_pymongo_get_all_databases(client=client)
        # teste_pymongo_get_all_collections(posts=posts)
        # teste_pymongo_get_all_indexes(posts=posts)
        
        # teste_pymongo_insert_one(posts=posts)
        # teste_pymongo_insert_many(posts=posts)
        
        # teste_pymongo_bulk_write(posts=posts)

        # teste_pymongo_update_one(posts=posts)
        # teste_pymongo_update_many(posts=posts)

        # teste_pymongo_delete_one(posts=posts)
        # teste_pymongo_delete_many(posts=posts)
        # teste_pymongo_drop_collection(posts=posts)
        
        # teste_pymongo_count(posts=posts)
        # teste_pymongo_find_one(posts=posts)
        # teste_pymongo_find(posts=posts)

        # teste_pymongo_cms(client=client, db=db)

        # teste_mongoengine_cms()

        


        # from bson import json_util
        # from bson.objectid import ObjectId
        # all_seeds = list(collection.find({}))
        # return  json.dumps(all_seeds, default=json_util.default)
        # user = mongo.db.users.find_one({'_id': ObjectId(id), })
        # response = json_util.dumps(user)

        

        # pymongo     = Sync      # https://pymongo.readthedocs.io/en/stable/
        # motor       = Async     # https://www.mongodb.com/docs/drivers/motor/
        # MongoEngine = ODM Sync  # https://docs.mongoengine.org/tutorial.html
        # ODMantic    = ODM Async # https://art049.github.io/odmantic/

        # python main.py

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade pymongo
# python -m pip install --upgrade motor
# python -m pip install --upgrade mongoengine
# python -m pip install --upgrade odmantic
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
