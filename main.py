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
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{campaign_id}")
async def read_campaign(campaign_id: int):
    for campaign in data:
        if campaign["campaign_id"] == campaign_id:
            return {"campaign": campaign}
        raise HTTPException(status_code=404, detail="Campaign not found")


@app.post("/campaigns",status_code=201)
async def create_campaign(body: dict[str, Any], request: Request):
    body = await request.json()

    new: Any = {
        "campaign_id":randint(100,1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now(),
}
    
    data.append(new)
    return {"campaign": new}

@app.put("/campaigns/{campaign_id}")
async def update_campaign(campaign_id: int, body: dict[str, Any]):
    for campaign in data:
        if campaign["campaign_id"] == campaign_id:
            campaign["name"] = body.get("name", campaign["name"])
            campaign["due_date"] = body.get("due_date", campaign["due_date"])
            return {"campaign": campaign}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.delete("/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: int):
    campaign_to_delete = None
    for campaign in data:
        if campaign["campaign_id"] == campaign_id:
            campaign_to_delete = campaign
            break
    if campaign_to_delete:
        data.remove(campaign_to_delete)
        return {"deleted_campaign": campaign_to_delete}
    else:
        raise HTTPException(status_code=404, detail="Campaign not found")