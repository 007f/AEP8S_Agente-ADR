"""Infraestrutura: Adapter para provedores de LLM (interface interna única: complete)."""
import asyncio
import os
import re
import httpx


class LLMError(Exception):
    pass


class _Base:
    needs_key = True

    def __init__(self, key: str, model: str):
        self.key, self.model = key, model

    async def complete(self, system: str, messages: list[dict]) -> str:
        if self.needs_key and not self.key: raise LLMError("Informe a chave de API.")
        for tent in range(5):
            try:
                async with httpx.AsyncClient(timeout=180) as c:
                    r = await c.post(self.url, headers=self.headers(), json=self.body(system, messages))
            except httpx.HTTPError as e:
                raise LLMError(f"Falha de rede ao chamar a API: {e}")
            if r.status_code in (500, 502, 503, 504) and tent < 3:  # sobrecarga temporária
                await asyncio.sleep((2, 5, 10)[tent])
                continue
            if r.status_code == 429 and tent < 3 and not re.search(r"quota|credit|billing", r.text, re.I):
                m = re.search(r"in (\d+(?:\.\d+)?)\s*s", r.text)  # limite por minuto: espera o tempo indicado
                await asyncio.sleep(min(float(m.group(1)) + 1 if m else 15, 60))
                continue
            break
        if r.status_code >= 400: raise LLMError(f"API retornou {r.status_code}: {r.text[:300]}")
        try:
            return self.parse(r.json())
        except (KeyError, IndexError, ValueError):
            raise LLMError("Resposta da API em formato inesperado.")


class AnthropicAdapter(_Base):
    url = "https://api.anthropic.com/v1/messages"
    def headers(self): return {"x-api-key": self.key, "anthropic-version": "2023-06-01"}
    def body(self, s, m): return {"model": self.model, "max_tokens": 8000, "system": s, "messages": m}
    def parse(self, j): return "".join(b.get("text", "") for b in j["content"])


# Provedores que falam o formato "chat completions" da OpenAI
OPENAI_COMPAT = {
    "openai": "https://api.openai.com/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/openai",
    "groq": "https://api.groq.com/openai/v1",
    "ollama": "http://localhost:11434/v1",
}


class OpenAICompatAdapter(_Base):
    def __init__(self, key, model, base):
        super().__init__(key, model)
        self.url = base.rstrip("/") + "/chat/completions"
        self.needs_key = "localhost" not in base  # Ollama local não usa chave
    def headers(self): return {"Authorization": f"Bearer {self.key}"} if self.key else {}
    def body(self, s, m):
        b = {"model": self.model, "messages": [{"role": "system", "content": s}] + m}
        if "groq.com" in self.url and "gpt-oss" in self.model: b["reasoning_effort"] = os.getenv("GROQ_REASONING", "low")  # menos tokens de raciocínio
        return b
    def parse(self, j): return j["choices"][0]["message"]["content"]


def make_adapter(provider: str, key: str, model: str) -> _Base:
    if provider == "anthropic": return AnthropicAdapter(key.strip(), model.strip())
    if provider in OPENAI_COMPAT: return OpenAICompatAdapter(key.strip(), model.strip(), OPENAI_COMPAT[provider])
    raise LLMError(f"Provedor desconhecido: {provider}")
