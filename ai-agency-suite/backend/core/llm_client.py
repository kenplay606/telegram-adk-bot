"""
LLM Client - Handles AI model interactions
SECURITY: API keys are loaded from environment variables only
"""
import os
from typing import Optional, Dict, Any, List
from loguru import logger
import httpx
from backend.config import settings


class LLMClient:
    """Client for interacting with LLM models (Ollama or OpenRouter)"""
    
    def __init__(self, use_cloud: bool = False):
        """
        Initialize LLM client
        
        Args:
            use_cloud: If True, use OpenRouter API (requires OPENROUTER_API_KEY in env)
                      If False, use local Ollama (default)
        """
        self.use_cloud = use_cloud
        
        if use_cloud:
            if not settings.OPENROUTER_API_KEY:
                logger.warning("OPENROUTER_API_KEY not set, falling back to Ollama")
                self.use_cloud = False
            else:
                self.openrouter_api_key = settings.OPENROUTER_API_KEY
                self.openrouter_model = settings.OPENROUTER_MODEL
                logger.info(f"LLM Client initialized with OpenRouter: {self.openrouter_model}")
        
        if not self.use_cloud:
            self.ollama_host = settings.OLLAMA_HOST
            self.ollama_model = settings.OLLAMA_MODEL
            logger.info(f"LLM Client initialized with Ollama: {self.ollama_model}")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        Generate text using the configured LLM
        
        Args:
            prompt: User prompt
            system_prompt: System instructions (optional)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional model-specific parameters
        
        Returns:
            Generated text
        """
        if self.use_cloud:
            return await self._generate_openrouter(prompt, system_prompt, temperature, max_tokens, **kwargs)
        else:
            return await self._generate_ollama(prompt, system_prompt, temperature, max_tokens, **kwargs)
    
    async def _generate_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate text using Ollama"""
        try:
            async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT) as client:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                payload = {
                    "model": self.ollama_model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    }
                }
                
                response = await client.post(
                    f"{self.ollama_host}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get("message", {}).get("content", "")
        
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise
    
    async def _generate_openrouter(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate text using OpenRouter API"""
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                headers = {
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "AI Agency Suite"
                }
                
                payload = {
                    "model": self.openrouter_model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                
                result = response.json()
                return result["choices"][0]["message"]["content"]
        
        except Exception as e:
            logger.error(f"OpenRouter generation error: {e}")
            raise
    
    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate JSON output
        
        Args:
            prompt: User prompt (should request JSON format)
            system_prompt: System instructions
            **kwargs: Additional parameters
        
        Returns:
            Parsed JSON dictionary
        """
        import json
        
        if not system_prompt:
            system_prompt = "You are a helpful assistant that always responds with valid JSON."
        else:
            system_prompt += "\nAlways respond with valid JSON."
        
        response = await self.generate(prompt, system_prompt, **kwargs)
        
        # Try to extract JSON from response
        try:
            # Remove markdown code blocks if present
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response}")
            raise
    
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ):
        """
        Generate text with streaming (yields chunks)
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            **kwargs: Additional parameters
        
        Yields:
            Text chunks as they're generated
        """
        if self.use_groq:
            # Groq streaming
            from groq import AsyncGroq
            client = AsyncGroq(api_key=self.groq_api_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            stream = await client.chat.completions.create(
                model=self.groq_model,
                messages=messages,
                stream=True,
                **kwargs
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        else:
            # Ollama streaming
            async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT) as client:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                payload = {
                    "model": self.ollama_model,
                    "messages": messages,
                    "stream": True,
                }
                
                async with client.stream(
                    "POST",
                    f"{self.ollama_host}/api/chat",
                    json=payload
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                yield data["message"]["content"]


# Global LLM client instance
# Temporarily using Ollama due to OpenRouter endpoint issues
llm_client = LLMClient(use_cloud=False)
