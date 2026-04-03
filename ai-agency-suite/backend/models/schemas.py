"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# Client Schemas
class ClientBase(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    industry: Optional[str] = None
    instagram_account_id: Optional[str] = None
    instagram_username: Optional[str] = None
    youtube_channel_id: Optional[str] = None
    facebook_page_id: Optional[str] = None
    brand_voice: Optional[str] = None
    target_audience: Optional[str] = None
    content_preferences: Optional[Dict[str, Any]] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    instagram_account_id: Optional[str] = None
    instagram_username: Optional[str] = None
    brand_voice: Optional[str] = None
    target_audience: Optional[str] = None
    content_preferences: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ClientResponse(ClientBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Campaign Schemas
class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    campaign_type: str
    target_keywords: Optional[List[str]] = None
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class CampaignCreate(CampaignBase):
    client_id: int


class CampaignResponse(CampaignBase):
    id: int
    client_id: int
    status: str
    impressions: int
    clicks: int
    conversions: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Content Schemas
class ContentBase(BaseModel):
    title: Optional[str] = None
    content_type: str
    platform: str
    text_content: Optional[str] = None
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None


class ContentCreate(ContentBase):
    client_id: int


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    text_content: Optional[str] = None
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    meta_data: Optional[Dict[str, Any]] = None


class ContentResponse(ContentBase):
    id: int
    client_id: int
    status: str
    scheduled_at: Optional[datetime]
    published_at: Optional[datetime]
    views: int
    likes: int
    comments: int
    shares: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Lead Schemas
class LeadBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    source: str
    message: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None


class LeadCreate(LeadBase):
    client_id: int


class LeadResponse(LeadBase):
    id: int
    client_id: int
    status: str
    score: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Agent Request/Response Schemas
class GenerateContentRequest(BaseModel):
    client_id: int
    content_type: str = Field(..., description="Type: video_script, ad_copy, email, website, etc.")
    platform: str = Field(..., description="Platform: instagram, youtube, facebook, website")
    topic: Optional[str] = None
    keywords: Optional[List[str]] = None
    additional_context: Optional[str] = None


class GenerateContentResponse(BaseModel):
    content_id: int
    content: str
    meta_data: Dict[str, Any]


class VideoGenerationRequest(BaseModel):
    script: str
    title: str
    duration: Optional[int] = 60  # seconds
    resolution: Optional[str] = "1080x1920"
    background_music: Optional[str] = None


class VideoGenerationResponse(BaseModel):
    video_url: str
    thumbnail_url: str
    duration: float
    file_size: int


# Instagram Webhook Schemas
class InstagramWebhookEntry(BaseModel):
    id: str
    time: int
    messaging: Optional[List[Dict[str, Any]]] = None


class InstagramWebhook(BaseModel):
    object: str
    entry: List[InstagramWebhookEntry]
