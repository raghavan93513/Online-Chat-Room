# fastapi template for authentication with firebase (pyrebase4 package)

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.websockets import WebSocket
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pyrebase import pyrebase
import os
import uvicorn
import json
import traceback
from dotenv import load_dotenv

# fastapi initialization
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

load_dotenv()

# User model
class User(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None

# firebase config
config = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "projectId": os.getenv("projectId"),
    "storageBucket": os.getenv("storageBucket"),
    "messagingSenderId": os.getenv("messagingSenderId"),
    "appId": os.getenv("appId"),
    "measurementId": os.getenv("measurementId"),
}

# firebase initialization
firebase = pyrebase.initialize_app(config)
firebaseauth = firebase.auth()

# connected clients
clients = []


@app.post("/create_user")
async def create_user(user: User):
    try:
        authuser = firebaseauth.create_user_with_email_and_password(user.email, user.password)
    except Exception as e:
        if "EMAIL_EXISTS" in str(e):
            return "ERROR: Email already exists"
        elif "INVALID_EMAIL" in str(e):
            return "ERROR: Invalid email"
        elif "WEAK_PASSWORD" in str(e):
            return "ERROR: Password is too weak"
        else:
            return "ERROR: Something went wrong: " + str(e)
    print(authuser)
    try:
        # update display name
        firebaseauth.update_profile(authuser["idToken"], display_name=user.display_name)
    except Exception as e:
        if "USER_NOT_FOUND" in str(e):
            return "ERROR: User not found"
        else:
            return "ERROR: Something went wrong: " + str(e)

    return authuser["idToken"]

@app.post("/login")
async def login(user: User):
    try:
        user = firebaseauth.sign_in_with_email_and_password(user.email, user.password)
        return user["idToken"]
    except Exception as e:
        if "INVALID_PASSWORD" in str(e):
            return "ERROR: Invalid password"
        elif "EMAIL_NOT_FOUND" in str(e):
            return "ERROR: Email not found"
        else:
            return "ERROR: Something went wrong: " + str(e)

@app.get("/")
async def root(request: Request):
    # get cookies
    cookies = request.cookies
    if "token" in cookies:
        # get token from cookies
        token = cookies["token"]
        try:
            # verify token
            decoded_token = firebaseauth.get_account_info(token)
            print(decoded_token)
            return templates.TemplateResponse("chat.html", {"request": request, "username": decoded_token["users"][0]["displayName"]})
        except Exception as e:
            # print traceback
            traceback.print_exc()
            return templates.TemplateResponse("loginpage.html", {"request": request, "user": None})
    else:
        return templates.TemplateResponse("loginpage.html", {"request": request, "user": None})
    
# create websocket connection for chat
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        try:
            data = await websocket.receive_text()
        except Exception as e:
            # remove client from list
            clients.remove(websocket)
        
        # send message to all connected clients
        for client in clients:
            await client.send_text(data)
    

# run the app
if __name__ == "__main__":
    uvicorn.run(app)

