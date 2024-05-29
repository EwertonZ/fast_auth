from fastapi import FastAPI, Depends, HTTPException, status
from utils import get_current_user
from auth import auth_router
from config import MONGO_USER, MONGO_PASS, MONGO_DB_NAME
import motor.motor_asyncio


app = FastAPI()

app.include_router(auth_router)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@lolproject.7vba9yt.mongodb.net/?retryWrites=true&w=majority&appName=Lolproject")
    app.mongodb = app.mongodb_client[MONGO_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/protected")
async def read_protected_route(current_user: dict = Depends(get_current_user)):
    return {"msg": f"Hello, {current_user['email']}! This is a protected route."}