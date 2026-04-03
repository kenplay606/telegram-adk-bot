"""
Ad Designer Agent - Creates advertising copy and campaigns
"""
from typing import Dict, Any, List, Optional
from loguru import logger
from backend.agents.base_agent import BaseAgent


class AdDesignerAgent(BaseAgent):
    """Agent for designing advertising campaigns"""
    
    def __init__(self, client_id: int):
        super().__init__(client_id, "AdDesigner")
    
    async def create_ad_campaign(
        self,
        campaign_type: str,
        platform: str,
        target_audience: Optional[str] = None,
        budget: Optional[float] = None,
        goals: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a complete ad campaign
        
        Args:
            campaign_type: Type of campaign (awareness, conversion, engagement)
            platform: Platform (facebook, instagram, google, linkedin)
            target_audience: Target audience description
            budget: Campaign budget
            goals: List of campaign goals
        
        Returns:
            Complete campaign with ad copy, targeting, and strategy
        """
        logger.info(f"Creating {campaign_type} campaign for {platform}")
        
        prompt = f"""Create a comprehensive advertising campaign:

Campaign Type: {campaign_type}
Platform: {platform}
Target Audience: {target_audience or 'General audience'}
Budget: ${budget or 'Not specified'}
Goals: {', '.join(goals) if goals else 'Increase brand awareness and engagement'}

Provide:
1. Campaign strategy
2. Ad copy variations (3-5 options)
3. Targeting recommendations
4. Budget allocation
5. Success metrics

Return as JSON with keys: strategy, ad_copies, targeting, budget_plan, metrics"""
        
        campaign = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are an expert digital marketing strategist specializing in paid advertising."
        )
        
        # Store campaign in memory
        self.memory.add_interaction(
            interaction_type="ad_campaign_created",
            content=f"{campaign_type} campaign for {platform}",
            metadata={
                'platform': platform,
                'campaign_type': campaign_type,
                'budget': budget
            }
        )
        
        return campaign
    
    async def generate_ad_copy(
        self,
        product_service: str,
        platform: str,
        tone: str = "professional",
        length: str = "short"
    ) -> List[str]:
        """
        Generate multiple ad copy variations
        
        Args:
            product_service: Product or service to advertise
            platform: Advertising platform
            tone: Tone of voice (professional, casual, urgent, friendly)
            length: Length (short, medium, long)
        
        Returns:
            List of ad copy variations
        """
        prompt = f"""Generate 5 compelling ad copy variations for:

Product/Service: {product_service}
Platform: {platform}
Tone: {tone}
Length: {length}

Each ad should:
- Grab attention immediately
- Highlight key benefits
- Include a clear call-to-action
- Be optimized for {platform}

Return as JSON array of ad copies."""
        
        result = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are an expert copywriter specializing in high-converting ad copy."
        )
        
        return result.get('ad_copies', result.get('ads', []))
    
    async def create_social_media_ad(
        self,
        platform: str,
        objective: str,
        visual_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create social media ad with copy and visual suggestions"""
        prompt = f"""Create a social media ad for {platform}:

Objective: {objective}
Visual Concept: {visual_description or 'Eye-catching, professional imagery'}

Provide:
1. Headline (attention-grabbing)
2. Primary text/caption
3. Call-to-action
4. Visual recommendations
5. Hashtag suggestions (if applicable)

Return as JSON."""
        
        ad = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt=f"You are a social media advertising expert for {platform}."
        )
        
        return ad
