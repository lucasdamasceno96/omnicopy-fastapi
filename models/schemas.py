# models/schemas.py

from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Session
from pydantic import BaseModel
from typing import TypeVar, Generic

# Modelo da Tabela do Banco de Dados
class Campaign(SQLModel, table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )

# Modelo para Criação (Entrada de dados na API)
class CampaignCreate(SQLModel):
    name: str
    due_date: datetime | None = None

# Modelo para Atualização (Entrada de dados na API)
class CampaignUpdate(SQLModel):
    name: str | None = None
    due_date: datetime | None = None

# Modelo de Resposta Genérico
T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    data: T