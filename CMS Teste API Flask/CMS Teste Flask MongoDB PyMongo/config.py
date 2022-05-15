from pymongo import MongoClient

try:
    uri = 'mongodb://root:example@localhost:27017/?maxPoolSize=20&retryWrites=true&w=majority'
    client = MongoClient(host=uri, serverSelectionTimeoutMS=1000)
    client.server_info()
    db = client["test-database-py-flask"]
except Exception as e:
    print(e)
