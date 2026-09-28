from __future__ import annotations

import asyncio
import uuid
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from agents.event_agents import (
    AgentLogger,
    BookingMonitoringAgent,
    BudgetPlanningAgent,
    RecommendationAggregatorAgent,
    RequirementAnalysisAgent,
    VendorSearchAgent,
)
from memory.store import memory


CATEGORY_ORDER = [
    "venue",
    "catering",
    "decor",
    "photography",
    "entertainment",
    "makeup",
    "others",
]


class EventState(TypedDict, total=False):
    prompt: str
    requirements: dict[str, Any]
    budget_plan: dict[str, Any]
    vendor_results: dict[str, Any]
    recommendations: dict[str, Any]
    agent_logs: list[dict[str, str]]
    approved: bool
    approval_decision: str
    event_id: str
    booking_data: dict[str, Any]
    monitoring_data: dict[str, Any]


class EventWorkflowEngine:
    """Orchestrates the 5-Agent Event Planning Workflow using LangGraph."""

    def __init__(self) -> None:
        self.requirements_agent = RequirementAnalysisAgent(memory)
        self.budget_agent = BudgetPlanningAgent(memory)
        self.aggregator_agent = RecommendationAggregatorAgent(memory)
        self.booking_monitor_agent = BookingMonitoringAgent(memory)
        self.graph = self._build_graph()

    def _build_graph(self):
        def analyze(state: EventState) -> EventState:
            reqs, log = self.requirements_agent.run(state.get("prompt", ""))
            state["requirements"] = reqs
            state.setdefault("agent_logs", []).append(log)
            return state

        def plan_budget(state: EventState) -> EventState:
            b_plan, log = self.budget_agent.run(state["requirements"])
            state["budget_plan"] = b_plan
            state.setdefault("agent_logs", []).append(log)
            return state

        async def vendor_search(state: EventState) -> EventState:
            budget_map = state["budget_plan"].get("category_allocations", {})
            categories = [c for c in CATEGORY_ORDER if c in budget_map] + [c for c in budget_map if c not in CATEGORY_ORDER]

            async def worker(category: str):
                agent = VendorSearchAgent(category=category, memory=memory)
                return await agent.run(state["requirements"], budget_map[category])

            results = await asyncio.gather(*(worker(category) for category in categories))
            state["vendor_results"] = {category: result for category, result in zip(categories, results)}
            
            search_log = AgentLogger.create_log(
                agent_name="Autonomous Vendor Discovery Agents (Parallel)",
                step="Parallel Category Search",
                thought=f"Initiated concurrent asynchronous search for {len(categories)} categories across venues, caterers, decorators, and entertainment.",
                action=f"Queried local verified catalogs and web search for {len(categories)} categories simultaneously.",
                result_summary=f"Retrieved candidate vendors for: {', '.join(categories)}.",
            )
            state.setdefault("agent_logs", []).append(search_log)
            return state

        def aggregate(state: EventState) -> EventState:
            recommendations, log = self.aggregator_agent.run(state["vendor_results"])
            state["recommendations"] = recommendations
            state.setdefault("agent_logs", []).append(log)
            return state

        def approval_gate(state: EventState) -> str:
            if state.get("approved"):
                return "book"
            return "end"

        def book(state: EventState) -> EventState:
            approved_vendors = []
            for vendors in state.get("recommendations", {}).values():
                if vendors:
                    approved_vendors.append(vendors[0])
            booking_data, log = self.booking_monitor_agent.run_booking(
                event_id=state.get("event_id", f"evt_{uuid.uuid4().hex[:8]}"),
                approved_vendors=approved_vendors,
                requirements=state.get("requirements"),
                budget_plan=state.get("budget_plan"),
            )
            state["booking_data"] = booking_data
            state.setdefault("agent_logs", []).append(log)
            return state

        def monitor(state: EventState) -> EventState:
            state["monitoring_data"] = self.booking_monitor_agent.run_monitoring(
                state.get("event_id", "evt_default"),
                state.get("booking_data", {}),
            )
            return state

        workflow = StateGraph(EventState)
        workflow.add_node("analyze", analyze)
        workflow.add_node("plan_budget", plan_budget)
        workflow.add_node("vendor_search", vendor_search)
        workflow.add_node("aggregate", aggregate)
        workflow.add_node("book", book)
        workflow.add_node("monitor", monitor)

        workflow.add_edge(START, "analyze")
        workflow.add_edge("analyze", "plan_budget")
        workflow.add_edge("plan_budget", "vendor_search")
        workflow.add_edge("vendor_search", "aggregate")
        workflow.add_conditional_edges("aggregate", approval_gate, {"book": "book", "end": END})
        workflow.add_edge("book", "monitor")
        workflow.add_edge("monitor", END)

        return workflow.compile()

    async def run_full_pipeline(self, prompt: str, auto_approve: bool = True) -> dict[str, Any]:
        """Executes the entire 5-Agent pipeline from prompt to booking confirmation."""
        event_id = f"evt_{uuid.uuid4().hex[:8]}"
        
        # 1. Analyze
        requirements, req_log = self.requirements_agent.run(prompt)
        
        # 2. Budget
        budget_plan, b_log = self.budget_agent.run(requirements)
        
        # 3. Parallel Vendor Search
        budget_map = budget_plan.get("category_allocations", {})
        categories = [c for c in CATEGORY_ORDER if c in budget_map] + [c for c in budget_map if c not in CATEGORY_ORDER]

        async def worker(category: str):
            agent = VendorSearchAgent(category=category, memory=memory)
            return await agent.run(requirements, budget_map[category])

        results = await asyncio.gather(*(worker(category) for category in categories))
        vendor_results = {category: result for category, result in zip(categories, results)}
        
        search_log = AgentLogger.create_log(
            agent_name="Autonomous Vendor Discovery Agents (Parallel)",
            step="Parallel Category Search",
            thought=f"Searched top suppliers across {len(categories)} categories with verified inclusions and photos.",
            action=f"Discovered candidate vendor packages for {', '.join(categories)}.",
            result_summary=f"Shortlisted candidate options across {len(categories)} categories.",
        )

        # 4. Aggregate & Rank
        recommendations, agg_log = self.aggregator_agent.run(vendor_results)

        # 5. Book & Generate Timeline
        top_package = [vendors[0] for vendors in recommendations.values() if vendors]
        booking_data, book_log = self.booking_monitor_agent.run_booking(
            event_id=event_id,
            approved_vendors=top_package,
            requirements=requirements,
            budget_plan=budget_plan,
        )

        # 6. Initialize Sentinel Monitoring
        monitoring_data = self.booking_monitor_agent.run_monitoring(event_id, booking_data)

        all_logs = [req_log, b_log, search_log, agg_log, book_log]
        
        state_data = {
            "event_id": event_id,
            "status": "booked",
            "requirements": requirements,
            "budget_plan": budget_plan,
            "recommendations": recommendations,
            "curated_package": top_package,
            "booking_data": booking_data,
            "monitoring_data": monitoring_data,
            "run_of_show": booking_data.get("run_of_show", []),
            "agent_logs": all_logs,
            "timeline": [
                {"step": "requirements_analyzed", "complete": True},
                {"step": "budget_allocated", "complete": True},
                {"step": "vendors_shortlisted", "complete": True},
                {"step": "approved_by_user", "complete": True},
                {"step": "booking_confirmed", "complete": True},
            ],
        }
        memory.set(f"event:{event_id}", state_data)
        memory.set("current_event", state_data)
        return state_data

    async def run_requirement_and_budget(self, prompt: str) -> dict[str, Any]:
        requirements, req_log = self.requirements_agent.run(prompt)
        budget_plan, budget_log = self.budget_agent.run(requirements)
        logs = [req_log, budget_log]
        memory.set("current_event", {"requirements": requirements, "budget_plan": budget_plan, "agent_logs": logs})
        return {"requirements": requirements, "budget_plan": budget_plan, "agent_logs": logs}

    async def run_vendor_search(self, requirements: dict[str, Any], budget_plan: dict[str, Any]) -> dict[str, Any]:
        budget_map = budget_plan.get("category_allocations", {})
        categories = [category for category in CATEGORY_ORDER if category in budget_map] + [c for c in budget_map if c not in CATEGORY_ORDER]

        async def worker(category: str):
            agent = VendorSearchAgent(category=category, memory=memory)
            return await agent.run(requirements, budget_map[category])

        results = await asyncio.gather(*(worker(category) for category in categories))
        return {category: result for category, result in zip(categories, results)}

    async def run_aggregation(self, vendor_results: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
        recommendations, agg_log = self.aggregator_agent.run(vendor_results)
        current = memory.get("current_event", {})
        memory.set("current_event", {**current, "recommendations": recommendations})
        return recommendations, agg_log

    async def run_booking(
        self,
        approved_vendors: list[dict[str, Any]],
        event_id: str,
        requirements: dict[str, Any] | None = None,
        budget_plan: dict[str, Any] | None = None,
        custom_run_of_show: list[dict[str, Any]] | None = None,
    ) -> tuple[dict[str, Any], dict[str, str]]:
        return self.booking_monitor_agent.run_booking(
            event_id=event_id,
            approved_vendors=approved_vendors,
            requirements=requirements,
            budget_plan=budget_plan,
            custom_run_of_show=custom_run_of_show,
        )

    async def run_monitoring(self, event_id: str, booking_data: dict[str, Any]) -> dict[str, Any]:
        return self.booking_monitor_agent.run_monitoring(event_id, booking_data)

    async def replan_category(self, event_id: str, category: str) -> tuple[dict[str, Any], dict[str, str]]:
        current = memory.get(f"event:{event_id}") or memory.get("current_event", {})
        requirements = current.get("requirements", {})
        budget_plan = current.get("budget_plan", {})
        budget_slice = budget_plan.get("category_allocations", {}).get(category, 50000.0)

        replan_data, log = await self.booking_monitor_agent.handle_cancellation(
            event_id=event_id,
            category=category,
            requirements=requirements,
            budget_slice=budget_slice,
        )
        return replan_data, log


__all__ = ["EventWorkflowEngine", "EventState"]
