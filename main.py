import uvicorn
from fastapi import FastAPI

from routes import router

app = FastAPI()

@app.get("/")
def read_root() -> str:
    return "Server is running!"

app.include_router(router=router)