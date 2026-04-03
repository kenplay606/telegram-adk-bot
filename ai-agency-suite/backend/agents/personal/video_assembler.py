"""
Video Assembler Agent - Creates videos from scripts using MoviePy and TTS
"""
import os
from typing import Dict, Any, Optional, List
from loguru import logger
from backend.agents.base_agent import BaseAgent
from backend.core.tts_client import tts_client
from backend.core.video_tools import video_tools


class VideoAssemblerAgent(BaseAgent):
    """Agent for assembling videos from scripts"""
    
    def __init__(self, client_id: int = 0):
        """Initialize for personal content (client_id=0)"""
        super().__init__(client_id, "VideoAssembler")
        self.tts = tts_client
        self.video_tools = video_tools
    
    async def create_video(
        self,
        script: str,
        title: str,
        background_images: Optional[List[str]] = None,
        background_color: tuple = (30, 30, 30),
        add_subtitles: bool = True,
        music_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a complete video from script
        
        Args:
            script: Video script text
            title: Video title
            background_images: List of background image paths
            background_color: Background color if no images
            add_subtitles: Whether to add subtitles
            music_path: Optional background music path
        
        Returns:
            Video metadata including path, duration, etc.
        """
        logger.info(f"Creating video: {title}")
        
        # Generate audio from script
        import uuid
        audio_id = str(uuid.uuid4())
        audio_path = os.path.join("temp_videos", f"audio_{audio_id}.mp3")
        os.makedirs("temp_videos", exist_ok=True)
        
        self.tts.text_to_speech(script, audio_path)
        
        # If no background images, create simple colored background
        if not background_images:
            from PIL import Image
            img_path = os.path.join("temp_videos", f"bg_{audio_id}.png")
            img = Image.new('RGB', (1080, 1920), background_color)
            img.save(img_path)
            background_images = [img_path]
        
        # Create video from images and audio
        video_path = self.video_tools.create_video_from_images(
            image_paths=background_images,
            audio_path=audio_path,
            duration_per_image=3.0
        )
        
        # Add subtitles if requested
        if add_subtitles:
            # Generate subtitle timing
            from backend.agents.personal.script_writer import ScriptWriterAgent
            script_writer = ScriptWriterAgent(self.client_id)
            
            # Get video duration
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(video_path)
            duration = clip.duration
            clip.close()
            
            subtitles_data = await script_writer.add_subtitles_timing(script, int(duration))
            
            if subtitles_data:
                # Convert to format expected by video_tools
                subtitles = [
                    (sub['text'], sub['start_time'], sub['end_time'])
                    for sub in subtitles_data
                ]
                video_path = self.video_tools.add_subtitles(video_path, subtitles)
        
        # Generate thumbnail
        thumbnail_path = self.video_tools.generate_thumbnail(title)
        
        # Get final video info
        from moviepy.editor import VideoFileClip
        final_clip = VideoFileClip(video_path)
        duration = final_clip.duration
        file_size = os.path.getsize(video_path)
        final_clip.close()
        
        result = {
            'video_path': video_path,
            'thumbnail_path': thumbnail_path,
            'audio_path': audio_path,
            'duration': duration,
            'file_size': file_size,
            'title': title,
            'resolution': f"{self.video_tools.width}x{self.video_tools.height}"
        }
        
        # Store in memory
        self.memory.add_interaction(
            interaction_type="video_created",
            content=f"Created video: {title}",
            metadata={
                'title': title,
                'duration': duration,
                'file_size': file_size
            }
        )
        
        logger.info(f"Video created successfully: {video_path}")
        return result
    
    async def create_slideshow_video(
        self,
        images: List[str],
        captions: List[str],
        title: str,
        duration_per_slide: float = 3.0
    ) -> Dict[str, Any]:
        """Create a slideshow-style video"""
        logger.info(f"Creating slideshow video: {title}")
        
        # Generate narration from captions
        full_script = " ".join(captions)
        
        import uuid
        audio_id = str(uuid.uuid4())
        audio_path = os.path.join("temp_videos", f"audio_{audio_id}.mp3")
        
        self.tts.text_to_speech(full_script, audio_path)
        
        # Create video
        video_path = self.video_tools.create_video_from_images(
            image_paths=images,
            audio_path=audio_path,
            duration_per_image=duration_per_slide
        )
        
        thumbnail_path = self.video_tools.generate_thumbnail(title)
        
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(video_path)
        duration = clip.duration
        file_size = os.path.getsize(video_path)
        clip.close()
        
        return {
            'video_path': video_path,
            'thumbnail_path': thumbnail_path,
            'duration': duration,
            'file_size': file_size,
            'title': title
        }
    
    async def add_intro_outro(
        self,
        video_path: str,
        intro_text: Optional[str] = None,
        outro_text: Optional[str] = None
    ) -> str:
        """Add intro and outro to video"""
        # This would require creating intro/outro clips and concatenating
        # Simplified version for now
        logger.info("Adding intro/outro to video")
        
        # For now, just return the original path
        # In a full implementation, you would:
        # 1. Create intro clip with text
        # 2. Create outro clip with text
        # 3. Concatenate intro + video + outro
        
        return video_path
