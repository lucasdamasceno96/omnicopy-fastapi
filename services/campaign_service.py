# services/campaign_service.py

from sqlmodel import Session, select
from fastapi import HTTPException
from ..models.schemas import Campaign, CampaignCreate, CampaignUpdate

def get_all_campaigns(session: Session):
    return session.exec(select(Campaign)).all()

def get_campaign_by_id(session: Session, campaign_id: int):
    db_campaign = session.get(Campaign, campaign_id)
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign

def create_campaign(session: Session, campaign_create: CampaignCreate):
    db_campaign = Campaign.model_validate(campaign_create)
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return db_campaign

def update_campaign(session: Session, campaign_id: int, campaign_update: CampaignUpdate):
    db_campaign = get_campaign_by_id(session, campaign_id) # Reutiliza a busca e o erro 404
    
    update_data = campaign_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_campaign, key, value)
        
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return db_campaign

def delete_campaign_by_id(session: Session, campaign_id: int):
    db_campaign = get_campaign_by_id(session, campaign_id) # Reutiliza a busca e o erro 404
    session.delete(db_campaign)
    session.commit()
    return {"message": "Campaign deleted successfully"}