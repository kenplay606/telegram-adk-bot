"""
SQLAlchemy database models
All tables include client_id for multi-client support
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.db_client import Base


class Client(Base):
    """Client model - represents a marketing client or personal account (id=0)"""
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    company = Column(String(255))
    industry = Column(String(100))
    
    # Social media accounts
    instagram_account_id = Column(String(255), unique=True, index=True)
    instagram_username = Column(String(100))
    youtube_channel_id = Column(String(255))
    facebook_page_id = Column(String(255))
    
    # Brand voice and preferences
    brand_voice = Column(Text)  # JSON string with tone, style, keywords
    target_audience = Column(Text)
    content_preferences = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="client", cascade="all, delete-orphan")
    content = relationship("Content", back_populates="client", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="client", cascade="all, delete-orphan")
    analytics = relationship("Analytics", back_populates="client", cascade="all, delete-orphan")


class Campaign(Base):
    """Marketing campaign model"""
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    campaign_type = Column(String(50))  # ad, seo, content, email, etc.
    status = Column(String(50), default="draft")  # draft, active, paused, completed
    
    # Campaign details
    target_keywords = Column(JSON)
    budget = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Results
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="campaigns")


class Content(Base):
    """Content model - stores all generated content"""
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    
    title = Column(String(500))
    content_type = Column(String(50))  # video, image, text, website, ad, email, etc.
    platform = Column(String(50))  # instagram, youtube, facebook, website, etc.
    
    # Content data
    text_content = Column(Text)
    media_url = Column(String(500))
    thumbnail_url = Column(String(500))
    meta_data = Column(JSON)  # Additional data like hashtags, captions, etc.
    
    # Status
    status = Column(String(50), default="draft")  # draft, scheduled, published, failed
    scheduled_at = Column(DateTime)
    published_at = Column(DateTime)
    
    # Performance
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="content")


class Lead(Base):
    """Lead model - captured leads for clients"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    
    name = Column(String(255))
    email = Column(String(255), index=True)
    phone = Column(String(50))
    company = Column(String(255))
    
    # Lead source
    source = Column(String(100))  # website, instagram, ad, etc.
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    
    # Lead data
    message = Column(Text)
    meta_data = Column(JSON)
    
    # Status
    status = Column(String(50), default="new")  # new, contacted, qualified, converted, lost
    score = Column(Integer, default=0)  # Lead score 0-100
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="leads")


class Analytics(Base):
    """Analytics model - tracks metrics over time"""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String(50))  # engagement, traffic, conversion, revenue, etc.
    
    # Dimensions
    platform = Column(String(50))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    content_id = Column(Integer, ForeignKey("content.id"))
    
    # Metadata
    meta_data = Column(JSON)
    
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    client = relationship("Client", back_populates="analytics")


class InstagramMessage(Base):
    """Instagram message model - for tracking DM conversations"""
    __tablename__ = "instagram_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    
    instagram_message_id = Column(String(255), unique=True, index=True)
    sender_id = Column(String(255), index=True)
    sender_username = Column(String(100))
    
    message_text = Column(Text)
    message_type = Column(String(50))  # text, image, video, etc.
    
    # Response
    response_text = Column(Text)
    responded_at = Column(DateTime)
    auto_responded = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # No relationship to Client to avoid circular imports
