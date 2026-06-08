from typing import AsyncIterator, Optional

from backend.config import (
    LLM_CLAUDE_API_KEY,
    LLM_CLAUDE_MODEL,
    LLM_OPENAI_API_KEY,
    LLM_OPENAI_MODEL,
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)

FALLBACK_CHAIN = ["claude", "openai", "ollama"]

DISCLAIMER = (
    "\n\n---\n*This information is for educational purposes only and does not "
    "constitute medical advice. Always consult your pediatrician or a qualified "
    "healthcare provider regarding any concerns about your child's health.*"
)


class LLMRouter:
    def __init__(self):
        self._anthropic_client = None
        self._openai_client = None

    @property
    def anthropic(self):
        if self._anthropic_client is None and LLM_CLAUDE_API_KEY:
            try:
                from anthropic import AsyncAnthropic
                self._anthropic_client = AsyncAnthropic(api_key=LLM_CLAUDE_API_KEY)
            except Exception:
                self._anthropic_client = False
        return self._anthropic_client if self._anthropic_client is not False else None

    @property
    def openai(self):
        if self._openai_client is None and LLM_OPENAI_API_KEY:
            try:
                from openai import AsyncOpenAI
                self._openai_client = AsyncOpenAI(api_key=LLM_OPENAI_API_KEY)
            except Exception:
                self._openai_client = False
        return self._openai_client if self._openai_client is not False else None

    async def generate(self, system_prompt: str, user_message: str) -> str:
        providers = [LLM_PROVIDER] + [p for p in FALLBACK_CHAIN if p != LLM_PROVIDER]

        for provider in providers:
            try:
                if provider == "claude":
                    return await self._call_claude(system_prompt, user_message)
                elif provider == "openai":
                    return await self._call_openai(system_prompt, user_message)
                elif provider == "ollama":
                    return await self._call_ollama(system_prompt, user_message)
            except Exception:
                continue

        return "I'm sorry, all LLM providers are currently unavailable. Please check your configuration and try again."

    async def generate_stream(self, system_prompt: str, user_message: str) -> AsyncIterator[str]:
        providers = [LLM_PROVIDER] + [p for p in FALLBACK_CHAIN if p != LLM_PROVIDER]

        for provider in providers:
            try:
                if provider == "claude":
                    async for token in self._stream_claude(system_prompt, user_message):
                        yield token
                    return
                elif provider == "openai":
                    async for token in self._stream_openai(system_prompt, user_message):
                        yield token
                    return
                elif provider == "ollama":
                    async for token in self._stream_ollama(system_prompt, user_message):
                        yield token
                    return
            except Exception:
                continue

        yield "I'm sorry, all LLM providers are currently unavailable."

    async def _call_claude(self, system_prompt: str, user_message: str) -> str:
        client = self.anthropic
        if client is None:
            raise RuntimeError("Anthropic client not available")
        resp = await client.messages.create(
            model=LLM_CLAUDE_MODEL,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return resp.content[0].text if resp.content else ""

    async def _call_openai(self, system_prompt: str, user_message: str) -> str:
        client = self.openai
        if client is None:
            raise RuntimeError("OpenAI client not available")
        resp = await client.chat.completions.create(
            model=LLM_OPENAI_MODEL,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return resp.choices[0].message.content or ""

    async def _call_ollama(self, system_prompt: str, user_message: str) -> str:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "system": system_prompt,
                    "prompt": user_message,
                    "stream": False,
                },
            ) as resp:
                data = await resp.json()
                return data.get("response", "")

    async def _stream_claude(self, system_prompt: str, user_message: str) -> AsyncIterator[str]:
        client = self.anthropic
        if client is None:
            raise RuntimeError("Anthropic client not available")
        async with client.messages.stream(
            model=LLM_CLAUDE_MODEL,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def _stream_openai(self, system_prompt: str, user_message: str) -> AsyncIterator[str]:
        client = self.openai
        if client is None:
            raise RuntimeError("OpenAI client not available")
        stream = await client.chat.completions.create(
            model=LLM_OPENAI_MODEL,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def _stream_ollama(self, system_prompt: str, user_message: str) -> AsyncIterator[str]:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "system": system_prompt,
                    "prompt": user_message,
                    "stream": True,
                },
            ) as resp:
                async for line in resp.content:
                    import json
                    try:
                        data = json.loads(line)
                        if data.get("response"):
                            yield data["response"]
                    except json.JSONDecodeError:
                        continue


_llm_router_instance: Optional[LLMRouter] = None


def get_llm_router() -> LLMRouter:
    global _llm_router_instance
    if _llm_router_instance is None:
        _llm_router_instance = LLMRouter()
    return _llm_router_instance
