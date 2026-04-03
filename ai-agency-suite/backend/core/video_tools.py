"""
Video processing tools using MoviePy
"""
import os
from typing import Optional, List, Tuple
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, TextClip,
    CompositeVideoClip, concatenate_videoclips
)
from PIL import Image, ImageDraw, ImageFont
from loguru import logger
from backend.config import settings


class VideoTools:
    """Tools for video creation and editing"""
    
    def __init__(self):
        """Initialize video tools"""
        self.output_dir = settings.VIDEO_OUTPUT_DIR
        self.thumbnail_dir = settings.THUMBNAIL_OUTPUT_DIR
        
        # Parse resolution
        width, height = settings.VIDEO_RESOLUTION.split('x')
        self.width = int(width)
        self.height = int(height)
        self.fps = settings.VIDEO_FPS
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.thumbnail_dir, exist_ok=True)
    
    def create_video_from_images(
        self,
        image_paths: List[str],
        audio_path: Optional[str] = None,
        output_path: Optional[str] = None,
        duration_per_image: float = 3.0,
        transition_duration: float = 0.5
    ) -> str:
        """
        Create video from a list of images
        
        Args:
            image_paths: List of image file paths
            audio_path: Optional audio file path
            output_path: Output video path
            duration_per_image: Duration for each image in seconds
            transition_duration: Crossfade transition duration
        
        Returns:
            Path to generated video
        """
        if not output_path:
            import uuid
            output_path = os.path.join(self.output_dir, f"video_{uuid.uuid4()}.mp4")
        
        try:
            # Create clips from images
            clips = []
            for img_path in image_paths:
                clip = ImageClip(img_path).set_duration(duration_per_image)
                clip = clip.resize((self.width, self.height))
                clips.append(clip)
            
            # Concatenate with transitions
            if len(clips) > 1:
                video = concatenate_videoclips(clips, method="compose")
            else:
                video = clips[0]
            
            # Add audio if provided
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                video = video.set_audio(audio)
            
            # Write video
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac'
            )
            
            logger.info(f"Created video: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            raise
    
    def add_subtitles(
        self,
        video_path: str,
        subtitles: List[Tuple[str, float, float]],
        output_path: Optional[str] = None,
        font_size: int = 40,
        font_color: str = 'white',
        bg_color: str = 'black'
    ) -> str:
        """
        Add subtitles to video
        
        Args:
            video_path: Input video path
            subtitles: List of (text, start_time, end_time) tuples
            output_path: Output video path
            font_size: Subtitle font size
            font_color: Subtitle text color
            bg_color: Subtitle background color
        
        Returns:
            Path to video with subtitles
        """
        if not output_path:
            base, ext = os.path.splitext(video_path)
            output_path = f"{base}_subtitled{ext}"
        
        try:
            video = VideoFileClip(video_path)
            
            # Create subtitle clips
            subtitle_clips = []
            for text, start, end in subtitles:
                txt_clip = TextClip(
                    text,
                    fontsize=font_size,
                    color=font_color,
                    bg_color=bg_color,
                    size=(self.width - 100, None),
                    method='caption'
                )
                txt_clip = txt_clip.set_position(('center', 'bottom'))
                txt_clip = txt_clip.set_start(start).set_end(end)
                subtitle_clips.append(txt_clip)
            
            # Composite video with subtitles
            final_video = CompositeVideoClip([video] + subtitle_clips)
            
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac'
            )
            
            logger.info(f"Added subtitles to video: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error adding subtitles: {e}")
            raise
    
    def generate_thumbnail(
        self,
        title: str,
        output_path: Optional[str] = None,
        background_color: Tuple[int, int, int] = (255, 100, 100),
        text_color: Tuple[int, int, int] = (255, 255, 255)
    ) -> str:
        """
        Generate a thumbnail image
        
        Args:
            title: Title text for thumbnail
            output_path: Output image path
            background_color: RGB background color
            text_color: RGB text color
        
        Returns:
            Path to generated thumbnail
        """
        if not output_path:
            import uuid
            output_path = os.path.join(self.thumbnail_dir, f"thumb_{uuid.uuid4()}.jpg")
        
        try:
            # Create image
            img = Image.new('RGB', (self.width, self.height), background_color)
            draw = ImageDraw.Draw(img)
            
            # Try to use a nice font, fall back to default
            try:
                font = ImageFont.truetype("arial.ttf", 80)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position (centered)
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
            
            # Draw text
            draw.text((x, y), title, fill=text_color, font=font)
            
            # Save thumbnail
            img.save(output_path, quality=95)
            
            logger.info(f"Generated thumbnail: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error generating thumbnail: {e}")
            raise
    
    def trim_video(
        self,
        video_path: str,
        start_time: float,
        end_time: float,
        output_path: Optional[str] = None
    ) -> str:
        """Trim video to specified duration"""
        if not output_path:
            base, ext = os.path.splitext(video_path)
            output_path = f"{base}_trimmed{ext}"
        
        try:
            video = VideoFileClip(video_path)
            trimmed = video.subclip(start_time, end_time)
            
            trimmed.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac'
            )
            
            logger.info(f"Trimmed video: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error trimming video: {e}")
            raise


# Global video tools instance
video_tools = VideoTools()
