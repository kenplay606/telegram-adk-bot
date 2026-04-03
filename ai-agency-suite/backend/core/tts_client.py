"""
Text-to-Speech client supporting both online (gTTS) and offline (pyttsx3)
"""
import os
from typing import Optional
from loguru import logger
from backend.config import settings


class TTSClient:
    """Text-to-Speech client"""
    
    def __init__(self, engine: Optional[str] = None):
        """
        Initialize TTS client
        
        Args:
            engine: 'gtts' (online) or 'pyttsx3' (offline). Defaults to config setting.
        """
        self.engine = engine or settings.TTS_ENGINE
        self.language = settings.TTS_LANGUAGE
        
        if self.engine == 'pyttsx3':
            import pyttsx3
            self.pyttsx_engine = pyttsx3.init()
        
        logger.info(f"TTS Client initialized with engine: {self.engine}")
    
    def text_to_speech(
        self,
        text: str,
        output_path: str,
        language: Optional[str] = None
    ) -> str:
        """
        Convert text to speech audio file
        
        Args:
            text: Text to convert
            output_path: Path to save audio file
            language: Language code (e.g., 'en', 'es'). Defaults to config setting.
        
        Returns:
            Path to generated audio file
        """
        lang = language or self.language
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if self.engine == 'gtts':
            return self._gtts_generate(text, output_path, lang)
        elif self.engine == 'pyttsx3':
            return self._pyttsx3_generate(text, output_path)
        else:
            raise ValueError(f"Unknown TTS engine: {self.engine}")
    
    def _gtts_generate(self, text: str, output_path: str, language: str) -> str:
        """Generate speech using gTTS (online)"""
        try:
            from gtts import gTTS
            
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(output_path)
            
            logger.info(f"Generated TTS audio with gTTS: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"gTTS generation error: {e}")
            raise
    
    def _pyttsx3_generate(self, text: str, output_path: str) -> str:
        """Generate speech using pyttsx3 (offline)"""
        try:
            self.pyttsx_engine.save_to_file(text, output_path)
            self.pyttsx_engine.runAndWait()
            
            logger.info(f"Generated TTS audio with pyttsx3: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"pyttsx3 generation error: {e}")
            raise
    
    def set_voice_properties(self, rate: int = 150, volume: float = 1.0):
        """
        Set voice properties (pyttsx3 only)
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        if self.engine == 'pyttsx3':
            self.pyttsx_engine.setProperty('rate', rate)
            self.pyttsx_engine.setProperty('volume', volume)


# Global TTS client instance
tts_client = TTSClient()
