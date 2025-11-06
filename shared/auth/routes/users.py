from datetime import datetime
from fastapi import APIRouter, HTTPException
from ...db.config_db import SessionDep
from ..models import user
from sqlmodel import select

router = APIRouter(prefix="/users")

# depois adicionar os limites na hora de mostrar aqui
@router.get("/", response_model=list[user.UserOut])
def list_users(session: SessionDep):
    """Lista usuarios cadastrados"""
    users = session.exec(select(user.UserDB)).all()
    return users

@router.get("/{user_id}", response_model=user.UserOut)
def read_user_id(user_id: int, session: SessionDep):
    """Lista usuário pelo ID"""
    user_obj = session.get(user.UserDB, user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User não encontrado")
    return user_obj

@router.post("/register", response_model=user.UserOut)
def user_register(user_data: user.UserIn, session: SessionDep):
    user_db = user.UserDB(
        username=user_data.username,
        password=user.hash_password(user_data.password).decode("utf-8"),
        email=user_data.email
        # created_at será preenchido automaticamente
    )
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

# remover a senha do retorno
@router.post("/login", response_model=user.UserOut)
def user_login(login_data: user.UserLogin, session: SessionDep):
    """Efetuar login"""
    # encontrar user via email
    query = select(user.UserDB).where(user.UserDB.email == login_data.email)
    user_obj = session.exec(query).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not user.verify_password(login_data.password, user_obj.password):
        raise HTTPException(status_code=401, detail="Senha incorreta")
    return user_obj

@router.delete("/delete_user/{user_id}")
def delete_user(user_id:int, session: SessionDep):
    user_obj = session.get(user.UserDB, user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    session.delete(user_obj)
    session.commit()
    return {"Msg": f"Usuário {user_id} apagado com sucesso"}
    

