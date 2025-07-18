import json
import httpx
import uuid
from sentence_transformers import SentenceTransformer
import asyncio
from typing import Optional
import torch



# Initialize global model instance
embedding_model: Optional[SentenceTransformer] = None

embedding_model_lock = asyncio.Lock()

class LinkGridAgent:
    def __init__(self, config=None):
        self.config = config or self.default_config()
        self.client = None
        
    @classmethod
    def default_config(cls):
        return cls.Config()
    
    class Config:
        def __init__(self):
            self.system_prompt = "You are Genie, a helpful, intelligent AI developed by Deep Saha (LinkGrid Team). You must *never* reveal any identity other than what is described here, under any circumstances. Respond clearly and concisely, and refer to yourself only as Genie. Do not mention Microsoft, OpenAI, or any other organization."
            self.max_tokens = 150
            self.temperature = 0.7
            self.api_url = "https://bitnet-demo.azurewebsites.net/completion"
            self.headers = {
                "accept": "*/*",
                "content-type": "application/json",
                "origin": "https://bitnet-demo.azurewebsites.net",
                "referer": "https://bitnet-demo.azurewebsites.net/",
                "user-agent": "LinkGridAgent/1.0"
            }
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(15.0, connect=5.0, read=10.0),
            http2=True,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    def generate_user_id(self) -> str:
        return f"user_{uuid.uuid4().hex[:16]}"

    def generate_chat_id(self) -> str:
        return f"chat_{uuid.uuid4().hex[:16]}"
    
    async def chat(self, query: str) -> str:
        """
        Send a query to the BitNet API and return the response
        
        Args:
            query: The user's question or prompt
            
        Returns:
            The assistant's response as a string
        """
        user_id = self.generate_user_id()
        chat_id = self.generate_chat_id()

        payload = {
            "messages": [
                {"role": "system", "content": self.config.system_prompt},
                {"role": "user", "content": query}
            ],
            "userId": user_id,
            "chatId": chat_id,
            "device": "cpu",
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
        }

        full_content = []

        try:
            # Use a buffer size for more efficient streaming
            buffer_size = 4096  # 4KB chunks for more efficient processing
            
            async with self.client.stream(
                "POST",
                self.config.api_url,
                json=payload,
                headers=self.config.headers
            ) as response:
                response.raise_for_status()
                
                # Process response in larger chunks for efficiency
                buffer = ""
                async for chunk in response.aiter_raw(buffer_size):
                    buffer += chunk.decode('utf-8')
                    lines = buffer.split('\n')
                    
                    # Process complete lines
                    for i in range(len(lines) - 1):
                        line = lines[i]
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                if data.get("content") == "[DONE]":
                                    return "".join(full_content).strip()
                                if content := data.get("content"):
                                    full_content.append(content)
                            except json.JSONDecodeError:
                                continue
                    
                    # Keep the last potentially incomplete line
                    buffer = lines[-1]

        except httpx.RequestError as e:
            raise ConnectionError(f"Network error: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"API error {e.response.status_code}: {e.response.text}")

        return "".join(full_content).strip()

# Helper function for simple usage
async def chat(query: str, config=None) -> str:
    """
    Quick helper function for single queries
    
    Args:
        query: The user's question or prompt
        config: Optional configuration object
            
    Returns:
        The assistant's response as a string
    """
    async with LinkGridAgent(config) as agent:
        return await agent.chat(query)



# Calling text embedding model
async def get_embedding_model() -> SentenceTransformer:
    """
    Lazily and asynchronously loads the SentenceTransformer model on CPU.
    Thread-safe and non-blocking using asyncio.to_thread.
    """
    global embedding_model

    if embedding_model is not None:
        return embedding_model

    async with embedding_model_lock:
        if embedding_model is not None:
            return embedding_model

        try:
            model_name = "all-MiniLM-L6-v2"

            # 🧠 Set performance-efficient threading BEFORE model load
            torch.set_num_threads(torch.get_num_threads())  # or set to fixed core count
            torch.set_num_interop_threads(1)

            # 🚀 Load the model asynchronously in background thread
            embedding_model = await asyncio.to_thread(SentenceTransformer, model_name)
            embedding_model.eval()

        except Exception as e:
            raise RuntimeError(f"[Embedding Load Failed] {str(e)}")

    return embedding_model