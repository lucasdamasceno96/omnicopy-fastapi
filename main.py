from datetime import datetime, timezone
from random import randint
#import select
from fastapi import FastAPI, Request, HTTPException, Depends
from typing import Annotated, Any
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select, Field

class Campaign(SQLModel, table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),nullable=True,index=True)


sql_file_name = "database.db"
sqlite_url = f"sqlite:///{sql_file_name}"
connect_args= {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
    
SessionDep = Annotated[Session, Depends(get_session)]
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Campaign)).first():
            session.add_all([
                Campaign(name="Summer Launch", due_date=datetime.now()),
                Campaign(name="Black Friday", due_date=datetime.now()),
            ])
            session.commit()
    yield

app = FastAPI(root_path="/api/v1", lifespan=lifespan)

@app.get("/")
async def root():
    return{"message":"Hello World from fastAPI !"}

data: Any = [
    {
        "campaign_id":1,
        "name": "Summer Launch",
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    },
    {
        "campaign_id":2,
        "name": "Black Friday",
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    }
]


@app.get("/campaigns")
async def read_campaigns(session: SessionDep):
    data = session.exec(select(Campaign)).all()
    return {"campaigns": data}
