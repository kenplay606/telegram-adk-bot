"""
Webhook endpoints for Instagram and other platforms
SECURITY: Webhook verification tokens loaded from environment
"""
from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from backend.config import settings
from backend.agents.marketing.instagram_messaging import InstagramMessagingAgent
from backend.core.db_client import SessionLocal
from backend.models.sqlalchemy_models import Client

router = APIRouter()


@router.get("/instagram")
async def instagram_webhook_verify(request: Request):
    """
    Instagram webhook verification
    Facebook sends a GET request to verify the webhook
    """
    params = request.query_params
    
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    
    if mode == "subscribe" and token == settings.INSTAGRAM_VERIFY_TOKEN:
        logger.info("Instagram webhook verified")
        return int(challenge)
    else:
        raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/instagram")
async def instagram_webhook_receive(request: Request):
    """
    Instagram webhook receiver
    Handles incoming messages and automatically responds
    """
    try:
        data = await request.json()
        logger.info(f"Instagram webhook received: {data}")
        
        # Process webhook data
        if data.get("object") == "instagram":
            for entry in data.get("entry", []):
                # Get messaging events
                messaging = entry.get("messaging", [])
                
                for event in messaging:
                    sender_id = event.get("sender", {}).get("id")
                    recipient_id = event.get("recipient", {}).get("id")
                    
                    # Check if this is a message event
                    if "message" in event:
                        message = event["message"]
                        message_id = message.get("mid")
                        message_text = message.get("text", "")
                        
                        # Find client by Instagram account ID
                        db = SessionLocal()
                        try:
                            client = db.query(Client).filter(
                                Client.instagram_account_id == recipient_id
                            ).first()
                            
                            if client:
                                # Process message with agent
                                agent = InstagramMessagingAgent(client.id)
                                response = await agent.process_incoming_message(
                                    message_id=message_id,
                                    sender_id=sender_id,
                                    sender_username=sender_id,  # Would need to fetch username
                                    message_text=message_text
                                )
                                
                                logger.info(f"Auto-responded to Instagram message for client {client.id}")
                            else:
                                logger.warning(f"No client found for Instagram account {recipient_id}")
                        
                        finally:
                            db.close()
        
        return {"status": "received"}
    
    except Exception as e:
        logger.error(f"Instagram webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def test_webhook():
    """Test endpoint for webhook testing"""
    return {"status": "webhook test successful"}
