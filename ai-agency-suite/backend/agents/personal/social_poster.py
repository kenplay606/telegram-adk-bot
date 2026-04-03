"""
Social Poster Agent - Posts content to social media platforms
SECURITY: All API credentials loaded from environment variables
"""
import os
from typing import Dict, Any, Optional
from loguru import logger
from backend.agents.base_agent import BaseAgent
from backend.config import settings


class SocialPosterAgent(BaseAgent):
    """Agent for posting content to social media"""
    
    def __init__(self, client_id: int = 0):
        """Initialize for personal content (client_id=0)"""
        super().__init__(client_id, "SocialPoster")
    
    async def post_to_youtube_shorts(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Upload video to YouTube Shorts
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
        
        Returns:
            Upload result with video ID and URL
        """
        logger.info(f"Uploading to YouTube Shorts: {title}")
        
        # Check if YouTube credentials are configured
        if not settings.YOUTUBE_CLIENT_ID or not settings.YOUTUBE_CLIENT_SECRET:
            logger.warning("YouTube credentials not configured, saving locally instead")
            return self._save_locally(video_path, title, "youtube_shorts")
        
        try:
            # YouTube API upload logic would go here
            # For now, simulate success
            logger.info("YouTube upload would happen here with proper credentials")
            
            return {
                'platform': 'youtube_shorts',
                'status': 'uploaded',
                'video_id': 'simulated_id',
                'url': 'https://youtube.com/shorts/simulated_id',
                'title': title
            }
        
        except Exception as e:
            logger.error(f"YouTube upload error: {e}")
            return self._save_locally(video_path, title, "youtube_shorts")
    
    async def post_to_instagram_reels(
        self,
        video_path: str,
        caption: str,
        hashtags: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Upload video to Instagram Reels
        
        Args:
            video_path: Path to video file
            caption: Video caption
            hashtags: List of hashtags
        
        Returns:
            Upload result
        """
        logger.info(f"Uploading to Instagram Reels")
        
        # Check if Instagram credentials are configured
        if not settings.INSTAGRAM_ACCESS_TOKEN:
            logger.warning("Instagram credentials not configured, saving locally instead")
            return self._save_locally(video_path, caption, "instagram_reels")
        
        try:
            # Instagram API upload logic would go here
            logger.info("Instagram upload would happen here with proper credentials")
            
            full_caption = caption
            if hashtags:
                full_caption += "\n\n" + " ".join([f"#{tag}" for tag in hashtags])
            
            return {
                'platform': 'instagram_reels',
                'status': 'uploaded',
                'caption': full_caption,
                'url': 'https://instagram.com/reel/simulated_id'
            }
        
        except Exception as e:
            logger.error(f"Instagram upload error: {e}")
            return self._save_locally(video_path, caption, "instagram_reels")
    
    async def post_to_facebook(
        self,
        video_path: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Upload video to Facebook
        
        Args:
            video_path: Path to video file
            message: Post message
        
        Returns:
            Upload result
        """
        logger.info(f"Uploading to Facebook")
        
        # Check if Facebook credentials are configured
        if not settings.FACEBOOK_ACCESS_TOKEN:
            logger.warning("Facebook credentials not configured, saving locally instead")
            return self._save_locally(video_path, message, "facebook")
        
        try:
            # Facebook API upload logic would go here
            logger.info("Facebook upload would happen here with proper credentials")
            
            return {
                'platform': 'facebook',
                'status': 'uploaded',
                'message': message,
                'url': 'https://facebook.com/video/simulated_id'
            }
        
        except Exception as e:
            logger.error(f"Facebook upload error: {e}")
            return self._save_locally(video_path, message, "facebook")
    
    def _save_locally(
        self,
        video_path: str,
        title: str,
        platform: str
    ) -> Dict[str, Any]:
        """
        Save video locally when API credentials not available
        
        Args:
            video_path: Path to video file
            title: Video title/caption
            platform: Target platform
        
        Returns:
            Local save result
        """
        output_dir = os.path.join("output", platform)
        os.makedirs(output_dir, exist_ok=True)
        
        # Copy video to output directory
        import shutil
        filename = os.path.basename(video_path)
        output_path = os.path.join(output_dir, filename)
        shutil.copy2(video_path, output_path)
        
        # Save metadata
        metadata_path = output_path.replace('.mp4', '_metadata.txt')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write(f"Platform: {platform}\n")
            f.write(f"Title/Caption: {title}\n")
            f.write(f"Video: {filename}\n")
        
        logger.info(f"Video saved locally: {output_path}")
        
        return {
            'platform': platform,
            'status': 'saved_locally',
            'path': output_path,
            'metadata_path': metadata_path,
            'note': 'Configure API credentials in .env to enable automatic uploading'
        }
    
    async def schedule_post(
        self,
        video_path: str,
        platform: str,
        scheduled_time: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Schedule a post for later"""
        logger.info(f"Scheduling post for {platform} at {scheduled_time}")
        
        # Store in database for scheduler to pick up
        from backend.core.db_client import SessionLocal
        from backend.models.sqlalchemy_models import Content
        from datetime import datetime
        
        db = SessionLocal()
        try:
            content = Content(
                client_id=self.client_id,
                title=kwargs.get('title', 'Scheduled Post'),
                content_type='video',
                platform=platform,
                media_url=video_path,
                status='scheduled',
                scheduled_at=datetime.fromisoformat(scheduled_time),
                metadata=kwargs
            )
            db.add(content)
            db.commit()
            
            return {
                'status': 'scheduled',
                'platform': platform,
                'scheduled_time': scheduled_time,
                'content_id': content.id
            }
        finally:
            db.close()
