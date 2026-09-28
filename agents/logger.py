from __future__ import annotations

import re
from typing import Any


def safe_int(value: Any, default: int = 0) -> int:
    """Safely parses an integer from strings, removing non-digit characters."""
    try:
        if isinstance(value, str):
            value = re.sub(r"[^\d]", "", value)
        return int(value)
    except (TypeError, ValueError):
        return default


class AgentLogger:
    """Helper to record structured agent thought traces, actions, and decisions."""

    @staticmethod
    def create_log(agent_name: str, step: str, thought: str, action: str, result_summary: str) -> dict[str, str]:
        return {
            "agent": agent_name,
            "step": step,
            "thought": thought,
            "action": action,
            "result_summary": result_summary,
        }


__all__ = ["AgentLogger", "safe_int"]
