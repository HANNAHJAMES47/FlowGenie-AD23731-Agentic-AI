"""Autonomous Background Sentinel Watchdog Agent for FlowGenie.

Monitors active vendor contract health in the background and autonomously
triggers self-healing replanning upon vendor cancellation or unresponsiveness.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any
from agents.booking_agent import ContingencyReplanner
from agents.ranking_agent import RankingAgent
from agents.vendor_agent import VendorSearchAgent
from memory.store import get_memory


class SentinelWatchdog:
    def __init__(self) -> None:
        self.memory = get_memory()
        self.ranking_agent = RankingAgent()
        self.contingency_agent = ContingencyReplanner()
        self.active_monitors: dict[str, bool] = {}

    def get_event_audit_log(self, event_id: str) -> list[dict[str, Any]]:
        """Retrieve all incident and recovery logs for a specific event."""
        return self.memory.get(f"sentinel_audit_{event_id}") or []

    def log_incident(
        self,
        event_id: str,
        incident_type: str,
        severity: str,
        message: str,
        action_taken: str,
    ) -> dict[str, Any]:
        """Record an autonomous sentinel event in memory."""
        logs = self.get_event_audit_log(event_id)
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "incident_type": incident_type,
            "severity": severity,  # INFO, WARNING, CRITICAL, RESOLVED
            "message": message,
            "action_taken": action_taken,
        }
        logs.append(entry)
        self.memory.set(f"sentinel_audit_{event_id}", logs)
        return entry

    async def auto_recover_vendor(
        self,
        event_id: str,
        category: str,
        reason: str = "Vendor cancellation detected by Sentinel Watchdog",
    ) -> dict[str, Any]:
        """Autonomously replaces a compromised vendor with the highest-ranked backup."""
        state_data = self.memory.get(f"event:{event_id}") or self.memory.get(f"event_state_{event_id}") or {}
        booking_data = state_data.get("booking_data", {})
        booked_vendors = list(booking_data.get("approved_vendors", state_data.get("booked_vendors", [])))
        requirements = state_data.get("requirements", {})
        budget_plan = state_data.get("budget_plan", {})

        # 1. Log critical failure detection
        self.log_incident(
            event_id=event_id,
            incident_type="VENDOR_ALERT",
            severity="CRITICAL",
            message=f"Supplier for '{category}' became unavailable: {reason}.",
            action_taken="Activated autonomous parallel search for verified backup suppliers.",
        )

        # 2. Discover backup replacements within budget slice
        budget_slice = float(budget_plan.get("category_allocations", {}).get(category, 50000.0))
        search_agent = VendorSearchAgent(category=category)
        discovered_backups = await search_agent.run(requirements, budget_slice)

        # 3. Rank backups using MCDA scoring
        recs, _ = self.ranking_agent.run({category: discovered_backups})
        ranked_backups = recs.get(category, [])

        if not ranked_backups:
            self.log_incident(
                event_id=event_id,
                incident_type="RECOVERY_FAILED",
                severity="WARNING",
                message=f"No replacement suppliers available for '{category}'.",
                action_taken="Escalated to human concierge desk.",
            )
            return {"status": "failed", "category": category}

        best_replacement = ranked_backups[0]

        # 4. Swap vendor in state
        updated_booked = []
        old_vendor_name = "Original Supplier"
        for v in booked_vendors:
            if v.get("category") == category:
                old_vendor_name = v.get("name", "Original Supplier")
                updated_booked.append(best_replacement)
            else:
                updated_booked.append(v)

        state_data["booked_vendors"] = updated_booked
        total_spend = sum(float(v.get("price", 0)) for v in updated_booked)
        total_budget = float(budget_plan.get("total_budget", 0))
        remaining = max(total_budget - total_spend, 0)

        if "booking_data" in state_data:
            state_data["booking_data"]["approved_vendors"] = updated_booked
            state_data["booking_data"]["total_spend"] = total_spend
            state_data["booking_data"]["budget_remaining"] = remaining

        if "booking_summary" in state_data:
            state_data["booking_summary"]["selected"] = updated_booked
            state_data["booking_summary"]["total_spend"] = total_spend
            state_data["booking_summary"]["budget_remaining"] = remaining

        self.memory.set(f"event:{event_id}", state_data)
        self.memory.set(f"event_state_{event_id}", state_data)
        self.memory.set("current_event", state_data)

        # 5. Log resolution
        self.log_incident(
            event_id=event_id,
            incident_type="AUTO_RECOVERY_SUCCESS",
            severity="RESOLVED",
            message=f"Successfully swapped '{old_vendor_name}' with top-ranked backup '{best_replacement.get('name')}'.",
            action_taken=f"Contract updated. New total spend: INR {total_spend:,.2f} (Savings/Remaining: INR {remaining:,.2f}).",
        )

        return {
            "status": "resolved",
            "category": category,
            "old_vendor": old_vendor_name,
            "new_vendor": best_replacement,
            "total_spend": total_spend,
            "budget_remaining": remaining,
        }

    def set_watchdog_active(self, event_id: str, active: bool) -> bool:
        """Enable or disable autonomous background health monitoring for an event."""
        self.active_monitors[event_id] = active
        self.log_incident(
            event_id=event_id,
            incident_type="WATCHDOG_STATUS",
            severity="INFO",
            message=f"Sentinel Auto-Pilot Watchdog {'ENABLED' if active else 'DISABLED'}.",
            action_taken="Background automated contract monitoring active." if active else "Monitoring paused.",
        )
        return active

    def is_watchdog_active(self, event_id: str) -> bool:
        """Check if autonomous monitoring is enabled for an event."""
        return self.active_monitors.get(event_id, True)


__all__ = ["SentinelWatchdog"]
