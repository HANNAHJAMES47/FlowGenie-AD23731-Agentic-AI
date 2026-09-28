from __future__ import annotations

"""Bridge module to preserve backwards-compatibility for imports from agents.event_agents."""

from agents.booking_agent import BookingMonitoringAgent
from agents.budget_agent import BudgetPlanningAgent
from agents.logger import AgentLogger, safe_int
from agents.ranking_agent import RecommendationAggregatorAgent
from agents.requirement_agent import RequirementAnalysisAgent
from agents.vendor_agent import VendorSearchAgent

__all__ = [
    "RequirementAnalysisAgent",
    "BudgetPlanningAgent",
    "VendorSearchAgent",
    "RecommendationAggregatorAgent",
    "BookingMonitoringAgent",
    "AgentLogger",
    "safe_int",
]
