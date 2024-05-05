from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
import uvicorn
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

class WebServer:
    def __init__(self, DataBase):
        self.database = DataBase
        self.chats = {}

    @staticmethod
    def send_response(content, status_code):
        return JSONResponse(content=content, status_code=status_code)

    @app.get("/")
    async def root(self):
        return self.send_response({}, 200)

    @app.get("/Login.html")
    async def login(self):
        return self.send_response({}, 200)

    @app.post("/send_details_Login")
    async def send_details_login(self, data: dict):
        acc = data
        result = self.database.accounts_details.find_one({"name": acc["name"].lower()})
        if result is not None and result["password"] == acc["pass"]:
            return self.send_response({"can_login": True}, 200)
        else:
            return self.send_response({"can_login": False}, 200)

    @app.post("/send_details_Register")
    async def send_details_register(self, data: dict):
        acc = data
        result = self.database.accounts_details.find_one({"name": acc["name"].lower()})
        if result is None:
            self.database.accounts_details.insert_one({"name": acc["name"].lower(), "password": acc["pass"]})
            return self.send_response({"existing": False}, 200)
        else:
            return self.send_response({"existing": True}, 200)

    @app.post("/AdminRegister")
    async def admin_register(self, data: dict):
        acc = data
        result_admin = self.database.Admins.find_one({"name": acc["name"].lower()})
        result_accounts = self.database.accounts_details.find_one({"name": acc["name"].lower()})
        if result_admin is None and result_accounts is None:
            self.database.Admins.insert_one({"name": acc["name"].lower(), "password": acc["pass"]})
            return self.send_response({"existing": False}, 200)
        else:
            return self.send_response({"existing": True}, 200)

    @app.post("/add_contact")
    async def add_contact(self, data: dict):
        friend_filter_query = {"name": data["data"].lower()}
        friend = self.database.accounts_details.find_one(friend_filter_query)
        if friend:
            user_filter_query = {"name": data["current_user"].lower()}
            user = self.database.accounts_details.find_one(user_filter_query)
            if user == friend:
                return self.send_response({"error": "Cannot add yourself"}, 200)
            else:
                if user and data["current_user"] is not None:
                    if data["data"].lower() in user.get("fields", []):
                        return self.send_response({"existing": True}, 200)
                    else:
                        update_query = {"$push": {"fields": data["data"].lower()}}
                        self.database.accounts_details.update_one(user_filter_query, update_query)
                        return self.send_response({"existing": False}, 200)
                else:
                    return self.send_response({"error": "User not found"}, 200)
        else:
            return self.send_response({"error": "Friend not found"}, 200)

    @app.post("/create_group")
    async def create_group(self, data: dict):
        # Handle create group logic here
        return self.send_response({"existing": True}, 200)


def open_database():
    uri = "mongodb+srv://lavak:Lava@heartrate.qduwqzq.mongodb.net/?retryWrites=true&w=majority&appName=heartrate"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    print(client.list_database_names())
    return client.heartrate  # access database


def main():
    db = open_database()
    server = WebServer(db)  # Replace DataBase() with your actual database initialization
    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
