"""
Unit test wrapper for the FlowGenie Multi-Agent Evaluation Suite.
Validates that all 5 arXiv-aligned dimensions and all 7 agents pass benchmarks.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evaluate_agents import FlowGenieAgentEvaluator


def test_multi_agent_evaluation():
    evaluator = FlowGenieAgentEvaluator()
    results = evaluator.run_all()
    
    # 1. Overall Status
    assert results["overall_status"] == "PASSED", f"Agent evaluation failed: {results}"
    assert results["system_metrics"]["agents_passed"] == 7, "Not all 7 agents passed unit evaluation."
    assert results["system_metrics"]["evaluation_dimensions_passed"] == 5, "Not all 5 evaluation dimensions passed."

    # 2. Dimension 1: Hierarchical DAG Satisfaction
    dag = results["hierarchical_dag_metrics"]
    assert dag["composite_dag_satisfaction_score"] >= 95.0, f"DAG score too low: {dag}"

    # 3. Dimension 2: Agent-as-a-Judge Alignment Rate
    judge = results["agent_as_a_judge_metrics"]
    assert judge["alignment_rate_pct"] >= 90.0, f"Agent-as-a-Judge alignment rate below 90%: {judge}"
    assert judge["judge_shift_pct"] <= 5.0, f"Judge shift too high: {judge}"

    # 4. Dimension 3: Sentinel Resilience & Pareto Score
    res = results["resilience_recovery_metrics"]
    assert res["pareto_replacement_score_delta_q"] >= 0.90, f"Pareto recovery score delta_q too low: {res}"
    assert res["mean_time_to_recovery_ms"] <= res["mttr_benchmark_ceiling_ms"], f"MTTR exceeded ceiling: {res}"

    # 5. Dimension 4: Execution Efficiency & Latency
    cost = results["execution_cost_metrics"]
    assert cost["status"] == "PASS", f"Execution efficiency failed: {cost}"

    # 6. Dimension 5: Behavioral Failure Taxonomy
    tax = results["behavioral_failure_taxonomy"]
    assert tax["distinct_entity_sourcing_rate_pct"] == 100.0, f"Duplicate entities detected: {tax}"
    assert tax["tool_schema_violation_rate_pct"] == 0.0, f"Schema violations detected: {tax}"
    assert tax["generality_sink_rate_pct"] == 0.0, f"Generality sink detected: {tax}"
    assert tax["temporal_schedule_desync_rate_pct"] == 0.0, f"Temporal schedule desync detected: {tax}"


if __name__ == "__main__":
    test_multi_agent_evaluation()
    print("\n[OK] All 5 evaluation dimensions & 7 agents validated successfully!")
