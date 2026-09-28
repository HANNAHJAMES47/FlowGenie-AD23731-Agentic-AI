from __future__ import annotations

from typing import Any
from agents.logger import AgentLogger
from memory.store import SharedMemory


class BudgetPlanningAgent:
    """2. Budget & Finance Strategist Agent: Allocates and validates category budgets."""

    def __init__(self, memory: SharedMemory | None = None):
        self.memory = memory or SharedMemory()
        self.agent_name = "Budget & Finance Strategist Agent"

    def _allocate(self, total_budget: int, event_type: str, guest_count: int, decor_style: str = "Modern") -> tuple[dict[str, float], dict[str, Any]]:
        event_key = event_type.lower()
        no_decor = decor_style.lower() in {"none", "no", "not required"}

        if event_key in {"birthday", "party"}:
            weights = {
                "venue": 0.22 if no_decor else 0.20,
                "catering": 0.38 if no_decor else 0.32,
                "decor": 0.00 if no_decor else 0.18,
                "photography": 0.18 if no_decor else 0.12,
                "entertainment": 0.18 if no_decor else 0.14,
                "others": 0.04,
            }
        elif event_key in {"corporate", "conference", "product launch"}:
            weights = {
                "venue": 0.34 if no_decor else 0.30,
                "catering": 0.26 if no_decor else 0.22,
                "decor": 0.00 if no_decor else 0.12,
                "photography": 0.18 if no_decor else 0.16,
                "entertainment": 0.12 if no_decor else 0.10,
                "others": 0.10,
            }
        else:  # Wedding, Anniversary, Engagement
            weights = {
                "venue": 0.34 if no_decor else 0.28,
                "catering": 0.32 if no_decor else 0.26,
                "decor": 0.00 if no_decor else 0.18,
                "photography": 0.16 if no_decor else 0.12,
                "entertainment": 0.10 if no_decor else 0.08,
                "makeup": 0.05 if no_decor else 0.05,
                "others": 0.03,
            }

        allocations = {cat: round(total_budget * w, 2) for cat, w in weights.items() if w > 0}
        catering_budget = allocations.get("catering", 0)
        per_plate_estimate = round(catering_budget / max(guest_count, 1), 2)

        feasibility = {
            "per_guest_spend": round(total_budget / max(guest_count, 1), 2),
            "estimated_per_plate_catering": per_plate_estimate,
            "feasibility_status": "Optimal" if per_plate_estimate >= 300 else "Tight Budget (Recommend value vendors)",
        }
        return allocations, feasibility

    def run(self, requirements: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
        total_budget = int(requirements.get("budget", 150000))
        event_type = requirements.get("event_type", "Wedding")
        guest_count = int(requirements.get("guest_count", 50))
        decor_style = requirements.get("preferences", {}).get("decor_style", "Modern")

        allocations, feasibility = self._allocate(total_budget, event_type, guest_count, decor_style)
        
        category_titles = {
            "venue": "Venue & Banquet",
            "catering": "Catering & Food",
            "decor": "Decor & Styling",
            "photography": "Photography & Video",
            "entertainment": "Entertainment & Music",
            "makeup": "Bridal & Party Makeup",
            "others": "Special & Miscellaneous",
        }

        custom_cat = requirements.get("custom_category") or requirements.get("preferences", {}).get("custom_category")
        if custom_cat and isinstance(custom_cat, dict):
            custom_key = custom_cat.get("key", "others")
            custom_title = custom_cat.get("title", "Custom Requirements")
            category_titles[custom_key] = custom_title
            if "others" in allocations and custom_key != "others":
                allocations[custom_key] = allocations.pop("others")
            elif custom_key not in allocations:
                allocations[custom_key] = round(total_budget * 0.05, 2)

        budget_plan = {
            "total_budget": total_budget,
            "event_type": event_type,
            "guest_count": guest_count,
            "category_allocations": allocations,
            "category_titles": category_titles,
            "feasibility": feasibility,
            "custom_category": custom_cat,
        }

        custom_thought = f" Custom slice allocated for {custom_cat['title']}." if custom_cat else ""
        log = AgentLogger.create_log(
            agent_name=self.agent_name,
            step="Budget Allocation & Feasibility Audit",
            thought=f"Audited total budget of INR {total_budget:,} for {guest_count} guests.{custom_thought}",
            action="Calculated weighted category allocations and verified catering per-plate viability.",
            result_summary=f"Allocated across {len(allocations)} categories ({', '.join(allocations.keys())}). Catering per plate: INR {feasibility['estimated_per_plate_catering']}.",
        )
        self.memory.set("budget_plan", budget_plan)
        return budget_plan, log


__all__ = ["BudgetPlanningAgent"]

