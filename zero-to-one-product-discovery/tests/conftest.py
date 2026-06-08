"""conftest.py — 共享测试工具和 fixture。

本文件提供 unit 和 integration 测试共用的工具函数。
"""

from __future__ import annotations

import json
import os
import tempfile
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

# ── API 配置 ──
API_PROVIDERS = {
    "deepseek": {
        "env_key": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com/v1",
        "models": ["deepseek-v4-flash", "deepseek-v4-pro"],
        "default_model": "deepseek-v4-flash",
    },
    "mimo": {
        "env_key": "MIMO_API_KEY",
        "base_url": "https://token-plan-cn.xiaomimimo.com/v1",
        "models": ["mimo-v2.5-pro", "mimo-v2.5"],
        "default_model": "mimo-v2.5",
    },
}


def _redact_secrets(text: str) -> str:
    """Remove configured API keys from diagnostic text before returning it."""
    redacted = text
    for config in API_PROVIDERS.values():
        key = os.environ.get(config["env_key"], "")
        if key:
            redacted = redacted.replace(key, "[REDACTED_API_KEY]")
    return redacted


def has_api_key(provider: str = "deepseek") -> bool:
    """检查指定 provider 的 API Key 是否存在。"""
    config = API_PROVIDERS.get(provider, {})
    env_key = config.get("env_key", "")
    return bool(os.environ.get(env_key))


def get_available_provider() -> str | None:
    """返回第一个可用的 provider 名称，无可用时返回 None。"""
    for name in API_PROVIDERS:
        if has_api_key(name):
            return name
    return None


def call_llm(
    prompt: str,
    system_prompt: str = "",
    provider: str = "deepseek",
    model: str | None = None,
    max_tokens: int = 2000,
    timeout: int = 60,
) -> dict[str, Any]:
    """调用 LLM API（OpenAI 兼容协议），返回响应 dict。

    Returns:
        {"ok": True, "content": "...", "model": "...", "usage": {...}}
        或 {"ok": False, "error": "...", "status_code": ...}
    """
    config = API_PROVIDERS[provider]
    api_key = os.environ.get(config["env_key"], "")
    base_url = config["base_url"]
    model = model or config["default_model"]

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }).encode("utf-8")

    url = f"{base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            content = body["choices"][0]["message"]["content"]
            return {
                "ok": True,
                "content": content,
                "model": body.get("model", model),
                "usage": body.get("usage", {}),
            }
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8")
        except Exception:
            pass
        return {"ok": False, "error": _redact_secrets(f"HTTP {e.code}: {error_body}"), "status_code": e.code}
    except urllib.error.URLError as e:
        return {"ok": False, "error": _redact_secrets(f"URL error: {e.reason}")}
    except Exception as e:
        return {"ok": False, "error": _redact_secrets(str(e))}


# ── Skill 测试用 system prompt ──
SKILL_SYSTEM_PROMPT = """You are a product discovery assistant.
You have access to a skill called zero-to-one-product-discovery.
When the user has an early-stage product idea without a complete product or runnable MVP,
you should use this skill to orchestrate early product discovery.

Core rules:
- Default to Diagnostic Start for vague ideas.
- Ask one highest-leverage question per turn.
- Do not produce final PRD, Roadmap, or Implementation Plan before grounding.
- Separate facts, assumptions, risks, and unknowns.
- Do not ask mature-product questions upfront (target user, MVP, tech stack, business model)
before generating candidate interpretations.

When the user provides materials, identify contradictions and gaps.
When the user demands full artifacts too early, downgrade to outline or decision surface."""


class Conversation:
    """多轮对话管理器 — 维护上下文，支持循环调用。"""

    def __init__(self, provider: str = "deepseek", model: str | None = None,
                 system_prompt: str = SKILL_SYSTEM_PROMPT):
        self.provider = provider
        self.model = model
        self.system_prompt = system_prompt
        self.messages: list[dict[str, str]] = []

    def send(self, user_message: str, max_tokens: int = 2000, timeout: int = 60) -> dict[str, Any]:
        """发送一条用户消息，返回 LLM 响应，自动维护上下文。"""
        self.messages.append({"role": "user", "content": user_message})
        result = call_llm_with_messages(
            messages=self.messages,
            system_prompt=self.system_prompt,
            provider=self.provider,
            model=self.model,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        if result["ok"]:
            self.messages.append({"role": "assistant", "content": result["content"]})
        return result

    def get_history(self) -> list[dict[str, str]]:
        """返回完整对话历史。"""
        return list(self.messages)


def call_llm_with_messages(
    messages: list[dict[str, str]],
    system_prompt: str = "",
    provider: str = "deepseek",
    model: str | None = None,
    max_tokens: int = 2000,
    timeout: int = 60,
) -> dict[str, Any]:
    """带完整 messages 数组的 LLM 调用（用于多轮对话）。"""
    config = API_PROVIDERS[provider]
    api_key = os.environ.get(config["env_key"], "")
    base_url = config["base_url"]
    model = model or config["default_model"]

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    payload = json.dumps({
        "model": model,
        "messages": full_messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }).encode("utf-8")

    url = f"{base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            content = body["choices"][0]["message"]["content"]
            return {
                "ok": True,
                "content": content,
                "model": body.get("model", model),
                "usage": body.get("usage", {}),
            }
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8")
        except Exception:
            pass
        return {"ok": False, "error": _redact_secrets(f"HTTP {e.code}: {error_body}"), "status_code": e.code}
    except urllib.error.URLError as e:
        return {"ok": False, "error": _redact_secrets(f"URL error: {e.reason}")}
    except Exception as e:
        return {"ok": False, "error": _redact_secrets(str(e))}
