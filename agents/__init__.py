from __future__ import annotations

from agents.booking_agent import BookingMonitoringAgent
from agents.budget_agent import BudgetPlanningAgent
from agents.logger import AgentLogger, safe_int
from agents.notification_agent import NotificationAgent
from agents.ranking_agent import RecommendationAggregatorAgent
from agents.requirement_agent import RequirementAnalysisAgent
from agents.sentinel_agent import SentinelWatchdog
from agents.vendor_agent import VendorSearchAgent

# Aliases for backward-compatibility
VenueAgent = VendorSearchAgent
CateringAgent = VendorSearchAgent
DecorAgent = VendorSearchAgent
PhotographyAgent = VendorSearchAgent
EntertainmentAgent = VendorSearchAgent
MakeupAgent = VendorSearchAgent
LogisticsAgent = VendorSearchAgent
RecommendationAgent = RecommendationAggregatorAgent
MonitoringAgent = BookingMonitoringAgent

__all__ = [
    "RequirementAnalysisAgent",
    "BudgetPlanningAgent",
    "VendorSearchAgent",
    "RecommendationAggregatorAgent",
    "BookingMonitoringAgent",
    "NotificationAgent",
    "SentinelWatchdog",
    "AgentLogger",
    "safe_int",
    "VenueAgent",
    "CateringAgent",
    "DecorAgent",
    "PhotographyAgent",
    "EntertainmentAgent",
    "MakeupAgent",
    "LogisticsAgent",
    "RecommendationAgent",
    "MonitoringAgent",
]
