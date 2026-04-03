"""
Instagram Messaging Agent - Handles Instagram DM automation
"""
from typing import Dict, Any, Optional
from loguru import logger
from backend.agents.base_agent import BaseAgent
from backend.core.db_client import SessionLocal
from backend.models.sqlalchemy_models import InstagramMessage


class InstagramMessagingAgent(BaseAgent):
    """Agent for handling Instagram direct messages"""
    
    def __init__(self, client_id: int):
        super().__init__(client_id, "InstagramMessaging")
    
    async def process_incoming_message(
        self,
        message_id: str,
        sender_id: str,
        sender_username: str,
        message_text: str
    ) -> Dict[str, Any]:
        """
        Process incoming Instagram message and generate response
        
        Args:
            message_id: Instagram message ID
            sender_id: Sender's Instagram ID
            sender_username: Sender's username
            message_text: Message content
        
        Returns:
            Response message and metadata
        """
        logger.info(f"Processing Instagram message from {sender_username}")
        
        # Check if this is a follow-up message
        recent_messages = self.memory.recall_similar(
            query=f"Instagram message from {sender_username}",
            n_results=3,
            interaction_type="instagram_message"
        )
        
        # Generate contextual response
        context = ""
        if recent_messages:
            context = "\n\nPrevious conversation:\n"
            for msg in recent_messages:
                context += f"- {msg['text'][:100]}\n"
        
        prompt = f"""Generate a professional, helpful response to this Instagram DM:

From: {sender_username}
Message: {message_text}
{context}

Requirements:
- Be friendly and professional
- Address their question/concern
- Provide value
- Include a call-to-action if appropriate
- Keep it concise (Instagram DM style)

Generate only the response text, no explanations."""
        
        response_text = await self.generate_with_context(
            prompt=prompt,
            system_prompt="You are a helpful customer service representative responding to Instagram messages.",
            use_memory=True
        )
        
        # Store message and response in database
        db = SessionLocal()
        try:
            ig_message = InstagramMessage(
                client_id=self.client_id,
                instagram_message_id=message_id,
                sender_id=sender_id,
                sender_username=sender_username,
                message_text=message_text,
                response_text=response_text,
                auto_responded=True
            )
            db.add(ig_message)
            db.commit()
        finally:
            db.close()
        
        # Store in memory
        self.memory.add_interaction(
            interaction_type="instagram_message",
            content=f"From {sender_username}: {message_text}\nResponse: {response_text}",
            metadata={
                'sender': sender_username,
                'sender_id': sender_id,
                'message_id': message_id
            }
        )
        
        return {
            'response_text': response_text,
            'sender_username': sender_username,
            'auto_responded': True
        }
    
    async def generate_story_reply(
        self,
        story_content: str,
        sender_username: str
    ) -> str:
        """Generate reply to Instagram story mention"""
        prompt = f"""Generate a friendly reply to someone who mentioned us in their Instagram story:

Story content: {story_content}
User: {sender_username}

Create a warm, engaging response that:
- Thanks them for the mention
- Encourages further engagement
- Is authentic and on-brand

Keep it brief and Instagram-appropriate."""
        
        response = await self.generate_with_context(
            prompt=prompt,
            system_prompt="You are managing Instagram engagement for a brand.",
            use_memory=False
        )
        
        return response.strip()
    
    async def classify_message_intent(self, message_text: str) -> Dict[str, Any]:
        """Classify the intent of an incoming message"""
        prompt = f"""Classify the intent of this Instagram message:

Message: {message_text}

Possible intents:
- inquiry (asking about products/services)
- support (needs help)
- feedback (providing feedback)
- collaboration (business opportunity)
- spam
- other

Return JSON with: intent, confidence (0-1), suggested_action"""
        
        result = await self.generate_json_with_context(
            prompt=prompt,
            system_prompt="You are an AI that classifies customer messages."
        )
        
        return result
