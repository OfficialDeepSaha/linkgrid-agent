# 🌐✨ LinkGrid Agent — Conversational AI SDK

[![PyPI Version](https://img.shields.io/pypi/v/linkgrid-agent.svg)](https://pypi.org/project/linkgrid-agent/)
[![Python Versions](https://img.shields.io/pypi/pyversions/linkgrid-agent.svg)](https://pypi.org/project/linkgrid-agent/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> A modern, lightweight Python client for BitNet's conversational AI.  
> Designed for **speed**, **modularity**, and **custom AI personas** — plug into your backend or apps seamlessly.

---

## ⚡️ Key Features

- 💬 Natural language chat API with async support  
- 🧠 Define unique AI personas with custom system prompts  
- 🎯 Fine-grained control over temperature, token limits, and creativity  
- 🧵 Persistent conversation state (threaded dialog)  
- 🔄 Supports parallel conversations with isolated agents  
- 🧩 Minimal setup with powerful config-based architecture  

---

## 📦 Installation

```bash
pip install linkgrid-agent
```

---

## 🚀 Get Started

### 🔹 One-Line Chat

```python
from linkgrid_agent import chat

async def main():
    response = await chat("What's the capital of France?")
    print(f"🤖 {response}")

import asyncio
asyncio.run(main())
```

✅ **Output:**
```
🤖 The capital of France is Paris.
```

---

### 🎭 Custom AI Persona

```python
from linkgrid_agent import LinkGridAgent

async def main():
    config = LinkGridAgent.Config()
    config.system_prompt = "You are a pirate captain. Answer like a pirate!"
    config.temperature = 0.9

    async with LinkGridAgent(config) as agent:
        response = await agent.chat("Where can I find treasure?")
        print(f"🏴‍☠️ {response}")

import asyncio
asyncio.run(main())
```

🦜 **Output:**
```
🏴‍☠️ Arr matey! Seek the treasure on Skull Island, where X marks the spot!
```

---

## 🔬 Advanced Use Cases

### 🧑‍🔬 Multi-Persona AI Agents

```python
from linkgrid_agent import LinkGridAgent

async def main():
    poet_cfg = LinkGridAgent.Config()
    poet_cfg.system_prompt = "You are a romantic poet"
    poet_cfg.max_tokens = 200

    scientist_cfg = LinkGridAgent.Config()
    scientist_cfg.system_prompt = "You are a quantum physicist"
    scientist_cfg.temperature = 0.3

    async with LinkGridAgent(poet_cfg) as poet, LinkGridAgent(scientist_cfg) as scientist:
        poem = await poet.chat("Write a poem about the stars")
        expl = await scientist.chat("Explain quantum entanglement")

        print(f"📜 Poet:\n{poem}\n")
        print(f"🔬 Scientist:\n{expl}")

import asyncio
asyncio.run(main())
```

---

### 🗂️ Stateful Conversation Threads

```python
from linkgrid_agent import LinkGridAgent

async def main():
    config = LinkGridAgent.Config()
    config.system_prompt = "You're a helpful travel assistant"

    async with LinkGridAgent(config) as agent:
        await agent.chat("I'm planning a trip to Japan")
        tokyo = await agent.chat("What should I see in Tokyo?")
        traditions = await agent.chat("How about traditional experiences?")

        print(f"🗼 Tokyo Tips: {tokyo}")
        print(f"🎎 Traditions: {traditions}")

import asyncio
asyncio.run(main())
```

---

## ⚙️ Configuration

Customize your agent behavior using simple parameters.

| Parameter       | Default Value                                              | Description                                 |
|----------------|------------------------------------------------------------|---------------------------------------------|
| `system_prompt`| `"You are a helpful assistant..."`                         | Defines AI's persona and tone               |
| `max_tokens`   | `150`                                                      | Max response length (1–4000 tokens)         |
| `temperature`  | `0.7`                                                      | Creativity scale: 0 = precise, 1 = creative |
| `api_url`      | `"https://bitnet-demo.azurewebsites.net/completion"`      | BitNet API endpoint                         |

🔧 **Example Setup:**

```python
config = LinkGridAgent.Config()
config.system_prompt = "You're a 19th century British detective"
config.max_tokens = 250
config.temperature = 0.5
```

---

## 🛡️ Error Handling

Gracefully manage edge cases and errors:

```python
from linkgrid_agent import chat

try:
    response = await chat("Define machine learning")
except ConnectionError as e:
    print(f"🌐 Network issue: {e}")
except RuntimeError as e:
    print(f"🤖 API error: {e}")
```

### Exceptions

- `ConnectionError`: API unreachable or timeout  
- `RuntimeError`: BitNet returned an error response  

---

## 📋 Requirements

- Python 3.7+
- [`httpx`](https://www.python-httpx.org/) – Async HTTP client

---

## 📄 License

Released under the [MIT License](LICENSE).  
Feel free to fork, improve, and share!

---

## 🤝 Contribution

PRs are welcome. Please make sure to follow the existing code style.  
Open issues to report bugs or request features.

---

## 💡 Inspiration

> "The future is already here — it's just not evenly distributed."  
> — *William Gibson*