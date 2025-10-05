# main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from datetime import datetime

from .db.database import create_db_and_tables, engine
from .models.schemas import Campaign
from .routers import campaigns

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    
    # Popula o banco com dados iniciais se estiver vazio
    with Session(engine) as session:
        if not session.exec(select(Campaign)).first():
            session.add_all([
                Campaign(name="Summer Launch", due_date=datetime.now()),
                Campaign(name="Black Friday", due_date=datetime.now()),
            ])
            session.commit()
    yield
    print("Shutting down...")

app = FastAPI(
    lifespan=lifespan,
    title="Campaign Manager API",
    description="A hands-on project to keep coding skills sharp.",
    version="1.0.0",
    root_path="/api/v1" # Opcional: define um prefixo global
)

# Inclui o roteador de campanhas na aplicação principal
app.include_router(campaigns.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Campaign Manager API!"}