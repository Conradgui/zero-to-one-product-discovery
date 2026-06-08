#!/usr/bin/env python3
"""Baseline Runner — direct bare-model conversations without Z2O skill context."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "benchmarks"))

from common_api import call_chat, get_provider


def run_task(task_path: str, output_path: str) -> None:
    task = json.loads(Path(task_path).read_text(encoding="utf-8"))

    provider = get_provider()
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not provider:
        output_file.write_text(
            json.dumps({"ok": False, "error": "No API key available"}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return

    messages: list[dict[str, str]] = []
    turns = []
    total_usage: dict[str, int] = {}
    total_start = time.time()

    user_turns = task["user_turns"]
    if task["baseline_mode"] == "single_turn_pressure":
        user_turns = [task.get("single_turn_baseline_prompt") or user_turns[0]]

    for index, user_message in enumerate(user_turns, start=1):
        messages.append({"role": "user", "content": user_message})
        turn_start = time.time()
        result = call_chat(
            messages,
            provider=provider,
            system_prompt="",
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
        "runner": "baseline",
        "provider": provider,
        "baseline_mode": task["baseline_mode"],
        "expected_turns": len(user_turns),
        "total_turns": len(turns),
        "ok": bool(turns) and all(turn["ok"] for turn in turns) and len(turns) == len(user_turns),
        "total_elapsed_seconds": round(total_elapsed, 2),
        "total_usage": total_usage,
        "turns": turns,
        "all_assistant_content": "\n\n".join(turn["assistant_response"] for turn in turns),
        "final_response": turns[-1]["assistant_response"] if turns else "",
        "task_snapshot": task,
    }

    output_file.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK baseline runner: {task['task_id']} -> {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_baseline.py <task.json> <output.json>")
        sys.exit(1)
    run_task(sys.argv[1], sys.argv[2])
