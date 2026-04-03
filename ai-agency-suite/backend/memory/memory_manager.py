"""
Memory Manager - Combines SQL and vector storage for comprehensive memory
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger
from backend.memory.chroma_client import chroma_client
from backend.core.db_client import SessionLocal
from backend.models.sqlalchemy_models import Client


class MemoryManager:
    """Manages client memories using both SQL and vector storage"""
    
    def __init__(self, client_id: int):
        """Initialize memory manager for a specific client"""
        self.client_id = client_id
        self.chroma = chroma_client
    
    def add_interaction(
        self,
        interaction_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store an interaction in memory
        
        Args:
            interaction_type: Type of interaction (message, content_generated, campaign, etc.)
            content: The interaction content
            metadata: Additional metadata
        
        Returns:
            Memory ID
        """
        if not metadata:
            metadata = {}
        
        metadata.update({
            'type': interaction_type,
            'timestamp': datetime.utcnow().isoformat(),
            'client_id': self.client_id
        })
        
        memory_id = self.chroma.add_memory(
            client_id=self.client_id,
            text=content,
            metadata=metadata
        )
        
        logger.info(f"Stored {interaction_type} interaction for client {self.client_id}")
        return memory_id
    
    def recall_similar(
        self,
        query: str,
        n_results: int = 5,
        interaction_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Recall similar memories based on query
        
        Args:
            query: Search query
            n_results: Number of results to return
            interaction_type: Filter by interaction type
        
        Returns:
            List of similar memories
        """
        filter_metadata = None
        if interaction_type:
            filter_metadata = {'type': interaction_type}
        
        memories = self.chroma.search_memories(
            client_id=self.client_id,
            query=query,
            n_results=n_results,
            filter_metadata=filter_metadata
        )
        
        return memories
    
    def get_recent_interactions(
        self,
        limit: int = 10,
        interaction_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get recent interactions"""
        all_memories = self.chroma.get_all_memories(
            client_id=self.client_id,
            limit=limit * 2  # Get more to filter
        )
        
        # Filter by type if specified
        if interaction_type:
            all_memories = [
                m for m in all_memories
                if m.get('metadata', {}).get('type') == interaction_type
            ]
        
        # Sort by timestamp (most recent first)
        all_memories.sort(
            key=lambda x: x.get('metadata', {}).get('timestamp', ''),
            reverse=True
        )
        
        return all_memories[:limit]
    
    def get_client_context(self) -> Dict[str, Any]:
        """
        Get comprehensive client context including brand voice, preferences, etc.
        
        Returns:
            Dictionary with client context
        """
        db = SessionLocal()
        try:
            client = db.query(Client).filter(Client.id == self.client_id).first()
            
            if not client:
                return {}
            
            context = {
                'client_id': client.id,
                'name': client.name,
                'company': client.company,
                'industry': client.industry,
                'brand_voice': client.brand_voice,
                'target_audience': client.target_audience,
                'content_preferences': client.content_preferences or {},
                'instagram_username': client.instagram_username,
            }
            
            return context
        finally:
            db.close()
    
    def update_client_preference(self, key: str, value: Any):
        """Update a client preference"""
        db = SessionLocal()
        try:
            client = db.query(Client).filter(Client.id == self.client_id).first()
            
            if client:
                if not client.content_preferences:
                    client.content_preferences = {}
                
                client.content_preferences[key] = value
                client.updated_at = datetime.utcnow()
                db.commit()
                
                logger.info(f"Updated preference '{key}' for client {self.client_id}")
        finally:
            db.close()
    
    def clear_memories(self):
        """Clear all memories for this client"""
        self.chroma.clear_client_memories(self.client_id)
        logger.info(f"Cleared all memories for client {self.client_id}")
