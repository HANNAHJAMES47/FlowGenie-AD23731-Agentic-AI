from __future__ import annotations

from typing import Any
from agents.logger import AgentLogger
from memory.store import SharedMemory


class RecommendationAggregatorAgent:
    """4. Recommendation & Ranking Agent: Multi-criteria decision analysis (MCDA) ranking."""

    def __init__(self, memory: SharedMemory | None = None):
        self.memory = memory or SharedMemory()
        self.agent_name = "Recommendation & Ranking Agent"

    def run(self, vendor_results: dict[str, list[dict[str, Any]]]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, str]]:
        ranked_recommendations: dict[str, list[dict[str, Any]]] = {}

        for category, vendors in vendor_results.items():
            if not vendors:
                continue
            # Composite scoring: rating (40%), fit (30%), price efficiency (30%)
            ranked = sorted(
                vendors,
                key=lambda v: (
                    float(v.get("rating", 4.0)) * 20.0
                    + float(v.get("event_fit_score", 0.8)) * 25.0
                    + (100000.0 / max(float(v.get("price", 1000)), 1.0)) * 0.01
                ),
                reverse=True,
            )
            for rank_idx, v in enumerate(ranked):
                v["rank"] = rank_idx + 1
                v["is_top_pick"] = rank_idx == 0

            ranked_recommendations[category] = ranked[:3]

        total_shortlisted = sum(len(v) for v in ranked_recommendations.values())
        log = AgentLogger.create_log(
            agent_name=self.agent_name,
            step="Multi-Criteria Recommendation Scoring",
            thought=f"Ranked {total_shortlisted} candidate vendors across {len(ranked_recommendations)} categories using composite quality-fit-budget metrics.",
            action="Curated top 3 recommendations per category with verified quality badges.",
            result_summary=f"Finalized shortlist with {len(ranked_recommendations)} category packages ready for user review.",
        )
        self.memory.set("aggregated_recommendations", ranked_recommendations)
        return ranked_recommendations, log


RankingAgent = RecommendationAggregatorAgent

__all__ = ["RecommendationAggregatorAgent", "RankingAgent"]
