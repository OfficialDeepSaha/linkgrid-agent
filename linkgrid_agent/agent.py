import json
import httpx
import uuid
from sentence_transformers import SentenceTransformer
import asyncio


# Initialize global model instance
embedding_model = None

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
            timeout=httpx.Timeout(25.0, connect=10.0),
            http2=True
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
            async with self.client.stream(
                "POST",
                self.config.api_url,
                json=payload,
                headers=self.config.headers
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            if data.get("content") == "[DONE]":
                                break
                            if content := data.get("content"):
                                full_content.append(content)
                        except json.JSONDecodeError:
                            continue

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
async def get_embedding_model():
    """
    Asynchronously and thread-safely initializes and returns the sentence-transformers model.
    """
    global embedding_model

    if embedding_model is None:
        async with embedding_model_lock:
            if embedding_model is None:  # double-checked locking
                model_name = 'all-MiniLM-L6-v2'
                device = 'cpu'
                try:
                    embedding_model = await asyncio.to_thread(
                        SentenceTransformer, model_name, device=device
                    )
                except Exception as e:
                    raise RuntimeError(f"Failed to load embedding model: {str(e)}")
    
    return embedding_model
