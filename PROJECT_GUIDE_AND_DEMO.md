# FlowGenie — Project Explanation & Mentor Demo Guide

**Project Name**: FlowGenie: Multi-Agent AI Event Planning & Autonomous Contingency Management  
**Course**: AD23731 – Foundations of Agentic AI  
**Institution**: Rajalakshmi Engineering College  
**Team**: Akshayaa S (231801007), Amala Encilin T (231801009), Hannah James (231801047)  
**Faculty Guide**: Dr. Beulah A  

---

## 1. Project Overview (What is FlowGenie?)

### The Real-World Problem:
Planning medium-to-large-scale events (Weddings, Corporate Galas, Birthdays) is stressful, time-consuming, and prone to last-minute chaos:
- **Budget Overruns**: Hosts struggle to mathematically divide budgets across 7 distinct categories (Venue, Catering, Decor, Photography, Entertainment, Makeup, Logistics).
- **Fragmented Research**: Hosts spend days jumping between search directories (Justdial, WedMeGood) with unverified numbers and repetitive listings.
- **Timing Misalignment**: Catering meals (Breakfast vs. Lunch vs. Dinner) and family rituals are disconnected from vendor booking.
- **Vendor Cancellations (Panic Point)**: When a supplier abruptly cancels, the organizer has zero instant backup options.

### The FlowGenie Solution:
FlowGenie is an **autonomous Multi-Agent AI system** orchestrated with **LangGraph** and **FastAPI** that:
1. Automatically computes mathematical budget breakdowns.
2. Discovers and ranks verified local suppliers across all 7 categories.
3. Dynamically generates an **hour-by-hour schedule** synchronized with family customs (e.g., South Indian Muhurtham, Sangeet, Christian Vows).
4. Enforces a **Human Approval Gate** before any financial commitments are locked.
5. Provides a background **Sentinel Watchdog** that autonomously detects supplier cancellations and provisions **1-click budget-compliant replacements in under 1 second**.
6. Auto-generates **WhatsApp (`wa.me`) and Email RFPs** to dispatch to suppliers instantly.

---

## 2. Step-by-Step Guide to Run the Project (Live Demo Flow)

### Step 1: Open Terminal & Activate Virtual Environment
Open PowerShell in the project directory (`d:\Agentic ai project`) and run:
```powershell
.\.venv\Scripts\Activate.ps1
```
*(You will see `(.venv)` appear at the start of your terminal line).*

---

### Step 2: Start the FlowGenie Application Server
Start the local FastAPI server:
```powershell
python run_local.py
```
*(The backend server will start at `http://127.0.0.1:8000/`)*.

---

### Step 3: Open the Web Application in Browser
Open Google Chrome or Edge and navigate to:
👉 **`http://127.0.0.1:8000/`**

---

### Step 4: Live Demo Script for Your Mentor

#### **A. Show the Event Input Form**
1. On the home page, select or type:
   - **Event Type**: `Wedding`
   - **City / Location**: `Bangalore`
   - **Guest Count**: `150`
   - **Budget Limit**: `450000` (₹4.5 Lakhs)
   - **Event Timing Slot**: `Morning (8:00 AM - 1:00 PM)`
   - **Catering Meal Slot**: `Morning (Breakfast/Pooja)`
   - **Cuisine**: `South Indian Pure Veg`
   - **Visual Theme**: `Royal Traditional`
2. Click **"Generate Multi-Agent Plan"**.

#### **B. Explain the Multi-Agent Execution in Progress**
- Show your mentor the live agent thinking logs on screen:
  - *Requirement Agent* normalizes parameters.
  - *Budget Agent* creates category slices.
  - *Vendor Agent* fetches candidates from live web search and catalog.
  - *Ranking Agent* calculates Pareto composite scores.

#### **C. Show the Vendor Recommendation & Custom Schedule View**
1. **Category Packages**: Point out that there are **Top-3 ranked vendor cards** for each of the 7 service categories.
   - Show that all vendor names are **100% distinct and unique**.
   - Show the **`Morning (Breakfast/Pooja)`** meal timing badge on the catering card.
   - Show the verified 4.8★ ratings, phone numbers, and photo galleries.
2. **Interactive Schedule Customizer**:
   - Scroll down to the **"Customize Hour-by-Hour Schedule"** section.
   - Show that it generated an authentic **South Indian Muhurtham** schedule with Breakfast at `08:00 AM` and Muhurtham at `09:00 AM`.
   - Click **"Add Milestone"** or change a ritual to demonstrate live customizability directly during vendor selection.

#### **D. Demonstrate Human Approval Checkpoint Gate**
- Explain to your mentor: *"Our AI never spends money automatically. LangGraph pauses execution at this FastAPI checkpoint."*
- Click **"Confirm & Lock Booking"**.

#### **E. Show Confirmed Itinerary & WhatsApp Dispatch**
1. The **Booking Confirmation View** opens.
2. Show the **"Download Itinerary"** button.
3. Show the **"Dispatch Supplier RFPs (WhatsApp)"** button:
   - Click it to show the pre-formatted WhatsApp brief containing the exact guest count, date, start time, and catering meal timing.

#### **F. Demonstrate the Sentinel Watchdog (Self-Healing Auto-Recovery)**
1. In the Confirmed View, scroll to the **Sentinel Watchdog Status Card** (Green Shield: `ACTIVE MONITORING`).
2. Click **"Simulate Vendor Cancellation"** (e.g., Catering defaults).
3. **Observe the Magic**:
   - The Sentinel Watchdog detects the cancellation instantly ($< 1\,\text{second}$).
   - An **Emergency Backup Modal** opens showing top-ranked replacement caterers within the exact budget slice.
   - Click **"Accept Replacement"** — the contract updates without disturbing the rest of the event!

---

### Step 5: Run Automated Tests & Multi-Agent Benchmark
Show your mentor that the entire codebase is verified with unit tests:
```powershell
python run_tests.py
```
*(Runs all 7 test suites: Auth, Unique Vendors, Custom Schedule, Timing Slots, Personalization, Sentinel Automation, and Agent Evaluation — all pass 100%).*

To run the agent benchmark evaluation report:
```powershell
python evaluate_agents.py
```
*(Generates `evaluation_report.json` and `EVALUATION_REPORT.md` with measured latencies and accuracy scores).*

---

## 3. How We Get Data (Data Sourcing & Agentic RAG)

FlowGenie uses a **Dual-Tier Data Sourcing Pipeline** to ensure vendor data is realistic, accurate, and never hallucinated:

```
[User Input (City, Category, Budget)]
                 │
                 ▼
 ┌──────────────────────────────────────────────────────────┐
 │  TIER 1: Real-Time Live Web Sourcing (Tavily Search API) │
 │  - Queries: "top wedding caterers in Bangalore Justdial" │
 │  - Queries: "photography studios in Mumbai WedMeGood"    │
 │  - Fetches: Business names, real ratings, addresses      │
 └────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
 ┌──────────────────────────────────────────────────────────┐
 │  TIER 2: Curated & Verified Regional Catalog (Fallback)  │
 │  - Calibrated baseline pricing in Indian Rupees (INR)    │
 │  - Verified contact numbers & capacity specs             │
 │  - Handcrafted SVG vector visual assets & photo suites   │
 └────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
 ┌──────────────────────────────────────────────────────────┐
 │  FILTERING, BRAND CLEANING & DEDUPLICATION ENGINE        │
 │  - Strips clickbait titles ("Top 10 Planners", "Check")  │
 │  - Enforces global distinct supplier deduplication       │
 │  - Attaches meal timing badges & Pareto ranking scores   │
 └──────────────────────────────────────────────────────────┘
```

### Why this is better:
- **No Hallucinations**: Prices are grounded in real Indian Rupees (INR) with per-guest plate formulas.
- **100% Unique Names**: Deduplication guarantees that no two categories share the same company name.
- **Meal-Slot Grounding**: Catering vendors are tagged specifically for Morning, Afternoon, or Night meals.

---

## 4. How the Multi-Agent System Works (The 7 AI Agents)

FlowGenie divides event planning into 5 sequential planning agents plus 2 autonomous background agents:

```
[Raw User Prompt / Form]
           │
           ▼
[1. Requirement Analysis Agent] ─── (Parses guest count, budget, date, cuisine, traditions)
           │
           ▼
[2. Budget Planning Agent]      ─── (Applies mathematical category weights: Venue 34%, Catering 32%, etc.)
           │
           ▼
[3. Vendor Sourcing Agent]      ─── (Live Tavily search on Justdial/WedMeGood + Curated Catalog)
           │
           ▼
[4. Recommendation Agent]       ─── (Pareto ranking: 40% Rating + 35% Price Proximity + 25% Fit)
           │
           ▼
[Dynamic Run-of-Show Engine]    ─── (Builds customized hour-by-hour milestones with meal timing sync)
           │
           ▼
[FASTAPI HUMAN APPROVAL GATE]   ─── (PAUSES EXECUTION. User reviews, edits schedule, and confirms)
           │
           ▼
[5. Booking Agent]              ─── (Locks contracts, calculates final spend, and saves itinerary)
           │
           ▼
[6. Sentinel Watchdog Agent]    ─── (Monitors vendor health; triggers sub-second auto-replanning if cancelled)
           │
           ▼
[7. Notification Dispatch Agent]─── (Generates pre-filled WhatsApp wa.me links & supplier RFPs)
```

### Agent Responsibilities & Formulas:

1. **Requirement Analysis Agent**: Extracts numerical values, date normalization, timing slots, and cultural traditions.
2. **Budget Planning Agent**:
   - Calculates catering floor: $B_{\text{cater}} \ge N_{\text{guests}} \times P_{\text{min\_meal}}$
   - Allocates remaining budget across Venue, Decor, Photography, Entertainment, Makeup, and Logistics with a $2\%\text{--}3\%$ safety cushion.
3. **Vendor Sourcing Agent**: Discovers candidates across all 7 categories with real contact info.
4. **Ranking Agent (Pareto MCDA Scoring)**:
   $$S(v) = 0.40 \cdot \left(\frac{\text{Rating}}{5.0}\right) + 0.35 \cdot \Phi(\text{Price}, \text{Budget}) + 0.25 \cdot \text{FitScore}$$
5. **Booking & Run-of-Show Agent**: Synchronizes Breakfast (08:30 AM), Lunch (01:00 PM), and Dinner (08:30 PM) milestones.
6. **Sentinel Watchdog Agent**: Background monitor that executes autonomous 1-click replacement in **$< 1.0\,\text{second}$**.
7. **Notification Dispatch Agent**: Constructs instant click-to-chat `https://wa.me/` URLs with complete event details.

---

## 5. Technology Stack Summary

| Technology | Purpose in Project |
|---|---|
| **Python 3.12** | Core programming language for all agent logic and backend. |
| **FastAPI + Uvicorn** | High-speed asynchronous REST API endpoints with Pydantic validation. |
| **LangGraph** | Multi-agent state machine, conditional routing, and state checkpointing. |
| **Tavily Search API** | Real-time live web search targeting Justdial and Indian wedding directories. |
| **SQLite** | Persistent database for user authentication, password hashing, and audit logs. |
| **WhatsApp Web API (`wa.me`)** | Direct click-to-chat dispatch of supplier RFPs. |
| **HTML5, CSS3, ES6 JavaScript** | Zero-dependency responsive frontend client interface (HopeRise design). |

---

## 6. Faculty / Mentor Viva Q&A (Common Questions & Answers)

### Q1: Why did you use LangGraph instead of a simple single prompt to ChatGPT?
> **Answer**: *"A single LLM prompt cannot guarantee budget math, cannot perform multi-source directory searches, and suffers from hallucinations. LangGraph allows us to split the problem into specialized modular agents, maintain state checkpoints, and enforce a strict Human-in-the-Loop approval gate before any booking is made."*

### Q2: How do you guarantee that the budget is never exceeded?
> **Answer**: *"Our Budget Planning Agent uses deterministic mathematical algorithms rather than probabilistic text generation. It applies weighted linear category slicing with a mandatory catering per-plate floor ($N_g \times P_{min\_meal}$) and reserves an unallocated $2\%\text{--}3\%$ contingency buffer."*

### Q3: How do you get data for non-catering services like decor or photography?
> **Answer**: *"The Vendor Agent dynamically constructs targeted queries per category (e.g., 'photographers in Bangalore WedMeGood', 'stage decor in Mumbai Justdial'). Tavily Search retrieves live business listings. We clean generic clickbait titles, deduplicate names, and combine them with our curated catalog of pricing benchmarks and equipment specifications."*

### Q4: What happens if a booked vendor cancels on the event day?
> **Answer**: *"Our Sentinel Watchdog Agent autonomously detects the cancellation anomaly, isolates only the affected category, queries the pre-computed candidate pool for within-budget replacements, and presents 1-click recovery options on the dashboard in under $1.0\,\text{second}$ without disrupting the rest of the event."*

### Q5: How is user authentication and session continuity handled?
> **Answer**: *"We implemented secure PBKDF2-HMAC-SHA256 password hashing in SQLite with session recovery tokens. When logged in, the user can save favorites, review past event itineraries, and modify active schedules seamlessly."

---

## 7. Project File Structure Reference

```
d:\Agentic ai project\
├── agents\                     # 7 Multi-Agent Implementations
│   ├── requirement_agent.py   # 1. Requirement Intent Parser
│   ├── budget_agent.py        # 2. Mathematical Budget Slicer
│   ├── vendor_agent.py        # 3. Live Tavily & Catalog Sourcing
│   ├── ranking_agent.py       # 4. Pareto MCDA Ranking Engine
│   ├── booking_agent.py       # 5. Run-of-Show Milestone Builder
│   ├── sentinel_agent.py      # 6. Self-Healing Watchdog Monitor
│   ├── notification_agent.py  # 7. WhatsApp & Email RFP Generator
│   └── auth_agent.py          # User Authentication & Database
├── api\
│   └── routes.py              # FastAPI REST Endpoints & Checkpoints
├── frontend\                  # HopeRise Web User Interface
│   ├── index.html             # Main Planning & Booking Interface
│   ├── login.html             # Auth Portal
│   ├── app.js                 # UI State & API Integration
│   └── styles.css             # HopeRise Palette & Modern UI
├── tests\                     # Comprehensive Test Suite
│   ├── test_auth_system.py
│   ├── test_unique_vendors.py
│   ├── test_custom_schedule.py
│   ├── test_timing_features.py
│   ├── test_personalization.py
│   ├── test_automation_systems.py
│   └── test_agent_evaluation.py
├── evaluate_agents.py         # Multi-Agent Benchmark Suite
├── run_tests.py               # 1-Click Master Test Runner
├── run_local.py               # Local FastAPI Server Runner
└── flowgenie_project_report.tex # Complete 8-Page LaTeX Report
```
