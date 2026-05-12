import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, SQLModel
from .database import create_db_and_tables, engine
from .routers import media, album

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan, title="Osvaldxy Portfolio")

app.mount("/static", StaticFiles(directory="osvaldxy_back/uploads"), name="static")

app.include_router(media.router, prefix="/api/media", tags=["Media"])
app.include_router(album.router, prefix="/api/album", tags=["Album"])

@app.get("/")
def health_check():
    return {"status": "backend is operational"}        


