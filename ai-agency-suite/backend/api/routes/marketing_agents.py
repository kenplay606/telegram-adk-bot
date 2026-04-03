"""
Marketing agents API routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from backend.agents.marketing.website_builder import WebsiteBuilderAgent
from backend.agents.marketing.ad_designer import AdDesignerAgent
from backend.agents.marketing.instagram_messaging import InstagramMessagingAgent

router = APIRouter()


class WebsiteBuildRequest(BaseModel):
    client_id: int
    business_name: str
    business_type: str
    description: Optional[str] = None
    features: Optional[List[str]] = None


class AdCampaignRequest(BaseModel):
    client_id: int
    campaign_type: str
    platform: str
    target_audience: Optional[str] = None
    budget: Optional[float] = None
    goals: Optional[List[str]] = None


class AdCopyRequest(BaseModel):
    client_id: int
    product_service: str
    platform: str
    tone: str = "professional"
    length: str = "short"


@router.post("/website/build")
async def build_website(request: WebsiteBuildRequest):
    """Build a website for a client"""
    agent = WebsiteBuilderAgent(request.client_id)
    result = await agent.build_website(
        business_name=request.business_name,
        business_type=request.business_type,
        description=request.description,
        features=request.features
    )
    return result


@router.post("/website/optimize-seo")
async def optimize_seo(client_id: int, html_path: str):
    """Optimize website for SEO"""
    agent = WebsiteBuilderAgent(client_id)
    result = await agent.optimize_seo(html_path)
    return result


@router.post("/ads/campaign")
async def create_ad_campaign(request: AdCampaignRequest):
    """Create an advertising campaign"""
    agent = AdDesignerAgent(request.client_id)
    campaign = await agent.create_ad_campaign(
        campaign_type=request.campaign_type,
        platform=request.platform,
        target_audience=request.target_audience,
        budget=request.budget,
        goals=request.goals
    )
    return campaign


@router.post("/ads/copy")
async def generate_ad_copy(request: AdCopyRequest):
    """Generate ad copy variations"""
    agent = AdDesignerAgent(request.client_id)
    copies = await agent.generate_ad_copy(
        product_service=request.product_service,
        platform=request.platform,
        tone=request.tone,
        length=request.length
    )
    return {"ad_copies": copies}


@router.post("/instagram/respond")
async def respond_to_instagram_message(
    client_id: int,
    message_id: str,
    sender_id: str,
    sender_username: str,
    message_text: str
):
    """Process and respond to Instagram message"""
    agent = InstagramMessagingAgent(client_id)
    response = await agent.process_incoming_message(
        message_id=message_id,
        sender_id=sender_id,
        sender_username=sender_username,
        message_text=message_text
    )
    return response


@router.post("/instagram/classify")
async def classify_instagram_message(client_id: int, message_text: str):
    """Classify Instagram message intent"""
    agent = InstagramMessagingAgent(client_id)
    result = await agent.classify_message_intent(message_text)
    return result
