import datetime

import pymongo


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://lavak:Lava@heartrate.qduwqzq.mongodb.net/?retryWrites=true&w=majority&appName=heartrate"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

print(client.list_database_names())
db = client.heartrate
todo1 = {"name": "Lava", "text": "My first todo!", "status": "open",
         "tags": ["python", "coding"], "date": str(datetime.datetime.now())}
todo2 = {"name": "examle", "text": "My second todo!", "status": "open",
         "tags": ["c++", "coding"], "date": str(datetime.datetime.now())}

todos = db.todos
# result = todos.insert_one(todo1)  # insert one
# result = todos.insert_many([todo1, todo2])  # insert multiple

# result = todos.find_one()
# print(result)  # find first one

# result = todos.find_one({"name": "examle"})
# print(result)  # find paticular one

result = todos.find({"name": "Lava"})
print(result)



# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


"""curl --location --request POST 'https://eu-central-1.aws.data.mongodb-api.com/app/data-fbhec/endpoint/data/v1/action/findOne' \
--header 'Content-Type: application/json' \
--header 'Access-Control-Request-Headers: *' \
--header 'api-key: <API_KEY>' \
--data-raw '{
    "collection":"<COLLECTION_NAME>",
    "database":"<DATABASE_NAME>",
    "dataSource":"heartrate",
    "projection": {"_id": 1}
}'
"""