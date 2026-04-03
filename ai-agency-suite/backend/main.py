"""
FastAPI Main Application
SECURITY: All sensitive data loaded from environment variables
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from backend.config import settings
from backend.core.db_client import init_db
from backend.utils.logger import setup_logger

# Initialize logger
setup_logger()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-client marketing agency + personal content automation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting AI Agency Suite...")
    init_db()
    logger.info("AI Agency Suite started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down AI Agency Suite...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Import and include routers
from backend.api.routes import clients, marketing_agents, personal_agents, webhook

app.include_router(clients.router, prefix="/api/clients", tags=["Clients"])
app.include_router(marketing_agents.router, prefix="/api/marketing", tags=["Marketing"])
app.include_router(personal_agents.router, prefix="/api/personal", tags=["Personal Content"])
app.include_router(webhook.router, prefix="/api/webhook", tags=["Webhooks"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
