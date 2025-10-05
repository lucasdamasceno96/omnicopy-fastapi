# db/database.py

from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends
from typing import Annotated

# 1. Configuração do Banco
SQL_FILE_NAME = "database.db"
SQLITE_URL = f"sqlite:///{SQL_FILE_NAME}"
CONNECT_ARGS = {"check_same_thread": False}

engine = create_engine(SQLITE_URL, connect_args=CONNECT_ARGS)

# 2. Função para criar as tabelas
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 3. Função de Dependência para obter a sessão
def get_session():
    with Session(engine) as session:
        yield session

# 4. Dependência para ser usada nos endpoints
SessionDep = Annotated[Session, Depends(get_session)]