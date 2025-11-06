from fastapi import APIRouter, Query, Body, Depends, HTTPException
from sqlmodel import Session, select
from shared.db.config_db import SessionDep
from shared.auth.models.user import UserDB
from ..models.recipe import Recipe, RecipeCreate, RecipeRead
from ..services.scrap import scrap_recipe
from google import genai
import os
from pydantic import BaseModel


router = APIRouter(prefix="/recipes")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@router.post("/scrap")
def extract_scrap_recipe_post(url: str):
    scrap_result = scrap_recipe(url)
    return scrap_result

# class SearchRequest(BaseModel):
#     query: str

# @router.post("/search")
# def search_recipes(request: SearchRequest):
#     query = request.query
#     # Use IA para interpretar a entrada do usuário
#     prompt = f"Encontre receitas com base na seguinte especificação: {query}"
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt,
#     )
    
#     print(response.text)
    
#     # Retorne os resultados gerados pela IA
#     return {"recipes": response.text}

class SearchRequest(BaseModel):
    query: str

@router.post("/search")
def search_recipes(request: SearchRequest):
    query = request.query
    # Use IA para interpretar a entrada do usuário
    prompt = f"""
    Encontre receitas com base na seguinte especificação: {query}.
    Retorne as receitas no seguinte formato JSON puro:
    [
        {{
            "title": "Título da receita",
            "description": "Descrição ou instruções da receita"
        }},
        ...
    ]
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    try:
        # Tenta interpretar a resposta como JSON
        recipes = response.text.strip()
        return {"recipes": recipes}
    except Exception as e:
        print("Erro ao interpretar a resposta:", e)
        return {"error": "Não foi possível processar a resposta da IA."}

# CRUD Operations following make_music pattern

@router.get("/list", response_model=list[RecipeRead])
def get_recipes(session: SessionDep):
    """Lista todas as receitas cadastradas"""
    recipes = session.exec(select(Recipe)).all()
    return recipes

@router.post("/create", response_model=RecipeRead)
def create_recipe(recipe_data: RecipeCreate, session: SessionDep):
    """Cria uma nova receita"""
    new_recipe = Recipe(
        content=recipe_data.content,
        title=recipe_data.title
        # owner_id será adicionado quando implementarmos autenticação
    )
    session.add(new_recipe)
    session.commit()
    session.refresh(new_recipe)
    return new_recipe

@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(recipe_id: int, session: SessionDep):
    """Busca uma receita específica por ID"""
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return recipe

# Rotas específicas para receitas de usuários
@router.post("/user/{user_id}/save", response_model=RecipeRead)
def save_recipe_for_user(user_id: int, recipe_data: RecipeCreate, session: SessionDep):
    """Salva uma receita para um usuário específico"""
    from ..utils.extract_fields import extract_title
    
    # Verifica se o usuário existe
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Cria uma nova receita associada ao usuário
    new_recipe = Recipe(
        content=recipe_data.content,
        title=recipe_data.title,
        owner_id=user_id
    )
    
    # Se não foi fornecido título, tenta extrair automaticamente
    if not new_recipe.title:
        extracted_title = extract_title(new_recipe.content)
        if extracted_title:
            new_recipe.title = extracted_title

    session.add(new_recipe)
    session.commit()
    session.refresh(new_recipe)
    
    return new_recipe

@router.get("/user/{user_id}", response_model=list[RecipeRead])
def get_user_recipes(user_id: int, session: SessionDep):
    """Busca todas as receitas de um usuário específico"""
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    recipes = session.exec(select(Recipe).where(Recipe.owner_id == user_id)).all()
    return recipes

@router.get("/user/{user_id}/{recipe_id}", response_model=RecipeRead)
def get_user_recipe(user_id: int, recipe_id: int, session: SessionDep):
    """Busca uma receita específica de um usuário"""
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    recipe = session.exec(
        select(Recipe).where(Recipe.id == recipe_id, Recipe.owner_id == user_id)
    ).first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    
    return recipe
