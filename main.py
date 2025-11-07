from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
import os
from pathlib import Path

# Adicionar diretório backend ao Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# IMPORTANTE: Importar todos os modelos ANTES de importar create_db_and_tables
# Para que o SQLModel possa registrar todas as tabelas
from shared.auth.models.user import UserDB
from projects.make_music.models.MusicalComposition import MusicalComposition
from projects.cookAi.models.recipe import Recipe
# from projects.mylove4u.models.diary import DiaryDB, DiaryUserLink

# Shared/Auth routes
from shared.auth.routes.users import router as users_router

# Project routes
from projects.make_music.routes.musicalCompositions import router as music_router
from projects.cookAi.routes.recipes import router as cookai_router
from projects.mylove4u.routes.diaries import router as mylove4u_router

from shared.db.config_db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Unified Personal Apps API",
    description="Multi-project API: Music, Cook, Love, Liturgic",
    version="1.0.0",
    lifespan=lifespan
)

# Ajustar CORS conforme criar os apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router, prefix="/auth", tags=["Authentication"])
app.include_router(music_router, prefix="/make_music", tags=["Music"])
app.include_router(cookai_router, prefix="/cook_ai", tags=["cookAi"])
app.include_router(mylove4u_router, prefix="/mylove_fu", tags=["My love 4u"])

@app.get("/")
def root():
    return {
        "message": "Unified Personal Apps API",
        "projects": {
            "music": "/make_music - Cifras e composições musicais",
            "cook": "/cookai - IA para receitas culinárias e web scrapping de receitas", 
            "love": "/love - Momentos especiais do casal",
            "liturgic": "/liturgic - Música sacra e litúrgica"
        },
        "auth": "/auth - Sistema de autenticação"
    }