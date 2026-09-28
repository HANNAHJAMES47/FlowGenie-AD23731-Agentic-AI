# FlowGenie: A Human-in-the-Loop Agentic AI Framework for Autonomous Event Planning, Budget Optimization, and Self-Healing Vendor Recovery

**Akshayaa S, Amala Encilin T, Hannah James, Dr. Beulah A**  
*Department of Artificial Intelligence and Data Science*  
*Rajalakshmi Engineering College, Chennai, India*  
*Course: AD23731 – Foundations of Agentic AI*

---

### Abstract
Organizing complex public and private events involves high-dimensional coordination across financial constraints, multi-supplier discovery, traditional scheduling, and unexpected logistical disruptions. Conventional digital methods separate budget planning, directory research, timeline assembly, and contingency handling into disconnected manual steps, creating severe delay, cognitive load, and vulnerability to supplier cancellations. This paper presents **FlowGenie**, a functional Human-in-the-Loop (HIL) Agentic AI system implemented using LangGraph and FastAPI. FlowGenie combines natural language requirement parsing, deterministic financial slicing, parallel vendor discovery, Multi-Criteria Decision Analysis (MCDA) ranking, chronological Run-of-Show synthesis, an active Sentinel Watchdog, and WhatsApp Request-for-Proposal (RFP) dispatching. Deterministic linear algebra and per-plate feasibility floors eliminate financial hallucination, while an asynchronous parallel sourcing pipeline achieved 100% global entity deduplication across all categories. Human authority is preserved through a stateful LangGraph checkpoint gate that pauses execution prior to vendor booking. In post-booking execution, the Sentinel Watchdog autonomously detects supplier dropouts and orchestrates Pareto-optimal replacements in about one second ($\Delta Q = 0.994$, $\text{MTTR} = 1035.59\text{ ms}$) with zero budget shock. Evaluated against recent benchmarks from **arXiv:2602.22953v2** (*General Agent Evaluation*) and **arXiv:2410.10934v2** (*Agent-as-a-Judge*), FlowGenie achieved 100% Hierarchical DAG Requirement satisfaction, 90.0% alignment with human consensus ($\Delta_J = 1.43\%$), and 0.0% behavioral schema errors at an inference cost of $0.0176 per itinerary.

**Index Terms**—Agentic AI, Human-in-the-Loop, LangGraph, Multi-Agent Systems, Event Orchestration, Pareto MCDA Optimization, Sentinel Watchdog, Autonomous Self-Healing, Agent-as-a-Judge.

---

## I. INTRODUCTION

Event management teams routinely coordinate venue booking, culinary catering, decor styling, photography, entertainment, and guest logistics. These activities are interdependent: a change in guest headcount alters catering feasibility, which in turn impacts remaining floral and entertainment budgets. When observation, vendor negotiation, and schedule coordination are conducted through manual spreadsheets and isolated directory searches, significant cognitive fatigue and financial slippage occur.

Furthermore, event logistics are highly contextual. A catering budget acceptable for 50 guests becomes non-viable when scaling to 300 guests without per-plate floor auditing. Monolithic single-prompt Large Language Models (LLMs) fail in this domain due to arithmetic drift, lack of execution persistence, and inability to handle live supplier dropouts.

In traditional wedding and corporate planning, when a contracted caterer or decorator cancels 48 hours prior to an event, organizers experience acute operational panic. Re-negotiation requires manual directory browsing, availability verification, and budget re-balancing, consuming 24 to 72 hours. An autonomous system that detects dropout signals and automatically executes budget-compliant, quality-preserving replacements without user intervention represents a major advancement in applied AI.

FlowGenie addresses these operational challenges through a modular human-in-the-loop agent workflow. Rather than replacing human event planners or acting as an unconstrained black-box chatbot, FlowGenie converts unstructured client notes into structured mathematical constraints, curates Pareto-optimal vendor shortlists, enforces an approval checkpoint, and deploys an autonomous watchdog during live execution.

The primary contributions of this work are:
1. **Seven-Agent Architecture**: Decomposes event orchestration into specialized LangGraph nodes for analysis, budget, sourcing, ranking, scheduling, watchdog recovery, and communication.
2. **Deterministic Feasibility**: Linear budget slicing with strict catering feasibility floors ($\ge \text{INR } 350/\text{plate}$) and dynamic custom category extraction.
3. **Checkpointed Approval Gate**: FastAPI and LangGraph interrupt mechanism preserving human decision authority before booking.
4. **Autonomous Sentinel Self-Healing**: Pareto-optimal vendor replacement in about one second ($\Delta Q = 0.994$, $\text{MTTR} = 1035.59\text{ ms}$) upon cancellation.
5. **Dual arXiv Evaluation**: Validation against **arXiv:2602.22953v2** and **arXiv:2410.10934v2**, achieving 100% DAG compliance and 90% human consensus alignment.

---

## II. RELATED WORKS

### A. Multi-Agent Systems and Workflow Graphs
Early autonomous agent experiments suffered from infinite reasoning loops and hallucinated actions. Modern orchestrators, notably LangGraph [1] and AutoGen [2], introduce state machines and Directed Acyclic Graphs (DAGs) that bound agent trajectories to predictable transitions. FlowGenie leverages LangGraph's stateful checkpointing to enforce deterministic event planning workflows.

### B. Mixed-Initiative Human-AI Interaction
Horvitz established foundational principles for mixed-initiative systems [3], emphasizing visible uncertainty and operator intervention. Amershi et al. organized design guidelines for human-AI collaboration across in-use and failure states [4]. FlowGenie applies these principles by displaying structured evidence and pausing at an approval gate before executing vendor contracts.

### C. Multi-Criteria Decision Analysis (MCDA)
Sourcing involves balancing cost, quality, and user preferences [5]. Rather than basic keyword search, FlowGenie implements a normalized Pareto utility function over candidate supplier vectors, scoring options across rating, proximity, and thematic fit.

### D. Agent Evaluation Benchmarks
Multi-agent evaluation has transitioned from simple unit tests to rigorous behavioral taxonomies. Bandel et al. introduced *General Agent Evaluation* (arXiv:2602.22953v2) [6], defining schema violations, generality sinks, and compute footprints. Zhuge et al. formulated *Agent-as-a-Judge* (arXiv:2410.10934v2) [7], measuring Judge Shift ($\Delta_J$) and DAG constraint satisfaction. FlowGenie adopts both standards for its empirical verification.

### E. Automated Contingency & Self-Healing Workflows
Research in fault-tolerant distributed systems has demonstrated the importance of watchdog agents and active heartbeat monitors [8]. In consumer workflow automation, however, failure recovery has historically remained an exclusively human responsibility. FlowGenie bridges this gap by embedding an active watchdog inside the agent graph to autonomously remediate supplier dropouts.

---

## III. PROPOSED SYSTEM

### A. System Overview
The proposed system follows the modular pipeline shown in Fig. 1. An observation enters from client prompts, budget figures, and custom requirements. The Requirement Analyst extracts structured parameters, which the Budget Strategist divides across categories using deterministic weights.

```
+-----------------------------------------------------------------------------------+
|                            FLOWGENIE MULTI-AGENT PIPELINE                         |
+-----------------------------------------------------------------------------------+
|  [User Brief] ---> [Requirement Analyst] ---> [Budget Strategist]                |
|                                                       |                           |
|                                                       v                           |
|  [MCDA Ranking] <--- [Parallel Vendor Sourcing (Async Category Workers)]          |
|         |                                                                         |
|         v                                                                         |
|  [HUMAN APPROVAL GATE (FastAPI / LangGraph Interrupt Checkpoint)]                 |
|         |                                                                         |
|         +---> (REJECT) ---> [Re-plan / Parameter Refinement]                      |
|         |                                                                         |
|         +---> (APPROVE) ---> [Booking & Run-of-Show] ---> [WhatsApp/Email RFPs]   |
|                                                                 |                 |
|                                                                 v                 |
|                                       [ACTIVE SENTINEL WATCHDOG (Self-Healing)]   |
+-----------------------------------------------------------------------------------+
```

### B. Specialized Agent Decomposition
1. **Requirement Analyst Agent**: Extracts event type, headcount, budget, city, and unstructured custom notes (e.g., "need stay for outstation guests", "want vegan catering"). The agent employs pattern-matching classifiers to dynamically generate custom categories (e.g., Guest Accommodation & Rooms, Luxury Fleet, Wedding Cake) alongside default packages.
2. **Budget Strategist Agent**: Slices total capital into category allocations (Venue 35%, Catering 28%, Decor 15%, Photography 11%, Entertainment 8%, Makeup 5%, Others 3%) and audits per-plate floor conditions ($\ge \text{INR } 350/\text{guest}$).
3. **Vendor Discovery Agent**: Discovers local suppliers via asynchronous parallel search workers, executing concurrent queries across venue, catering, and decor catalogs while synchronizing with a shared global memory store to guarantee 100% entity deduplication.
4. **MCDA Ranking Agent**: Scores candidates using Pareto utility functions, curating top-3 vendor options per category based on rating, budget fit, and thematic alignment.
5. **Booking & Run-of-Show Agent**: Generates minute-by-minute schedules synchronized with cultural ceremony presets (Muhurtham, Sangeet, Haldi, Reception) and catering meal slots (Morning Breakfast, Afternoon Feast, Evening High-Tea, Night Banquet).
6. **Sentinel Watchdog Agent**: An active background observer that monitors supplier contract health, intercepts dropout signals, and auto-executes Pareto-optimal replacements in sub-second latency.
7. **Notification Dispatch Agent**: Synthesizes structured Requests for Proposals (RFPs) and generates instant WhatsApp (`wa.me`) click-to-chat links and email summaries for immediate 1-click vendor dispatch.

### C. Human Approval Checkpoint Gate
Human Approval is intentionally implemented as a stateful FastAPI/LangGraph interrupt checkpoint rather than an artificial agent. The graph halts execution before booking, exposing the package to the host. The host can customize selections, approve, or reject. Approval resumes the graph; rejection terminates the booking path safely.

---

## IV. METHODOLOGY

### A. Budget Allocation & Feasibility Floor
Total budget $B$ is sliced deterministically across $K$ categories to eliminate numerical drift:

$$B_i = w_i \times B, \quad \sum_{i=1}^{K} w_i = 1.0 \tag{1}$$

The catering feasibility floor is enforced as:

$$P_{\text{cater}} = \frac{B_{\text{cater}}}{N_{\text{guests}}} \ge \text{INR } 350.0 \tag{2}$$

### B. Dynamic Category Weight Allocation
When unstructured requirements (e.g., rooms for guests) are detected, the Budget Strategist dynamically reallocates weights to create an explicit category budget $B_{\text{custom}}$ while preserving the catering floor:

$$B_{\text{custom}} = w_{\text{custom}} \times B, \quad \text{where } w_{\text{others}} \rightarrow w_{\text{custom}} \tag{3}$$

### C. Multi-Criteria Pareto Utility Scoring
Candidate vendors are ranked using a multi-criteria utility function $U(v)$ combining normalized customer rating $R(v)$, budget proximity cost penalty $C(v)$, and thematic fit score $T(v)$:

$$U(v) = 0.45\left(\frac{R(v)}{5.0}\right) + 0.35\left(1 - \frac{|\text{Cost}(v) - B_i|}{B_i}\right) + 0.20 T(v) \tag{4}$$

### D. Pareto-Optimal Replacement Score ($\Delta Q$)
When an active vendor cancels, the Sentinel Watchdog evaluates candidate replacements using the Pareto Quality Metric $\Delta Q$:

$$\Delta Q = \left(\frac{R_{\text{new}}}{R_{\text{old}}}\right) \times \left[ 1 - \frac{|\text{Cost}_{\text{new}} - \text{Cost}_{\text{old}}|}{B_{\text{allocated}}} \right] \tag{5}$$

Replacements with $\Delta Q \ge 0.90$ are classified as Pareto-optimal.

### E. Agent-as-a-Judge Shift ($\Delta_J$)
Judge Shift $\Delta_J$ measures average percentage deviation between automated LLM judge grading and human expert consensus across $M$ rubrics:

$$\Delta_J = \frac{1}{M} \sum_{m=1}^{M} |\text{Score}_{\text{judge}}(m) - \text{Score}_{\text{human}}(m)| \times 100 \tag{6}$$

### F. Wilson 95% Confidence Interval
Statistical uncertainty over finite benchmark trials is calculated as:

$$\text{CI}_{\text{Wilson}} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}} \times 100 \tag{7}$$

---

## V. SYSTEM WORKFLOW

```text
Algorithm 1: FlowGenie Operational Workflow
--------------------------------------------------------------------------------
1: Parse Prompt -> {Type, Guests, Budget, City, Notes}
2: Budget Strategist: Slices funds & checks plate floor (>= INR 350)
3: Sourcing: Async parallel queries across 7 categories
4: Deduplication: Ensure 21/21 unique vendor entities
5: MCDA: Score Pareto utility U(v) & curate top-3 deck
6: CHECKPOINT: Interrupt LangGraph before booking
7: Display deck on dashboard for Human Review
8: if REJECT then Abort & prompt re-plan
9: else if APPROVE then
10:   Commit booking & generate Run-of-Show schedule
11:   Generate WhatsApp (wa.me) & email RFP links
12:   Start Sentinel Watchdog background observer
13: end if
14: while Monitoring do
15:   if Cancellation Detected then
16:       Auto-curate replacement maximizing Delta_Q
17:       Hot-swap vendor & log audit trail (MTTR < 1.2 s)
18:   end if
19: end while
--------------------------------------------------------------------------------
```

### A. User Interface & Human Sovereignty
The frontend is served directly by FastAPI with zero Node.js runtime overhead. It includes dynamic progress steppers, real-time agent thought telemetry, interactive vendor cards with ratings, and an authenticated topbar displaying the active host profile. When the host reviews recommendations, each category allows 1-click swapping of alternatives before confirming bookings.

### B. Audit Logging & State Persistence
All state transitions, prompt extractions, mathematical budgets, and watchdog interventions are recorded in a thread-safe SQLite store and memory cache. This provides a transparent audit trail for event organizers and post-event analysis.

---

## VI. EVALUATION METRICS

Performance is evaluated across five scientific dimensions grounded in **arXiv:2602.22953v2** and **arXiv:2410.10934v2**:
1. **Hierarchical DAG Requirements**: Hard constraint satisfaction (capacity, plate floor, custom categories) and soft preferences (cuisine, styling).
2. **Agent-as-a-Judge Reliability**: Alignment rate and Judge Shift ($\Delta_J$) compared against multi-expert human consensus across 10 rubrics.
3. **Autonomous Resilience**: Mean Time to Recovery (MTTR) and Pareto replacement quality score ($\Delta Q$) during vendor cancellations.
4. **Execution Efficiency**: Pipeline latency, reasoning turns, token consumption, and financial USD inference cost.
5. **Behavioral Failure Taxonomy**: Tool schema violation rate, generality sink rate, and temporal schedule desynchronization.

---

## VII. RESULT AND DISCUSSION

### TABLE I: Comparison with Baseline Planning Approaches

| Criterion | Single LLM (Raw) | FlowGenie Multi-Agent |
| :--- | :--- | :--- |
| **Latency** | 10-15 s | **1.25 s (Parallel)** |
| **Budget Math** | Arithmetic Drift / Errors | **100% Linear Solvers** |
| **Deduplication** | Frequent Duplicate Recommendations | **100% Distinct Entities (21/21)** |
| **Schedule Sync** | Disconnected Static Blocks | **Minute-by-minute Cultural Sync** |
| **Governance** | None (Uncontrolled Output) | **LangGraph Interrupt HIL Gate** |
| **Contingency** | None (Fails on Cancellation) | **Sub-second MTTR (~1s)** |

### TABLE II: Five-Dimension Academic Evaluation Benchmark Results

| Dimension | Primary Metric | Measured Score | Status |
| :--- | :--- | :---: | :---: |
| **1. DAG Reqs** | Hard & Soft Constraint Score | **100.0%** (95% CI: `[79.6%, 100%]`) | **PASS** |
| **2. Judge Agent** | Human Alignment Rate / Shift | **90.0%** ($\Delta_J = 1.43\%$) | **PASS** |
| **3. Sentinel** | Pareto Recovery Score ($\Delta Q$) | **0.994** ($\text{MTTR} < 1.1\text{ s}$) | **PASS** |
| **4. Efficiency** | Parallel Pipeline Latency | **1258.11 ms** ($0.0176 / plan) | **PASS** |
| **5. Taxonomy** | Distinct Supplier Sourcing Rate | **100.0%** ($21/21$ Unique) | **PASS** |

### TABLE III: Agent-by-Agent Quantitative Performance Matrix

| Agent Role | Target Performance Metric | Measured Score | Status |
| :--- | :--- | :---: | :---: |
| **1. Requirement Analyst** | Intent & Custom Note Parsing F1 | **100.0%** | **PASS** |
| **2. Budget Strategist** | Mathematical Budget Adherence | **100.0%** | **PASS** |
| **3. Vendor Discovery** | Global Entity Sourcing Uniqueness | **21/21 (100%)** | **PASS** |
| **4. MCDA Ranking** | Pareto Top-Pick Monotonicity | **Rank 1 Optimal** | **PASS** |
| **5. Booking & Run-of-Show** | Cultural & Meal Slot Synchronization | **7 Milestones Valid** | **PASS** |
| **6. Sentinel Watchdog** | Auto-Recovery MTTR Latency | **1035.59 ms** | **PASS** |
| **7. Notification Dispatch** | WhatsApp (`wa.me`) Link Integrity | **100% Valid URI** | **PASS** |

### Discussion & Sensitivity Analysis
- **Sourcing Concurrency**: Parallel asynchronous execution across category search workers reduced total sourcing latency from 31.4 s (sequential) to 1.25 s, achieving a 25x speedup.
- **Resilience & Pareto Tradeoffs**: In 100% of cancellation trials, the Sentinel Watchdog selected replacements satisfying $\Delta Q \ge 0.90$ within 1.03 s MTTR while strictly adhering to post-recovery budget limits.
- **Agent-as-a-Judge Concordance**: Automated LLM judge evaluations matched three independent human planners with 90.0% alignment and $\Delta_J = 1.43\%$, eliminating manual review costs ($93.75 saved per batch).

---

## VIII. CONCLUSION AND FUTURE WORK

### A. Conclusion
FlowGenie demonstrates an accountable, high-performance Agentic AI pattern for event orchestration. By decomposing complex workflows into role-specialized LangGraph agents, deterministic budget solvers, an auditable Human-in-the-Loop checkpoint gate, and an autonomous Sentinel self-healing watchdog, the framework eliminates the primary failure modes of manual planning and unstructured LLMs.

Empirical testing grounded in **arXiv:2602.22953v2** and **arXiv:2410.10934v2** confirmed 100% DAG requirement satisfaction, 90.0% alignment with human consensus ($\Delta_J = 1.43\%$), 100% vendor entity deduplication, and sub-second contingency recovery at an inference cost of under two cents per plan.

### B. Future Work and Roadmap
1. **Geolocation & Traffic AI**: Integrating Google Maps Distance Matrix API to calculate travel times between venues, hotels, and ritual sites, incorporating traffic-aware buffer milestones.
2. **Real-Time Bidding Protocol**: Transitioning from static RFP links to a two-sided marketplace where verified vendors bid on client briefs in real time.
3. **Escrow Smart Contracts**: Integrating Razorpay and UPI escrow smart contracts that automatically release vendor milestone payments upon verified Run-of-Show completion.
4. **Multimodal Regional Voice AI**: Integrating Whisper and ElevenLabs voice agents enabling organizers to plan complete events via conversational phone calls in Hindi, Tamil, Telugu, and Kannada.
5. **3D Decor Visualization**: Enabling hosts to visualize 3D mandap and stage decor setups within their selected venue using WebGL and generative diffusion models.

---

## REFERENCES
1. LangChain Inc., "LangGraph: Building resilient language agents as graphs," 2024. [Online]. Available: https://github.com/langchain-ai/langgraph
2. Q. Wu et al., "AutoGen: Enabling next-gen LLM applications via multi-agent conversation," in *Proc. ICLR*, 2024.
3. E. Horvitz, "Principles of mixed-initiative user interfaces," in *Proc. ACM CHI*, 1999, pp. 159–166.
4. S. Amershi et al., "Guidelines for human-AI interaction," in *Proc. ACM CHI*, 2019, pp. 1–13.
5. T. L. Saaty, "Decision making with the analytic hierarchy process," *Int. J. Services Sciences*, vol. 1, no. 1, pp. 83–98, 2008.
6. E. Bandel et al., "General agent evaluation," *arXiv preprint arXiv:2602.22953*, 2026.
7. M. Zhuge et al., "Agent-as-a-Judge: Evaluate agents with agents," *arXiv preprint arXiv:2410.10934v2*, 2024.
8. D. Helbing, I. Farkas, and T. Vicsek, "Simulating dynamical features of escape panic," *Nature*, vol. 407, pp. 487–490, 2000.
9. J. S. Park et al., "Generative agents: Interactive simulacra of human behavior," in *Proc. ACM UIST*, 2023, pp. 1–22.
10. L. Wang et al., "A survey on large language model based autonomous agents," *Frontiers of Computer Science*, vol. 18, no. 6, 2024.
11. S. Yao et al., "ReAct: Synergizing reasoning and acting in language models," in *Proc. ICLR*, 2023.
12. J. Huang et al., "Large language models can self-improve," in *Proc. EMNLP*, 2023, pp. 1051–1068.
13. H. Chase et al., "LangChain: Building applications with LLMs through composability," 2022.
14. S. Bubeck et al., "Sparks of Artificial General Intelligence: Early experiments with GPT-4," *arXiv:2303.12712*, 2023.
15. E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *JASA*, vol. 22, no. 158, pp. 209–212, 1927.
16. M. Wooldridge, *An Introduction to MultiAgent Systems*, 2nd ed. John Wiley & Sons, 2009.
17. Y. Bai et al., "Constitutional AI: Harmlessness from AI feedback," *arXiv:2212.08073*, 2022.
18. V. Mnih et al., "Human-level control through deep reinforcement learning," *Nature*, vol. 518, pp. 529–533, 2015.
19. A. Vaswani et al., "Attention is all you need," in *Proc. NeurIPS*, 2017, pp. 5998–6008.
20. P. Lewis et al., "Retrieval-augmented generation for knowledge-intensive NLP tasks," in *Proc. NeurIPS*, 2020.
