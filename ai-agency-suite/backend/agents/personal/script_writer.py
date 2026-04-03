"""
Script Writer Agent - Writes video scripts for shorts/reels
"""
from typing import Dict, Any, Optional, List
from loguru import logger
from backend.agents.base_agent import BaseAgent


class ScriptWriterAgent(BaseAgent):
    """Agent for writing video scripts"""
    
    def __init__(self, client_id: int = 0):
        """Initialize for personal content (client_id=0)"""
        super().__init__(client_id, "ScriptWriter")
    
    async def write_script(
        self,
        title: str,
        main_points: List[str],
        duration: int = 60,
        style: str = "educational",
        include_timestamps: bool = True
    ) -> Dict[str, Any]:
        """
        Write a complete video script
        
        Args:
            title: Video title
            main_points: Key points to cover
            duration: Target duration in seconds
            style: Script style (educational, entertaining, storytelling, etc.)
            include_timestamps: Whether to include timestamps
        
        Returns:
            Complete script with sections and timing
        """
        logger.info(f"Writing {duration}s script for: {title}")
        
        points_text = "\n".join([f"- {point}" for point in main_points])
        
        prompt = f"""Write a {duration}-second video script for a short-form video:

Title: {title}
Style: {style}
Key Points to Cover:
{points_text}

Script Structure:
1. Hook (0-3s): Grab attention immediately
2. Introduction (3-8s): Set context
3. Main Content (8-{duration-10}s): Deliver value
4. Call-to-Action ({duration-10}-{duration}s): Engage viewers

Requirements:
- Write for spoken delivery
- Use simple, conversational language
- Include pauses and emphasis markers
- Make it engaging and fast-paced
- Include visual cues in [brackets]
{"- Include timestamps for each section" if include_timestamps else ""}

Return as JSON with: hook, introduction, main_content, cta, full_script, estimated_duration, visual_cues"""
        
        script = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt=f"You are an expert scriptwriter for viral short-form videos in {style} style.",
            use_memory=False
        )
        
        # Store script in memory
        self.memory.add_interaction(
            interaction_type="script_written",
            content=f"Title: {title}\nScript: {script.get('full_script', '')[:500]}",
            metadata={
                'title': title,
                'duration': duration,
                'style': style
            }
        )
        
        return script
    
    async def generate_hook_variations(
        self,
        topic: str,
        count: int = 5
    ) -> List[str]:
        """
        Generate multiple hook variations for A/B testing
        
        Args:
            topic: Video topic
            count: Number of hooks to generate
        
        Returns:
            List of hook variations
        """
        prompt = f"""Generate {count} different attention-grabbing hooks for a video about: {topic}

Each hook should:
- Be 1-2 sentences (3 seconds max)
- Create curiosity or urgency
- Use different psychological triggers
- Be unique from each other

Triggers to use: curiosity, fear of missing out, controversy, surprising fact, question

Return as JSON array of hook strings."""
        
        result = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are an expert at writing viral video hooks."
        )
        
        return result.get('hooks', [])
    
    async def add_subtitles_timing(
        self,
        script: str,
        duration: int
    ) -> List[Dict[str, Any]]:
        """
        Generate subtitle timing for script
        
        Args:
            script: Full script text
            duration: Video duration in seconds
        
        Returns:
            List of subtitle segments with timing
        """
        prompt = f"""Break this script into subtitle segments with timing:

Script: {script}
Duration: {duration} seconds

Requirements:
- Each subtitle should be 2-5 words
- Timing should be natural for speech
- Include start and end times
- Optimize for readability

Return as JSON array with: text, start_time, end_time"""
        
        subtitles = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are an expert at creating subtitle timing for videos."
        )
        
        return subtitles.get('subtitles', [])
    
    async def optimize_script_for_platform(
        self,
        script: str,
        platform: str
    ) -> Dict[str, Any]:
        """Optimize script for specific platform"""
        prompt = f"""Optimize this script for {platform}:

Original Script: {script}

Platform-specific optimizations for {platform}:
- Adjust pacing
- Modify language/tone
- Add platform-specific elements
- Optimize length

Return as JSON with: optimized_script, changes_made, platform_tips"""
        
        optimized = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt=f"You are an expert in {platform} content optimization."
        )
        
        return optimized
    
    async def generate_cta_variations(
        self,
        goal: str,
        count: int = 3
    ) -> List[str]:
        """Generate call-to-action variations"""
        prompt = f"""Generate {count} compelling call-to-action variations for this goal: {goal}

Each CTA should:
- Be clear and actionable
- Create urgency
- Be platform-appropriate
- Use different approaches

Return as JSON array of CTA strings."""
        
        result = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are an expert at writing high-converting CTAs."
        )
        
        return result.get('ctas', [])
