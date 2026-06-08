#!/usr/bin/env python3
"""Small OpenAI-compatible API client for Z2O benchmarks.

This file belongs to the benchmark harness, not the runtime skill. Baseline
runner imports only this client so it does not reuse the skill/test helpers.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


API_PROVIDERS = {
    "deepseek": {
        "env_key": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-v4-flash",
    },
    "mimo": {
        "env_key": "MIMO_API_KEY",
        "base_url": "https://token-plan-cn.xiaomimimo.com/v1",
        "default_model": "mimo-v2.5",
    },
}


def redact_secrets(text: str) -> str:
    redacted = text
    for config in API_PROVIDERS.values():
        key = os.environ.get(config["env_key"], "")
        if key:
            redacted = redacted.replace(key, "[REDACTED_API_KEY]")
    return redacted


def get_provider() -> str | None:
    preferred = os.environ.get("Z2O_BENCHMARK_PROVIDER", "deepseek").lower()
    provider_order = [preferred] + [name for name in API_PROVIDERS if name != preferred]
    for name in provider_order:
        config = API_PROVIDERS.get(name)
        if config and os.environ.get(config["env_key"]):
            return name
    return None


def call_chat(
    messages: list[dict[str, str]],
    *,
    provider: str,
    system_prompt: str = "",
    model: str | None = None,
    max_tokens: int = 2600,
    temperature: float = 0.25,
    timeout: int = 90,
) -> dict[str, Any]:
    config = API_PROVIDERS[provider]
    api_key = os.environ.get(config["env_key"], "")
    selected_model = model or os.environ.get("Z2O_BENCHMARK_MODEL") or config["default_model"]

    request_messages: list[dict[str, str]] = []
    if system_prompt:
        request_messages.append({"role": "system", "content": system_prompt})
    request_messages.extend(messages)

    payload = json.dumps(
        {
            "model": selected_model,
            "messages": request_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        f"{config['base_url']}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return {
                "ok": True,
                "content": body["choices"][0]["message"]["content"],
                "model": body.get("model", selected_model),
                "usage": body.get("usage", {}),
                "provider": provider,
            }
    except urllib.error.HTTPError as exc:
        error_body = ""
        try:
            error_body = exc.read().decode("utf-8")
        except Exception:
            pass
        return {
            "ok": False,
            "error": redact_secrets(f"HTTP {exc.code}: {error_body}"),
            "status_code": exc.code,
            "provider": provider,
            "model": selected_model,
        }
    except urllib.error.URLError as exc:
        return {
            "ok": False,
            "error": redact_secrets(f"URL error: {exc.reason}"),
            "provider": provider,
            "model": selected_model,
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": redact_secrets(str(exc)),
            "provider": provider,
            "model": selected_model,
        }
