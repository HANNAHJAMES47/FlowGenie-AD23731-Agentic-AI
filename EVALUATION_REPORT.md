# FlowGenie Multi-Agent AI System Evaluation Report

**Academic Course**: AD23731 – Foundations of Agentic AI  
**Institution**: Rajalakshmi Engineering College  
**Timestamp**: 2026-09-28T12:06:35.070870  
**Overall Benchmark Status**: **PASSED**  
**Evaluation Standard**: Grounded in **arXiv:2602.22953v2** (*General Agent Evaluation*) & **arXiv:2410.10934v2** (*Agent-as-a-Judge*)  

---

## 1. Executive Summary & Dimension Scores

| Evaluation Dimension | Primary Scientific Metric | Measured Score | Standard / Baseline | Status |
| :--- | :--- | :---: | :---: | :---: |
| **1. Hierarchical DAG Requirements** | Hard & Soft Constraint Satisfaction | **100.0%** | $\ge 95.0\%$ | **PASS** |
| **2. Agent-as-a-Judge Reliability** | Human Consensus Alignment Rate | **90.0%** | $\ge 90.0\%$ | **PASS** |
| **3. Autonomous Resilience & Self-Healing** | Pareto Replacement Score ($\Delta Q$) | **0.994** | $\ge 0.90$ | **PASS** |
| **4. Execution Efficiency & Footprint** | Total Multi-Agent Pipeline Latency | **1130.66 ms** | $< 12000\text{ ms}$ | **PASS** |
| **5. Behavioral Error & Failure Taxonomy** | Distinct Supplier Sourcing Rate | **100.0%** | $\ge 95.0\%$ | **PASS** |

---

## 2. Dimension Breakdown & Empirical Formulations

### Dimension 1: Hierarchical DAG Requirement Satisfaction (Paper 2)
Tasks are modeled as a Directed Acyclic Graph (DAG) distinguishing between hard physical constraints and soft user preferences:
- **Hard Constraints Rate**: **100.0%** (95% Wilson Score CI: `[79.61%, 100.0%]`)
  - *Guest Scale & Venue Fit*: Exact headcount matched against vendor capacity.
  - *Catering Per-Plate Feasibility Floor*: Confirmed $\ge \text{INR } 350.0 / \text{guest}$.
  - *Dynamic Custom Category Extraction*: Extracted unstructured user notes (e.g. `stay`, `cake`, `transport`).
- **Soft Preferences Rate**: **100.0%** (95% Wilson Score CI: `[60.97%, 100.0%]`)
  - *Cuisine & Cultural Traditions*: South Indian, North Indian, Continental, and tradition presets.
- **Composite DAG Score**: **100.0%**

### Dimension 2: Agent-as-a-Judge Evaluation (Paper 2)
An independent Evaluator Agent inspected end-to-end plan artifacts against expert human planning rubrics:
- **Human Consensus Alignment Rate**: **90.0%** (95% CI: `[69.9%, 97.21%]`)
- **Judge Shift ($\Delta J$)**: **1.43%** (Mean absolute deviation from ground truth)
- **Cost & Time Reduction**: Replaces $93.75 of manual human labor with automated agent verification, achieving a **100.0% cost reduction** and **100.0% time reduction**.

### Dimension 3: Autonomous Resilience & Pareto Recovery Score (Paper 1 & 2)
The Sentinel Watchdog autonomously intercepted unexpected vendor dropouts:
- **Mean Time to Recovery (MTTR)**: **4122.87 ms** (Benchmark target: $< 5000\text{ ms}$).
- **Pareto-Optimal Replacement Score ($\Delta Q$)**: **0.994**
  $$\Delta Q = \frac{\text{Rating}_{\text{new}}}{\text{Rating}_{\text{old}}} \times \left(1 - \frac{|\text{Cost}_{\text{new}} - \text{Cost}_{\text{old}}|}{\text{Budget}_{\text{allocated}}}\right)$$
- **Post-Recovery Budget Guarantee**: Maintained 100% budget compliance without user-facing price shock.

### Dimension 4: Step Efficiency, Latency & Compute Footprint (Paper 1)
- **Multi-Agent Pipeline Latency**: **1130.66 ms** across 7 parallel & sequential turns.
- **Estimated Token Consumption**: ~2450 input tokens, ~1150 output tokens.
- **Estimated Financial Inference Cost**: **$0.017625** per generated event itinerary.

### Dimension 5: Behavioral Error & Failure Taxonomy (Paper 1)
- **Distinct Supplier Sourcing Rate**: **100.0%** (High-diversity vendor entities across 21 candidates).
- **Tool Schema Violation Rate**: **0.0%** (100% compliant with structured payloads).
- **Generality Sink / Dropped Category Rate**: **0.0%** (Zero early terminations).
- **Temporal Schedule Desync Rate**: **0.0%** (Zero meal-slot time mismatches).

---

## 3. Agent-by-Agent Quantitative Matrix

| Agent | Architecture / Role | Primary Metric | Measured Score | Status |
| :--- | :--- | :--- | :---: | :---: |
| **1. Requirement Analyst** | NLP Brief Parser & Custom Intent | Intent Extraction F1 | **100.0%** | **PASS** |
| **2. Budget Strategist** | Mathematical Slicer & Floor Auditor | Constraint Adherence | **100.0%** | **PASS** |
| **3. Vendor Discovery** | Parallel Concurrent Sourcing | Candidate Sourcing Diversity | **3 Candidates** | **PASS** |
| **4. MCDA Ranking** | Multi-Criteria Pareto Optimizer | Pareto Top-Pick Monotonicity | **Rank 1 Aligned** | **PASS** |
| **5. Booking & Traditions** | Chronological Scheduler | Cultural / Meal Sync | **7 Milestones** | **PASS** |
| **6. Sentinel Watchdog** | Autonomous Self-Healing Observer | Auto-Recovery Latency | **4122.87 ms** | **PASS** |
| **7. Notification Dispatch** | Communications Dispatcher | wa.me & Email URI Integrity | **100% Valid URI** | **PASS** |

---

## 4. Academic Citations
1. **General Agent Evaluation**: *Systematic Study of General Agents Across Heterogeneous Environments and Protocols* (arXiv:2602.22953v2).
2. **Agent-as-a-Judge**: *Evaluate Agents with Agents — Process-Supervised Intermediate Feedback and Hierarchical Requirements* (arXiv:2410.10934v2).
