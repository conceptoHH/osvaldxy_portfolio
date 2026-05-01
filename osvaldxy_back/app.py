from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Osvaldxy Portfolio")

app.mount("/media", StaticFiles(directory="uploads"), name="media")

@app.get("/")
def health_check():
    return {"status": "backend is operational"}


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

