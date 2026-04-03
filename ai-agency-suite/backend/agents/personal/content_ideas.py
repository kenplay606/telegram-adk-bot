"""
Content Ideas Agent - Generates viral content ideas for personal brand
"""
from typing import List, Dict, Any, Optional
from loguru import logger
from backend.agents.base_agent import BaseAgent


class ContentIdeasAgent(BaseAgent):
    """Agent for generating viral content ideas"""
    
    def __init__(self, client_id: int = 0):
        """Initialize for personal content (client_id=0)"""
        super().__init__(client_id, "ContentIdeas")
    
    async def generate_video_ideas(
        self,
        niche: str,
        platform: str = "youtube_shorts",
        count: int = 10,
        trending_topics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate viral video ideas
        
        Args:
            niche: Content niche (finance, tech, lifestyle, etc.)
            platform: Target platform (youtube_shorts, instagram_reels, tiktok)
            count: Number of ideas to generate
            trending_topics: Optional list of trending topics to incorporate
        
        Returns:
            List of video ideas with titles, hooks, and outlines
        """
        logger.info(f"Generating {count} video ideas for {niche} on {platform}")
        
        trending_context = ""
        if trending_topics:
            trending_context = f"\nIncorporate these trending topics: {', '.join(trending_topics)}"
        
        prompt = f"""Generate {count} viral video ideas for {platform} in the {niche} niche.
{trending_context}

For each idea, provide:
1. Title (catchy, clickable)
2. Hook (first 3 seconds to grab attention)
3. Main points (3-5 key points)
4. Call-to-action
5. Estimated duration (15-60 seconds)
6. Viral potential score (1-10)

Focus on:
- Attention-grabbing hooks
- Value-packed content
- Shareability
- Trending formats

Return as JSON array with keys: title, hook, main_points, cta, duration, viral_score"""
        
        result = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt=f"You are a viral content strategist specializing in {platform} content.",
            use_memory=False
        )
        
        ideas = result.get('ideas', result.get('video_ideas', []))
        
        # Store ideas in memory
        for idea in ideas:
            self.memory.add_interaction(
                interaction_type="content_idea",
                content=f"Title: {idea.get('title')}\nHook: {idea.get('hook')}",
                metadata={
                    'niche': niche,
                    'platform': platform,
                    'viral_score': idea.get('viral_score', 0)
                }
            )
        
        return ideas
    
    async def analyze_trending_topics(self, niche: str) -> List[str]:
        """
        Analyze and suggest trending topics in a niche
        
        Args:
            niche: Content niche
        
        Returns:
            List of trending topics
        """
        prompt = f"""Based on current trends, suggest 10 trending topics in the {niche} niche that would work well for short-form video content.

Consider:
- Current events
- Seasonal trends
- Evergreen topics with new angles
- Controversial but safe topics
- Educational trends

Return as JSON array of topic strings."""
        
        result = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are a trend analyst for social media content."
        )
        
        return result.get('topics', result.get('trending_topics', []))
    
    async def generate_content_calendar(
        self,
        niche: str,
        days: int = 30,
        posts_per_day: int = 1
    ) -> Dict[str, Any]:
        """
        Generate a content calendar
        
        Args:
            niche: Content niche
            days: Number of days to plan
            posts_per_day: Posts per day
        
        Returns:
            Content calendar with daily post ideas
        """
        total_posts = days * posts_per_day
        
        prompt = f"""Create a {days}-day content calendar for {niche} content with {posts_per_day} post(s) per day.

For each day, provide:
- Date (Day 1, Day 2, etc.)
- Post title/topic
- Content type (tutorial, tips, story, etc.)
- Key message
- Hashtags

Ensure variety and strategic posting schedule.

Return as JSON with 'calendar' array."""
        
        calendar = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are a content strategist creating posting schedules."
        )
        
        return calendar
    
    async def optimize_idea_for_platform(
        self,
        idea: str,
        source_platform: str,
        target_platform: str
    ) -> Dict[str, Any]:
        """Adapt content idea from one platform to another"""
        prompt = f"""Adapt this content idea from {source_platform} to {target_platform}:

Original Idea: {idea}

Provide:
- Adapted title
- Platform-specific hook
- Format adjustments
- Optimal length
- Platform-specific tips

Return as JSON."""
        
        adapted = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are an expert in cross-platform content adaptation."
        )
        
        return adapted
