import pymongo


MONGODB_URL = 'mongodb://root:example@localhost:27017/'
client = pymongo.MongoClient(MONGODB_URL)
database = client['test-database-py-fastapi'] 
