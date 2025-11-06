from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends

# session -> conexão ativa com o banco, é um objeto

# Nome do arquivo do banco de dados SQLite
sqlite_file_name = "database.db"
# URL de conexão no formato aceito pelo SQLModel/SQLAlchemy
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Argumentos extras para a conexão
# 'check_same_thread': False permite acesso ao banco por múltiplas threads (útil em aplicações web)
connect_args = {"check_same_thread": False}

# Cria o objeto engine, responsável pela comunicação com o banco de dados
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    """
    Cria todas as tabelas no banco de dados conforme os modelos definidos.
    Deve ser chamada uma vez ao iniciar o projeto ou ao atualizar modelos.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Gera uma sessão de conexão com o banco de dados.
    Usada para executar operações (CRUD) dentro dos endpoints.
    """
    with Session(engine) as session:
        yield session

# Dependência do FastAPI para injetar a sessão do banco nos endpoints
SessionDep = Annotated[Session, Depends(get_session)]
