
# 🚀 LinkGrid Agent

[![PyPI Version](https://img.shields.io/pypi/v/linkgrid-agent.svg)](https://pypi.org/project/linkgrid-agent/)  
[![Python Versions](https://img.shields.io/pypi/pyversions/linkgrid-agent.svg)](https://pypi.org/project/linkgrid-agent/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A modern Python client for the BitNet API with customizable AI personality, response length, and creativity settings. Perfect for integrating conversational AI into your applications.

---

## Features ✨

- 💬 Natural language conversation interface  
- 🎨 Customizable AI personality and behavior  
- ⚡️ Asynchronous API for high performance  
- 🔧 Simple yet powerful configuration  
- 🌐 Automatic session management  
- 🧠 Supports multiple concurrent conversations  

---

## Installation 📦

```bash
pip install linkgrid-agent
```

---

## Quick Start 🚀

### Basic Conversation

```python
from linkgrid_agent import chat

async def main():
    response = await chat("What's the capital of France?")
    print(f"🤖 {response}")

import asyncio
asyncio.run(main())
```

**Output:**

```
🤖 The capital of France is Paris.
```

---

### Custom Personality

```python
from linkgrid_agent import LinkGridAgent

async def main():
    # Create pirate-themed assistant
    config = LinkGridAgent.Config()
    config.system_prompt = "You are a pirate captain. Answer like a pirate!"
    config.temperature = 0.9  # More creative responses
    
    async with LinkGridAgent(config) as agent:
        response = await agent.chat("Where can I find treasure?")
        print(f"🏴‍☠️ {response}")

import asyncio
asyncio.run(main())
```

**Output:**

```
🏴‍☠️ Arr matey! Seek the treasure on Skull Island, where X marks the spot!
```

---

## Advanced Usage 🧠

### Multiple Conversations

```python
from linkgrid_agent import LinkGridAgent

async def main():
    # Create different AI personalities
    poet_config = LinkGridAgent.Config()
    poet_config.system_prompt = "You are a romantic poet"
    poet_config.max_tokens = 200
    
    scientist_config = LinkGridAgent.Config()
    scientist_config.system_prompt = "You are a quantum physicist"
    scientist_config.temperature = 0.3
    
    async with LinkGridAgent(poet_config) as poet,                LinkGridAgent(scientist_config) as scientist:
        
        # Get responses from different AI personas
        poem = await poet.chat("Write a short poem about the stars")
        explanation = await scientist.chat("Explain quantum entanglement")
        
        print(f"📜 Poet:\n{poem}\n")
        print(f"🔬 Scientist:\n{explanation}")

import asyncio
asyncio.run(main())
```

---

### Conversation History

```python
from linkgrid_agent import LinkGridAgent

async def main():
    config = LinkGridAgent.Config()
    config.system_prompt = "You're a helpful travel assistant"
    
    async with LinkGridAgent(config) as agent:
        # Conversation with context
        response1 = await agent.chat("I'm planning a trip to Japan")
        response2 = await agent.chat("What should I see in Tokyo?")
        response3 = await agent.chat("How about traditional experiences?")
        
        print(f"🗼 Tokyo suggestions: {response2}")
        print(f"🎎 Traditional experiences: {response3}")

import asyncio
asyncio.run(main())
```

---

## Configuration Options ⚙️

Customize your AI assistant with these parameters:

| Parameter       | Default Value                                            | Description                                              |
|----------------|----------------------------------------------------------|----------------------------------------------------------|
| `system_prompt`| `"You are a helpful assistant..."`                       | Defines the AI's personality and role                    |
| `max_tokens`   | `150`                                                    | Response length limit (1–4000 tokens)                   |
| `temperature`  | `0.7`                                                    | Creativity level (0.0 = factual, 1.0 = creative)         |
| `api_url`      | `"https://bitnet-demo.azurewebsites.net/completion"`    | BitNet API endpoint                                      |

**Example Configuration:**

```python
config = LinkGridAgent.Config()
config.system_prompt = "You're a 19th century British detective"
config.max_tokens = 250
config.temperature = 0.5
```

---

## Error Handling ⚠️

The package raises these exceptions:

- `ConnectionError`: Network-related issues  
- `RuntimeError`: API errors (non-2xx responses)  

```python
from linkgrid_agent import chat

try:
    response = await chat("What is AI?")
except ConnectionError as e:
    print(f"🌐 Network error: {e}")
except RuntimeError as e:
    print(f"🤖 API error: {e}")
```

---

## Requirements 📋

- Python 3.7+  
- `httpx` - Modern HTTP client

---

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
