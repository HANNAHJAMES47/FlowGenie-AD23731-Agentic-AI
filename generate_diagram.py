import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_flowgenie_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_facecolor("#FAFAFA")
    fig.patch.set_facecolor("#FFFFFF")

    # Define box styles
    agent_box = dict(boxstyle="round,pad=0.5", fc="#EEF2FF", ec="#4F46E5", lw=1.5)
    hil_box = dict(boxstyle="round,pad=0.5", fc="#FEF3C7", ec="#D97706", lw=2.0)
    sentinel_box = dict(boxstyle="round,pad=0.5", fc="#ECFDF5", ec="#059669", lw=1.8)
    data_box = dict(boxstyle="round,pad=0.4", fc="#F3F4F6", ec="#6B7280", lw=1.2)

    # 1. User Input & Ingestion
    ax.text(0.12, 0.85, "1. User Requirement Brief\n• Event Type, Headcount\n• Budget (INR), City\n• Custom Notes (Stay/Cake)", 
            ha="center", va="center", bbox=data_box, fontsize=8.5, fontweight="bold", family="sans-serif")

    # 2. Requirement Analyst & Budget Strategist (Phase 1)
    ax.text(0.38, 0.85, "2. Requirement Analyst Agent\n• NLP Parameter Extraction\n• Dynamic Category Parsing", 
            ha="center", va="center", bbox=agent_box, fontsize=8.5, family="sans-serif")

    ax.text(0.64, 0.85, "3. Budget & Finance Strategist\n• Linear Slicing Math\n• Feasibility Floor (≥ ₹350/plate)", 
            ha="center", va="center", bbox=agent_box, fontsize=8.5, family="sans-serif")

    ax.text(0.90, 0.85, "4. Vendor Discovery Agent\n• Parallel Async Sourcing\n• Global Entity Deduplication", 
            ha="center", va="center", bbox=agent_box, fontsize=8.5, family="sans-serif")

    # 3. MCDA Ranking
    ax.text(0.90, 0.48, "5. MCDA Ranking Agent\n• Pareto Utility Scoring\n• Curates Top-3 Per Category", 
            ha="center", va="center", bbox=agent_box, fontsize=8.5, family="sans-serif")

    # 4. Human Approval Gate (Central Decision Checkpoint)
    ax.text(0.52, 0.48, "6. Human-in-the-Loop Approval Gate\n(FastAPI / LangGraph Interrupt Checkpoint)\n• Review Vendor Shortlist\n• Swap / Customize Items\n• [REJECT / ABORT] or [CONFIRM & BOOK]", 
            ha="center", va="center", bbox=hil_box, fontsize=9.5, fontweight="bold", family="sans-serif")

    # 5. Booking & Run-of-Show
    ax.text(0.15, 0.48, "7. Booking & Run-of-Show Agent\n• Minute-by-Minute Timeline\n• Cultural Muhurtham & Meal Sync", 
            ha="center", va="center", bbox=agent_box, fontsize=8.5, family="sans-serif")

    # 6. Notification Dispatch & Sentinel Watchdog
    ax.text(0.25, 0.15, "8. Notification Dispatch Agent\n• 1-Click WhatsApp (wa.me) RFPs\n• Client Contract Confirmation Email", 
            ha="center", va="center", bbox=agent_box, fontsize=8.5, family="sans-serif")

    ax.text(0.75, 0.15, "9. Autonomous Sentinel Watchdog\n• Active Execution Monitor (Background Heartbeat)\n• Autonomous Dropout Interception (MTTR < 1.2s)\n• Pareto Optimal Replacement (ΔQ = 0.994)", 
            ha="center", va="center", bbox=sentinel_box, fontsize=8.5, fontweight="bold", family="sans-serif")

    # Arrows
    arrow_props = dict(arrowstyle="->", color="#1E293B", lw=1.5, mutation_scale=15)
    sentinel_arrow = dict(arrowstyle="<->", color="#059669", lw=1.8, mutation_scale=15, linestyle="dashed")
    alert_arrow = dict(arrowstyle="->", color="#DC2626", lw=1.8, mutation_scale=15)

    ax.annotate("", xy=(0.26, 0.85), xytext=(0.20, 0.85), arrowprops=arrow_props)
    ax.annotate("", xy=(0.51, 0.85), xytext=(0.47, 0.85), arrowprops=arrow_props)
    ax.annotate("", xy=(0.77, 0.85), xytext=(0.73, 0.85), arrowprops=arrow_props)
    ax.annotate("", xy=(0.90, 0.58), xytext=(0.90, 0.77), arrowprops=arrow_props)
    ax.annotate("", xy=(0.69, 0.48), xytext=(0.80, 0.48), arrowprops=arrow_props)
    ax.annotate("", xy=(0.27, 0.48), xytext=(0.35, 0.48), arrowprops=arrow_props)
    ax.annotate("", xy=(0.18, 0.23), xytext=(0.15, 0.40), arrowprops=arrow_props)
    ax.annotate("", xy=(0.58, 0.15), xytext=(0.40, 0.15), arrowprops=arrow_props)

    # Sentinel feedback loop
    ax.annotate("Incident Self-Healing Loop", xy=(0.75, 0.38), xytext=(0.75, 0.24), arrowprops=sentinel_arrow,
                ha="center", va="center", fontsize=8, color="#059669", fontweight="bold")

    # Title & Subtitle
    plt.title("FlowGenie Multi-Agent System Architecture & Human-in-the-Loop Execution Graph", 
              fontsize=12, fontweight="bold", pad=15, color="#0F172A")
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    plt.tight_layout()

    output_path = "screenshots/flowgenie_architecture_diagram.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Architecture diagram saved to: {output_path}")

if __name__ == "__main__":
    generate_flowgenie_diagram()
