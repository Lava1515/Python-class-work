from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# Mounting static files directory
app.mount("/webroot", StaticFiles(directory="webroot"), name="webroot")


class WebServer:
    def __init__(self, DataBase):
        self.database = DataBase
        self.chats = {}

    @staticmethod
    def read_file(file_name):
        """ Read A File """
        with open(file_name, "rb") as f:
            data = f.read()
        return data

    def load_chat_messages(self, chat_id):
        filename = f'chats_data/{chat_id}_messages.json'
        try:
            with open(filename, 'r') as file:
                self.chats[chat_id] = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, create a new one with numbering
            self.chats[chat_id] = []
            with open(filename, 'w') as file:
                json.dump(self.chats[chat_id], file)

    @staticmethod
    def update_messages_file(chat_id, messages):
        filename = f'chats_data/{chat_id}_messages.json'
        with open(filename, 'w') as file:
            json.dump(messages, file)

    @staticmethod
    def send_response(content, status_code):
        return JSONResponse(content=content, status_code=status_code)

web_server = WebServer(DataBase()) # Assuming you have a DataBase class

@app.get("/", response_class=HTMLResponse)
async def root():
    return app.mounted_directories["webroot"].index_html

@app.get("/Login.html", response_class=HTMLResponse)
async def login():
    return app.mounted_directories["webroot"].login_html

@app.post("/send_details_Login")
async def send_details_login(data: dict):
    acc = data
    result = web_server.database.accounts_details.find_one({"name": acc["name"].lower()})
    if result is not None and result["password"] == acc["pass"]:
        return {"can_login": True}
    else:
        return {"can_login": False}

# Add other routes similarly

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
