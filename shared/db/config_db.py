from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
import os

# Carrega o .env automaticamente (busca no diretório atual e pais)
load_dotenv()

# Validação das variáveis de ambiente
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT", "5432")  # Porta padrão do PostgreSQL
DB_NAME = os.environ.get("DB_NAME")

# Validação de variáveis obrigatórias
required_vars = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST,
    "DB_NAME": DB_NAME
}

missing = [k for k, v in required_vars.items() if not v]
if missing:
    raise EnvironmentError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing)}")

print(f"Conectando ao banco de dados em {DB_HOST}:{DB_PORT}/{DB_NAME} como usuário {DB_USER}")

# Construindo a URL de conexão de forma segura COM A PORTA
DATABASE_URL = f"postgresql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criando o engine com suporte a UTF-8
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"client_encoding": "utf8"},
    pool_pre_ping=True  # Verifica se a conexão está ativa antes de usar
)

def create_db_and_tables():
    """
    Cria todas as tabelas no banco de dados conforme os modelos definidos.
    Deve ser chamada uma vez ao iniciar o projeto ou ao atualizar modelos.
    """
    SQLModel.metadata.create_all(engine)

# Mantém compatibilidade com código antigo
def init_db():
    """Alias para create_db_and_tables()"""
    create_db_and_tables()

def get_session():
    """
    Gera uma sessão de conexão com o banco de dados.
    Usada para executar operações (CRUD) dentro dos endpoints.
    """
    with Session(engine) as session:
        yield session

# Dependência do FastAPI para injetar a sessão do banco nos endpoints
SessionDep = Annotated[Session, Depends(get_session)]

# Modo de teste (descomentado caso necessário)
# if os.getenv("ENV") == "test":
#     print("\n\n ambiente: ", os.getenv("ENV"), "\n\n")
#     print("Modo de teste ativado: o banco de dados será reiniciado a cada inicialização.")
#     def create_db_and_tables():
#         SQLModel.metadata.drop_all(engine)  # Exclui todas as tabelas
#         SQLModel.metadata.create_all(engine)  # Recria todas as tabelas