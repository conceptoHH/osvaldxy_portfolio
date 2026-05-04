from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from database import create_db_and_tables
from routers import media

app = FastAPI(title="Osvaldxy Portfolio")

app.mount("/media", StaticFiles(directory="uploads"), name="media")

app.include_router(media.router, prefix="/api/media", tags=["Media"])

@app.get("/")
def health_check():
    return {"status": "backend is operational"}

app.on_event("startup")
def on_startup():
    create_db_and_tables()
        


