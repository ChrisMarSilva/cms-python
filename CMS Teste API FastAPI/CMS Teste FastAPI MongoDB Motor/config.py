import motor.motor_asyncio


MONGODB_URL = 'mongodb://root:example@localhost:27017/'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client['test-database-py-fastapi']  # client.python_db

# print(database["book"].find().to_list(length=1000)) 
