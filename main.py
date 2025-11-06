from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import musicalCompositions, users
from models.MusicalComposition import MusicalComposition
from db.config_db import engine, create_db_and_tables
from sqlmodel import Session

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (se precisar fazer cleanup)

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(musicalCompositions.router)
