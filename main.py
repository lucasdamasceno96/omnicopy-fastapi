from datetime import datetime
from random import randint
from fastapi import FastAPI, Request
from typing import Any
from fastapi import HTTPException

app = FastAPI(root_path="/api/v1")

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