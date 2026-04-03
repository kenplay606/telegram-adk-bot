"""
Base agent class for all AI agents
"""
from typing import Optional, Dict, Any
from loguru import logger
from backend.core.llm_client import llm_client
from backend.memory.memory_manager import MemoryManager


class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, client_id: int, agent_name: str):
        """
        Initialize base agent
        
        Args:
            client_id: Client ID this agent works for
            agent_name: Name of the agent
        """
        self.client_id = client_id
        self.agent_name = agent_name
        self.llm = llm_client
        self.memory = MemoryManager(client_id)
        
        logger.info(f"{agent_name} initialized for client {client_id}")
    
    async def generate_with_context(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        use_memory: bool = True,
        **kwargs
    ) -> str:
        """
        Generate text with client context and memory
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            use_memory: Whether to include relevant memories
            **kwargs: Additional LLM parameters
        
        Returns:
            Generated text
        """
        # Get client context
        context = self.memory.get_client_context()
        
        # Build enhanced system prompt
        enhanced_system = system_prompt or ""
        
        if context:
            enhanced_system += f"\n\nClient Context:"
            if context.get('company'):
                enhanced_system += f"\nCompany: {context['company']}"
            if context.get('industry'):
                enhanced_system += f"\nIndustry: {context['industry']}"
            if context.get('brand_voice'):
                enhanced_system += f"\nBrand Voice: {context['brand_voice']}"
            if context.get('target_audience'):
                enhanced_system += f"\nTarget Audience: {context['target_audience']}"
        
        # Add relevant memories if requested
        if use_memory:
            memories = self.memory.recall_similar(prompt, n_results=3)
            if memories:
                enhanced_system += "\n\nRelevant Past Interactions:"
                for mem in memories:
                    enhanced_system += f"\n- {mem['text'][:200]}"
        
        # Generate response
        response = await self.llm.generate(
            prompt=prompt,
            system_prompt=enhanced_system,
            **kwargs
        )
        
        # Store interaction in memory
        self.memory.add_interaction(
            interaction_type=f"{self.agent_name}_generation",
            content=f"Prompt: {prompt}\nResponse: {response}",
            metadata={'agent': self.agent_name}
        )
        
        return response
    
    async def generate_json_with_context(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate JSON output with context"""
        context = self.memory.get_client_context()
        
        enhanced_system = system_prompt or "You are a helpful assistant that responds with valid JSON."
        
        if context:
            enhanced_system += f"\n\nClient Context: {context}"
        
        return await self.llm.generate_json(
            prompt=prompt,
            system_prompt=enhanced_system,
            **kwargs
        )
