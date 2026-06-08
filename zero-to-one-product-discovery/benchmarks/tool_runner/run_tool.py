#!/usr/bin/env python3
"""Tool Runner — run benchmark conversations with the Z2O skill rules loaded."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "benchmarks"))

from common_api import call_chat, get_provider


PROMPT_FILES = [
    "SKILL.md",
    "references/workflow.md",
    "child-skills/prd/ADAPTER.md",
    "child-skills/roadmap/ADAPTER.md",
    "child-skills/artifact-export/ADAPTER.md",
    "child-skills/execution-bridge/ADAPTER.md",
]


FULL_PROFILE_REFERENCES = [
    "SKILL.md",
    "references/workflow.md",
    "references/planning-artifacts.md",
    "references/artifact-adapters.md",
    "references/multi-agent-orchestration.md",
]


def _excerpt(path: Path, limit: int) -> str:
    text = path.read_text(encoding="utf-8")
    return text[:limit]


def _full_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_default_excerpts() -> list[str]:
    excerpts = []
    for relative in PROMPT_FILES:
        path = ROOT / relative
        limit = 12000 if relative == "SKILL.md" else 6000
        excerpts.append(f"\n\n## {relative}\n{_excerpt(path, limit)}")
    return excerpts


def _load_full_child_skill_context() -> list[str]:
    excerpts = []
    for relative in FULL_PROFILE_REFERENCES:
        path = ROOT / relative
        excerpts.append(f"\n\n## {relative}\n{_full_text(path)}")

    for path in sorted((ROOT / "child-skills").glob("*/ADAPTER.md")):
        relative = path.relative_to(ROOT)
        excerpts.append(f"\n\n## {relative}\n{_full_text(path)}")
    return excerpts


def load_tool_system_prompt(task: dict | None = None) -> str:
    task = task or {}
    profile = task.get("tool_context_profile", "default")
    if profile == "full_child_skill_activation":
        excerpts = _load_full_child_skill_context()
        profile_notice = (
            "Tool context profile: full_child_skill_activation.\n"
            "The following routing references and child-skill adapters are active execution "
            "contracts, not passive background reading. When the task requests PRD, Roadmap, "
            "Review/Auditor, or Context Handoff output, explicitly follow the relevant adapter "
            "contracts and return their visible contract fields. Simulate Controller, Producer, "
            "and Auditor roles in user-visible summaries only; do not reveal hidden reasoning.\n"
        )
    else:
        excerpts = _load_default_excerpts()
        profile_notice = "Tool context profile: default.\n"

    required = task.get("required_child_skills", [])
    task_instructions = task.get("tool_runner_instructions", "")
    required_text = f"Required child skills for this task: {', '.join(required)}.\n" if required else ""
    task_text = f"\nTask-specific Tool instructions:\n{task_instructions}\n" if task_instructions else ""

    return (
        "You are executing the zero-to-one-product-discovery skill as the Tool Runner.\n"
        + profile_notice
        + required_text
        + "Follow the local skill rules and adapter boundaries below. Treat them as the "
        "source of truth. Keep responses user-visible and do not expose hidden chain-of-thought.\n"
        "For benchmark evidence, be explicit about facts, assumptions, unknowns, risks, "
        "stage gates, readiness, not-ready statuses, dry-run boundaries, and the next "
        "highest-leverage action. Do not invent user research, external execution, files, "
        "issue URLs, or API results.\n"
        + task_text
        + "\n".join(excerpts)
    )


def run_task(task_path: str, output_path: str) -> None:
    task_file = Path(task_path)
    task = json.loads(task_file.read_text(encoding="utf-8"))

    provider = get_provider()
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not provider:
        output_file.write_text(
            json.dumps({"ok": False, "error": "No API key available"}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return

    system_prompt = load_tool_system_prompt(task)
    messages: list[dict[str, str]] = []
    turns = []
    total_usage: dict[str, int] = {}
    total_start = time.time()

    for index, user_message in enumerate(task["user_turns"], start=1):
        messages.append({"role": "user", "content": user_message})
        turn_start = time.time()
        result = call_chat(
            messages,
            provider=provider,
            system_prompt=system_prompt,
            max_tokens=task.get("max_tokens", 2600),
            timeout=task.get("timeout_seconds", 90),
        )
        elapsed = time.time() - turn_start

        usage = result.get("usage", {}) or {}
        for key, value in usage.items():
            if isinstance(value, int):
                total_usage[key] = total_usage.get(key, 0) + value

        assistant_response = result.get("content", "")
        turns.append(
            {
                "turn": index,
                "user_message": user_message,
                "assistant_response": assistant_response,
                "ok": result["ok"],
                "error": result.get("error"),
                "elapsed_seconds": round(elapsed, 2),
                "model": result.get("model"),
                "usage": usage,
            }
        )

        if not result["ok"]:
            break
        messages.append({"role": "assistant", "content": assistant_response})

    total_elapsed = time.time() - total_start
    output = {
        "task_id": task["task_id"],
        "task_name": task["task_name"],
        "runner": "tool",
        "provider": provider,
        "baseline_mode": task["baseline_mode"],
        "tool_context_profile": task.get("tool_context_profile", "default"),
        "required_child_skills": task.get("required_child_skills", []),
        "expected_turns": len(task["user_turns"]),
        "total_turns": len(turns),
        "ok": bool(turns) and all(turn["ok"] for turn in turns) and len(turns) == len(task["user_turns"]),
        "total_elapsed_seconds": round(total_elapsed, 2),
        "total_usage": total_usage,
        "turns": turns,
        "all_assistant_content": "\n\n".join(turn["assistant_response"] for turn in turns),
        "final_response": turns[-1]["assistant_response"] if turns else "",
        "task_snapshot": task,
    }

    output_file.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK tool runner: {task['task_id']} -> {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_tool.py <task.json> <output.json>")
        sys.exit(1)
    run_task(sys.argv[1], sys.argv[2])
