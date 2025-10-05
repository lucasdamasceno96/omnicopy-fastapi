# routers/campaigns.py

from fastapi import APIRouter
from ..models.schemas import Campaign, CampaignCreate, CampaignUpdate, Response
from ..db.database import SessionDep
from ..services import campaign_service

router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"],
)

@router.get("", response_model=Response[list[Campaign]])
async def read_campaigns(session: SessionDep):
    data = campaign_service.get_all_campaigns(session)
    return {"data": data}

@router.get("/{campaign_id}", response_model=Response[Campaign])
async def read_campaign(campaign_id: int, session: SessionDep):
    data = campaign_service.get_campaign_by_id(session, campaign_id)
    return {"data": data}

@router.post("", response_model=Response[Campaign], status_code=201)
async def create_campaign(campaign: CampaignCreate, session: SessionDep):
    data = campaign_service.create_campaign(session, campaign)
    return {"data": data}

@router.put("/{campaign_id}", response_model=Response[Campaign])
async def update_campaign(campaign_id: int, campaign_update: CampaignUpdate, session: SessionDep):
    data = campaign_service.update_campaign(session, campaign_id, campaign_update)
    return {"data": data}

@router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: int, session: SessionDep):
    return campaign_service.delete_campaign_by_id(session, campaign_id)