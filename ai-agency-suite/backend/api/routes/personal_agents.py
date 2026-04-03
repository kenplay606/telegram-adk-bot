"""
Personal content agents API routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from backend.agents.personal.content_ideas import ContentIdeasAgent
from backend.agents.personal.script_writer import ScriptWriterAgent
from backend.agents.personal.video_assembler import VideoAssemblerAgent
from backend.agents.personal.social_poster import SocialPosterAgent

router = APIRouter()


class VideoIdeasRequest(BaseModel):
    niche: str
    platform: str = "youtube_shorts"
    count: int = 10
    trending_topics: Optional[List[str]] = None


class ScriptRequest(BaseModel):
    title: str
    main_points: List[str]
    duration: int = 60
    style: str = "educational"


class VideoCreationRequest(BaseModel):
    script: str
    title: str
    background_images: Optional[List[str]] = None
    add_subtitles: bool = True


class SocialPostRequest(BaseModel):
    video_path: str
    platform: str
    title: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None
    tags: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None


@router.post("/ideas/generate")
async def generate_video_ideas(request: VideoIdeasRequest):
    """Generate viral video ideas"""
    agent = ContentIdeasAgent()
    ideas = await agent.generate_video_ideas(
        niche=request.niche,
        platform=request.platform,
        count=request.count,
        trending_topics=request.trending_topics
    )
    return {"ideas": ideas}


@router.post("/ideas/trending")
async def get_trending_topics(niche: str):
    """Get trending topics for a niche"""
    agent = ContentIdeasAgent()
    topics = await agent.analyze_trending_topics(niche)
    return {"trending_topics": topics}


@router.post("/ideas/calendar")
async def generate_content_calendar(niche: str, days: int = 30, posts_per_day: int = 1):
    """Generate content calendar"""
    agent = ContentIdeasAgent()
    calendar = await agent.generate_content_calendar(niche, days, posts_per_day)
    return calendar


@router.post("/script/write")
async def write_script(request: ScriptRequest):
    """Write a video script"""
    agent = ScriptWriterAgent()
    script = await agent.write_script(
        title=request.title,
        main_points=request.main_points,
        duration=request.duration,
        style=request.style
    )
    return script


@router.post("/script/hooks")
async def generate_hooks(topic: str, count: int = 5):
    """Generate hook variations"""
    agent = ScriptWriterAgent()
    hooks = await agent.generate_hook_variations(topic, count)
    return {"hooks": hooks}


@router.post("/script/ctas")
async def generate_ctas(goal: str, count: int = 3):
    """Generate CTA variations"""
    agent = ScriptWriterAgent()
    ctas = await agent.generate_cta_variations(goal, count)
    return {"ctas": ctas}


@router.post("/video/create")
async def create_video(request: VideoCreationRequest):
    """Create a video from script"""
    agent = VideoAssemblerAgent()
    result = await agent.create_video(
        script=request.script,
        title=request.title,
        background_images=request.background_images,
        add_subtitles=request.add_subtitles
    )
    return result


@router.post("/post/youtube")
async def post_to_youtube(request: SocialPostRequest):
    """Post video to YouTube Shorts"""
    agent = SocialPosterAgent()
    result = await agent.post_to_youtube_shorts(
        video_path=request.video_path,
        title=request.title or "Untitled",
        description=request.description or "",
        tags=request.tags
    )
    return result


@router.post("/post/instagram")
async def post_to_instagram(request: SocialPostRequest):
    """Post video to Instagram Reels"""
    agent = SocialPosterAgent()
    result = await agent.post_to_instagram_reels(
        video_path=request.video_path,
        caption=request.caption or "",
        hashtags=request.hashtags
    )
    return result


@router.post("/post/facebook")
async def post_to_facebook(request: SocialPostRequest):
    """Post video to Facebook"""
    agent = SocialPosterAgent()
    result = await agent.post_to_facebook(
        video_path=request.video_path,
        message=request.caption or request.description or ""
    )
    return result


@router.post("/post/schedule")
async def schedule_post(
    video_path: str,
    platform: str,
    scheduled_time: str,
    title: Optional[str] = None,
    description: Optional[str] = None
):
    """Schedule a post for later"""
    agent = SocialPosterAgent()
    result = await agent.schedule_post(
        video_path=video_path,
        platform=platform,
        scheduled_time=scheduled_time,
        title=title,
        description=description
    )
    return result
