"""Shared helpers for Phase 4 real API usability tests.

These scripts intentionally validate behavior and evidence persistence, not
fine-grained model quality. Phase 5 benchmark scoring handles quality.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_ROOT = Path(
    "/Users/conrad/Desktop/项目面试包/zero-to-one-product-discovery/"
    "02_codex_新证据_按手册重做/04_phase_4_real_usability"
)
RAW_DIR = EVIDENCE_ROOT / "raw_outputs"
REPORT_DIR = EVIDENCE_ROOT / "reports"

API_PROVIDERS = {
    "deepseek": {
        "env_key": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com/v1",
        "models": [
            os.environ.get("DEEPSEEK_MODEL", ""),
            "deepseek-chat",
            "deepseek-v4-flash",
            "deepseek-v4-pro",
        ],
    },
    "mimo": {
        "env_key": "MIMO_API_KEY",
        "base_url": "https://token-plan-cn.xiaomimimo.com/v1",
        "models": [
            os.environ.get("MIMO_MODEL", ""),
            "mimo-v2.5",
            "mimo-v2.5-pro",
        ],
    },
}

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


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


def redact(text: str) -> str:
    redacted = text
    for config in API_PROVIDERS.values():
        key = os.environ.get(config["env_key"], "")
        if key:
            redacted = redacted.replace(key, "[REDACTED_API_KEY]")
    return redacted


def available_provider(preferred: str = "deepseek") -> str:
    preferred_key = API_PROVIDERS[preferred]["env_key"]
    if os.environ.get(preferred_key):
        return preferred
    for name, config in API_PROVIDERS.items():
        if os.environ.get(config["env_key"]):
            return name
    raise RuntimeError("No DEEPSEEK_API_KEY or MIMO_API_KEY is available in environment")


def provider_models(provider: str) -> list[str]:
    seen: set[str] = set()
    models = []
    for model in API_PROVIDERS[provider]["models"]:
        if model and model not in seen:
            models.append(model)
            seen.add(model)
    return models


def call_llm(
    messages: list[dict[str, str]],
    provider: str,
    max_tokens: int = 1600,
    timeout: int = 60,
) -> dict[str, Any]:
    config = API_PROVIDERS[provider]
    api_key = os.environ.get(config["env_key"], "")
    url = f"{config['base_url']}/chat/completions"
    last_error: dict[str, Any] | None = None

    full_messages = [{"role": "system", "content": SKILL_SYSTEM_PROMPT}] + messages
    for model in provider_models(provider):
        payload = json.dumps(
            {
                "model": model,
                "messages": full_messages,
                "max_tokens": max_tokens,
                "temperature": 0.3,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            url,
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
                content = body["choices"][0]["message"]["content"]
                return {
                    "ok": True,
                    "content": content,
                    "model": body.get("model", model),
                    "usage": body.get("usage", {}),
                    "provider": provider,
                }
        except urllib.error.HTTPError as exc:
            error_body = ""
            try:
                error_body = exc.read().decode("utf-8")
            except Exception:
                pass
            last_error = {
                "ok": False,
                "provider": provider,
                "model": model,
                "status_code": exc.code,
                "error": redact(f"HTTP {exc.code}: {error_body}"),
            }
            if exc.code in {400, 404}:
                continue
            return last_error
        except urllib.error.URLError as exc:
            return {
                "ok": False,
                "provider": provider,
                "model": model,
                "error": redact(f"URL error: {exc.reason}"),
            }
        except Exception as exc:
            return {
                "ok": False,
                "provider": provider,
                "model": model,
                "error": redact(str(exc)),
            }

    return last_error or {"ok": False, "provider": provider, "error": "No model attempted"}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_scenario(
    path_id: str,
    name: str,
    turns: list[str],
    timeout_seconds: int,
    scenario_type: str,
    min_chars: int = 50,
    max_tokens: int = 1600,
) -> int:
    ensure_dirs()
    provider = available_provider("deepseek")
    started = time.time()
    messages: list[dict[str, str]] = []
    turn_results: list[dict[str, Any]] = []
    ok = True
    failed_stage = ""
    error_summary = ""

    for index, turn in enumerate(turns, start=1):
        messages.append({"role": "user", "content": turn})
        result = call_llm(messages, provider=provider, max_tokens=max_tokens, timeout=timeout_seconds)
        turn_elapsed = time.time() - started
        if not result.get("ok"):
            ok = False
            failed_stage = f"turn_{index}_api_call"
            error_summary = str(result.get("error", "unknown error"))[:500]
            turn_results.append({"turn": index, "input": turn, "response": result, "elapsed": turn_elapsed})
            break
        content = result.get("content", "")
        messages.append({"role": "assistant", "content": content})
        turn_results.append({"turn": index, "input": turn, "response": result, "elapsed": turn_elapsed})
        if len(content.strip()) < min_chars:
            ok = False
            failed_stage = f"turn_{index}_nonempty_output"
            error_summary = f"Output shorter than {min_chars} characters"
            break
        if turn_elapsed > timeout_seconds:
            ok = False
            failed_stage = f"turn_{index}_timeout"
            error_summary = f"Elapsed {turn_elapsed:.1f}s exceeded {timeout_seconds}s"
            break

    elapsed = time.time() - started
    raw = {
        "path_id": path_id,
        "path_name": name,
        "scenario_type": scenario_type,
        "provider": provider,
        "turns": turn_results,
        "messages": messages,
    }
    result_report = {
        "path_id": path_id,
        "path_name": name,
        "scenario_type": scenario_type,
        "ok": ok,
        "provider": provider,
        "model": next((r.get("response", {}).get("model") for r in turn_results if r.get("response", {}).get("model")), None),
        "elapsed_seconds": round(elapsed, 2),
        "turn_count": len(turn_results),
        "message_count": len(messages),
        "raw_output": str(RAW_DIR / f"{path_id}.json"),
        "failed_stage": failed_stage or None,
        "error_summary": error_summary or None,
    }
    if path_id == "P0_006":
        result_report["phase3_guard_evidence"] = (
            "03_phase_3_quality_tests/PHASE_3_测试结果说明.md"
        )

    write_json(RAW_DIR / f"{path_id}.json", raw)
    write_json(REPORT_DIR / f"{path_id}_result.json", result_report)

    if ok:
        print(f"✅ {path_id} {name} — 可用（耗时 {elapsed:.1f} 秒）")
        return 0
    print(f"❌ {path_id} {name} — 失败（阶段：{failed_stage} / 原因：{error_summary}）")
    return 1


if __name__ == "__main__":
    print("This module is shared by usability scripts.", file=sys.stderr)
    raise SystemExit(2)
