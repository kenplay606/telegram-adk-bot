"""
ChromaDB client for vector memory storage
Each client has their own collection for isolated memory
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from loguru import logger
from backend.config import settings


class ChromaClient:
    """Client for managing ChromaDB vector storage"""
    
    def __init__(self):
        """Initialize ChromaDB client"""
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        logger.info(f"ChromaDB initialized at {settings.CHROMA_PERSIST_DIR}")
    
    def get_collection(self, client_id: int):
        """Get or create collection for a specific client"""
        collection_name = f"client_{client_id}_memory"
        
        try:
            collection = self.client.get_collection(name=collection_name)
        except Exception:
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"client_id": client_id}
            )
            logger.info(f"Created new collection: {collection_name}")
        
        return collection
    
    def add_memory(
        self,
        client_id: int,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        memory_id: Optional[str] = None
    ):
        """Add a memory to client's collection"""
        collection = self.get_collection(client_id)
        
        if not memory_id:
            import uuid
            memory_id = str(uuid.uuid4())
        
        if not metadata:
            metadata = {}
        
        collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[memory_id]
        )
        
        logger.debug(f"Added memory {memory_id} for client {client_id}")
        return memory_id
    
    def search_memories(
        self,
        client_id: int,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search memories for a client"""
        collection = self.get_collection(client_id)
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_metadata
        )
        
        memories = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                memories.append({
                    'id': results['ids'][0][i],
                    'text': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results.get('distances') else None
                })
        
        return memories
    
    def get_memory(self, client_id: int, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific memory by ID"""
        collection = self.get_collection(client_id)
        
        try:
            result = collection.get(ids=[memory_id])
            if result['documents']:
                return {
                    'id': memory_id,
                    'text': result['documents'][0],
                    'metadata': result['metadatas'][0] if result['metadatas'] else {}
                }
        except Exception as e:
            logger.error(f"Error getting memory {memory_id}: {e}")
        
        return None
    
    def update_memory(
        self,
        client_id: int,
        memory_id: str,
        text: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Update an existing memory"""
        collection = self.get_collection(client_id)
        
        update_data = {'ids': [memory_id]}
        if text:
            update_data['documents'] = [text]
        if metadata:
            update_data['metadatas'] = [metadata]
        
        collection.update(**update_data)
        logger.debug(f"Updated memory {memory_id} for client {client_id}")
    
    def delete_memory(self, client_id: int, memory_id: str):
        """Delete a memory"""
        collection = self.get_collection(client_id)
        collection.delete(ids=[memory_id])
        logger.debug(f"Deleted memory {memory_id} for client {client_id}")
    
    def get_all_memories(
        self,
        client_id: int,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all memories for a client"""
        collection = self.get_collection(client_id)
        
        result = collection.get(limit=limit)
        
        memories = []
        if result['documents']:
            for i, doc in enumerate(result['documents']):
                memories.append({
                    'id': result['ids'][i],
                    'text': doc,
                    'metadata': result['metadatas'][i] if result['metadatas'] else {}
                })
        
        return memories
    
    def clear_client_memories(self, client_id: int):
        """Clear all memories for a client"""
        collection_name = f"client_{client_id}_memory"
        try:
            self.client.delete_collection(name=collection_name)
            logger.info(f"Cleared all memories for client {client_id}")
        except Exception as e:
            logger.error(f"Error clearing memories for client {client_id}: {e}")


# Global ChromaDB client instance
chroma_client = ChromaClient()
