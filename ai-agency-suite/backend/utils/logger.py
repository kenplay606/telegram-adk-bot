"""
Logging configuration using Loguru
"""
import sys
from loguru import logger
from backend.config import settings


def setup_logger():
    """Configure logger"""
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL
    )
    
    # Add file handler
    logger.add(
        settings.LOG_FILE,
        rotation="10 MB",
        retention="30 days",
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"
    )
    
    logger.info("Logger initialized")


# Initialize logger on import
setup_logger()
