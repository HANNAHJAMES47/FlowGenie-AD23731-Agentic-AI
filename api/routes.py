from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from agents.event_agents import AgentLogger
from memory.store import memory
from workflow.graph import EventWorkflowEngine

router = APIRouter()
engine = EventWorkflowEngine()


def _get_event(event_id: str) -> dict[str, Any] | None:
    return memory.get(f"event:{event_id}")


@router.post("/pipeline/auto-execute")
async def auto_execute_pipeline(payload: dict[str, Any]) -> dict[str, Any]:
    """Runs the full 5-agent pipeline end-to-end automatically in a single execution flow."""
    prompt = payload.get("prompt")
    preferences = payload.get("preferences", {})
    custom_notes = payload.get("custom_notes") or preferences.get("custom_notes") or payload.get("notes") or preferences.get("notes") or ""

    if not prompt:
        event_type = payload.get("event_type", "Wedding")
        guest_count = payload.get("guest_count", 50)
        location = payload.get("location", "Bangalore")
        event_date = payload.get("date") or payload.get("event_date") or "2026-12-15"
        budget = payload.get("budget", 150000)
        cuisine = preferences.get("cuisine") or payload.get("cuisine", "Multi-Cuisine")
        decor = preferences.get("decor_style") or payload.get("decor_style", "Modern")
        prompt = (
            f"Plan a {event_type} for {guest_count} guests in {location} on {event_date} "
            f"with a budget of INR {budget}. Preferences: {cuisine} cuisine, {decor} decor style."
            + (f" Special custom requirements: {custom_notes}." if custom_notes else "")
        )
    elif custom_notes and custom_notes.lower() not in prompt.lower():
        prompt = f"{prompt.rstrip('. ')}. Special requirement: {custom_notes}."

    pipeline_result = await engine.run_full_pipeline(prompt, auto_approve=True)
    return {
        "event_id": pipeline_result["event_id"],
        "status": "booked",
        "pipeline_completed": True,
        "requirements": pipeline_result["requirements"],
        "budget_plan": pipeline_result["budget_plan"],
        "curated_package": pipeline_result["curated_package"],
        "recommendations": pipeline_result["recommendations"],
        "booking_summary": {
            "selected": pipeline_result["curated_package"],
            "total_spend": pipeline_result["booking_data"]["total_spend"],
            "budget_remaining": pipeline_result["booking_data"]["budget_remaining"],
        },
        "run_of_show": pipeline_result["run_of_show"],
        "agent_logs": pipeline_result["agent_logs"],
        "message": "Full 5-Agent automated pipeline executed successfully from requirement analysis to booking and schedule generation.",
    }


@router.post("/plan")
async def plan_event(payload: dict[str, Any]) -> dict[str, Any]:
    prompt = payload.get("prompt")
    preferences = payload.get("preferences", {})
    event_time_slot = payload.get("event_time_slot") or preferences.get("event_time_slot") or "Evening / Night (5:00 PM - 11:30 PM)"
    event_start_time = payload.get("event_start_time") or preferences.get("event_start_time") or "06:00 PM"
    catering_meal_slot = payload.get("catering_meal_slot") or preferences.get("catering_meal_slot") or "Night (Dinner Buffet / Reception Banquet)"
    custom_notes = payload.get("custom_notes") or preferences.get("custom_notes") or payload.get("notes") or preferences.get("notes") or ""

    if not prompt:
        event_type = payload.get("event_type", "Wedding")
        guest_count = payload.get("guest_count", 50)
        location = payload.get("location", "Bangalore")
        event_date = payload.get("date") or payload.get("event_date") or "2026-12-15"
        budget = payload.get("budget", 150000)
        cuisine = preferences.get("cuisine") or payload.get("cuisine", "Multi-Cuisine")
        decor = preferences.get("decor_style") or payload.get("decor_style", "Modern")
        prompt = (
            f"Plan a {event_type} for {guest_count} guests in {location} on {event_date} "
            f"({event_time_slot}, starting at {event_start_time}) with a budget of INR {budget}. "
            f"Catering: {catering_meal_slot} with {cuisine} cuisine. Decor: {decor} style."
            + (f" Special custom requirements: {custom_notes}." if custom_notes else "")
        )
    elif custom_notes and custom_notes.lower() not in prompt.lower():
        prompt = f"{prompt.rstrip('. ')}. Special requirement: {custom_notes}."

    # 1 & 2. Run Requirement Analyst & Budget Strategist Agents
    requirements_data = await engine.run_requirement_and_budget(prompt)
    requirements = requirements_data["requirements"]
    requirements["event_time_slot"] = event_time_slot
    requirements["event_start_time"] = event_start_time
    requirements["catering_meal_slot"] = catering_meal_slot
    requirements["custom_notes"] = custom_notes
    requirements.setdefault("preferences", {})["event_time_slot"] = event_time_slot
    requirements["preferences"]["event_start_time"] = event_start_time
    requirements["preferences"]["catering_meal_slot"] = catering_meal_slot
    requirements["preferences"]["custom_notes"] = custom_notes
    if "cuisine" in preferences:
        requirements["preferences"]["cuisine"] = preferences["cuisine"]
    if "decor_style" in preferences:
        requirements["preferences"]["decor_style"] = preferences["decor_style"]

    budget_plan = requirements_data["budget_plan"]
    agent_logs = list(requirements_data.get("agent_logs", []))

    # 3. Run Autonomous Vendor Discovery Agents (Parallel)
    vendor_results = await engine.run_vendor_search(requirements, budget_plan)
    categories = list(vendor_results.keys())
    search_log = AgentLogger.create_log(
        agent_name="Autonomous Vendor Discovery Agents",
        step="Vendor Sourcing & Parallel Exploration",
        thought=f"Searched top-rated suppliers across {len(categories)} categories in {requirements.get('location', 'Bangalore')} with full service inclusions and photos.",
        action=f"Discovered {sum(len(v) for v in vendor_results.values())} candidate vendor packages.",
        result_summary=f"Sourced {', '.join(categories)} vendor options matching budget parameters.",
    )
    agent_logs.append(search_log)

    # 4. Run Recommendation & Ranking Agent
    recommendations, agg_log = await engine.run_aggregation(vendor_results)
    agent_logs.append(agg_log)

    initial_run_of_show = engine.booking_monitor_agent._generate_run_of_show(
        requirements.get("event_type", "Wedding"),
        requirements.get("preferences", {}),
    )

    event_id = payload.get("event_id") or f"evt_{uuid.uuid4().hex[:8]}"
    event_state = {
        "event_id": event_id,
        "status": "waiting_for_approval",
        "requirements": requirements,
        "budget_plan": budget_plan,
        "recommendations": recommendations,
        "run_of_show": initial_run_of_show,
        "agent_logs": agent_logs,
        "approval_required": True,
        "approved": False,
        "timeline": [
            {"step": "requirements_analyzed", "complete": True},
            {"step": "budget_allocated", "complete": True},
            {"step": "vendors_shortlisted", "complete": True},
            {"step": "approved_by_user", "complete": False},
            {"step": "booking_confirmed", "complete": False},
        ],
    }
    memory.set(f"event:{event_id}", event_state)
    memory.set("current_event", event_state)

    return {
        "event_id": event_id,
        "status": "waiting_for_approval",
        "summary": {
            "event_type": requirements["event_type"],
            "guest_count": requirements["guest_count"],
            "location": requirements["location"],
            "date": requirements["date"],
            "budget": budget_plan["total_budget"],
            "preferences": requirements.get("preferences", {}),
        },
        "budget_plan": budget_plan,
        "recommendations": recommendations,
        "run_of_show": initial_run_of_show,
        "agent_logs": agent_logs,
        "approval_required": True,
    }


@router.post("/approve")
async def approve_event(payload: dict[str, Any]) -> dict[str, Any]:
    event_id = payload.get("event_id")
    decision = payload.get("decision", "approve").lower()
    approved = payload.get("approved_vendors", [])

    if not event_id:
        raise HTTPException(status_code=400, detail="event_id is required.")

    event_state = _get_event(event_id)
    if not event_state:
        raise HTTPException(status_code=404, detail="Event not found.")

    if decision == "reject":
        event_state["status"] = "rejected"
        event_state["approval_required"] = False
        memory.set(f"event:{event_id}", event_state)
        return {"event_id": event_id, "status": "rejected", "message": "Booking was rejected by the user."}

    if not approved:
        recs = event_state.get("recommendations", {})
        for cat_vendors in recs.values():
            if cat_vendors:
                approved.append(cat_vendors[0])

    custom_run_of_show = payload.get("run_of_show")

    # 5. Run Booking & Contingency Agent
    booking_data, booking_log = await engine.run_booking(
        approved_vendors=approved,
        event_id=event_id,
        requirements=event_state.get("requirements"),
        budget_plan=event_state.get("budget_plan"),
        custom_run_of_show=custom_run_of_show,
    )
    monitoring_data = await engine.run_monitoring(event_id, booking_data)

    event_state["status"] = "booked"
    event_state["approved"] = True
    event_state["approval_required"] = False
    event_state["booking_data"] = booking_data
    event_state["monitoring_data"] = monitoring_data
    event_state["run_of_show"] = booking_data.get("run_of_show", [])
    event_state.setdefault("agent_logs", []).append(booking_log)
    event_state["timeline"] = [
        {"step": "requirements_analyzed", "complete": True},
        {"step": "budget_allocated", "complete": True},
        {"step": "vendors_shortlisted", "complete": True},
        {"step": "approved_by_user", "complete": True},
        {"step": "booking_confirmed", "complete": True},
    ]

    memory.set(f"event:{event_id}", event_state)
    memory.set("current_event", event_state)

    return {
        "event_id": event_id,
        "status": "booked",
        "booking_summary": {
            "selected": approved,
            "total_spend": booking_data["total_spend"],
            "budget_remaining": booking_data["budget_remaining"],
        },
        "run_of_show": booking_data.get("run_of_show", []),
        "agent_log": booking_log,
        "message": "Booking confirmed after human approval. Run-of-show schedule generated.",
    }


@router.post("/schedule/update")
async def update_schedule(payload: dict[str, Any]) -> dict[str, Any]:
    """Updates the custom hour-by-hour run-of-show timeline schedule."""
    event_id = payload.get("event_id")
    run_of_show = payload.get("run_of_show", [])
    if not event_id:
        raise HTTPException(status_code=400, detail="event_id is required.")

    event_state = _get_event(event_id)
    if not event_state:
        event_state = memory.get("current_event", {})

    event_state.setdefault("booking_data", {})["run_of_show"] = run_of_show
    if "monitoring_data" in event_state and isinstance(event_state["monitoring_data"], dict):
        event_state["monitoring_data"]["run_of_show"] = run_of_show
    event_state["run_of_show"] = run_of_show

    memory.set(f"event:{event_id}", event_state)
    memory.set("current_event", event_state)

    return {
        "event_id": event_id,
        "status": "updated",
        "run_of_show": run_of_show,
        "message": f"Successfully updated event schedule with {len(run_of_show)} custom milestones.",
    }


@router.get("/schedule/presets")
async def get_schedule_presets() -> dict[str, Any]:
    """Provides authentic cultural tradition presets for 1-click timeline generation."""
    return {
        "south_indian": {
            "name": "🪔 South Indian Muhurtham & Kalyanam",
            "milestones": [
                {"time": "06:30 AM", "title": "Mandap Setup & Floral Kolam", "description": "Traditional floral garlands, rangoli kolam, and nadaswaram musicians arrive.", "category": "decor"},
                {"time": "07:30 AM", "title": "Ganesh & Kashi Yatra Pooja", "description": "Family rituals, mangala snanam, and pre-muhurtham blessings.", "category": "ceremony"},
                {"time": "09:00 AM", "title": "Auspicious Muhurtham & Sapthapadi", "description": "Tying of the Mangalsutra, 7 sacred steps around the holy fire, and floral shower.", "category": "ceremony"},
                {"time": "11:30 AM", "title": "Traditional Banana Leaf Kalyana Feast", "description": "Authentic multi-course vegetarian lunch feast with live payasam service.", "category": "catering"},
                {"time": "03:00 PM", "title": "Post-Ceremony Games & Family Portraits", "description": "Traditional coconut games, ring finding, and candid bridal portraits.", "category": "photography"},
                {"time": "06:30 PM", "title": "Evening Reception & Carnatic Fusion", "description": "Stage greetings, photo line, acoustic music, and buffet dinner.", "category": "entertainment"},
            ],
        },
        "sangeet_north": {
            "name": "💃 Sangeet, Baraat & Royal Reception",
            "milestones": [
                {"time": "10:00 AM", "title": "Mehendi & Floral Jewelry Session", "description": "Bridal henna artists, folk singing, and colorful marigold cabana setup.", "category": "makeup"},
                {"time": "04:30 PM", "title": "Grand Baraat Procession with Dhol", "description": "Groom arrival with brass band, live dhol beats, and Milni welcome ceremony.", "category": "entertainment"},
                {"time": "06:00 PM", "title": "Jaimala (Varmala) Stage Exchange", "description": "Rose petal blast, stage garland exchange, and golden hour family photos.", "category": "ceremony"},
                {"time": "07:00 PM", "title": "Sangeet Dance Performances & DJ", "description": "Choreographed family dance showdown, cocktail snacks, and LED stage.", "category": "entertainment"},
                {"time": "08:30 PM", "title": "Mughlai & Royal Dinner Buffet", "description": "Live tandoor, chaat counters, biryani pots, and dessert spread.", "category": "catering"},
                {"time": "10:30 PM", "title": "Sacred Pheras & Vidaai Ceremony", "description": "Late evening Vedic pheras followed by emotional family send-off.", "category": "ceremony"},
            ],
        },
        "christian_wedding": {
            "name": "⛪ Church Ceremony & Evening Reception",
            "milestones": [
                {"time": "11:00 AM", "title": "Bridal Dressing & First Look", "description": "Hair styling, veil setting, and bridal party first-look portraits.", "category": "makeup"},
                {"time": "03:30 PM", "title": "Church Nuptial Mass & Vows", "description": "Bridal entrance, exchange of wedding rings, solemn vows, and choir music.", "category": "ceremony"},
                {"time": "05:30 PM", "title": "Cocktail Hour & Passed Canapés", "description": "Welcome mocktails, canapés, and sunset acoustic string duo.", "category": "catering"},
                {"time": "06:45 PM", "title": "Grand Entrance, Toasts & First Dance", "description": "Couple entrance, speeches, and first dance.", "category": "entertainment"},
                {"time": "07:45 PM", "title": "Multi-Course Gala Dinner & Cake Cutting", "description": "Tiered wedding cake cutting and sit-down dining experience.", "category": "catering"},
                {"time": "09:30 PM", "title": "Open Dance Floor & Sparkler Send-off", "description": "DJ party, late-night bites, and sparkler illuminated exit.", "category": "entertainment"},
            ],
        },
        "birthday_party": {
            "name": "🎂 Birthday & Milestone Celebration",
            "milestones": [
                {"time": "02:00 PM", "title": "Venue Access & Balloon Decor Setup", "description": "Balloon arch installation, customized stage backdrop, and LED lighting.", "category": "decor"},
                {"time": "04:30 PM", "title": "Live Chaat & Mocktail Bar Active", "description": "Live chaat, slider stations, signature drinks, and finger foods.", "category": "catering"},
                {"time": "05:00 PM", "title": "Guests Arrival & Photo Booth", "description": "Photo booth with instant props, red carpet backdrop, and ambient music.", "category": "photography"},
                {"time": "06:30 PM", "title": "Cake Cutting & Spotlight Toasts", "description": "Celebration fanfare, singing, confetti poppers, and sparkling toast.", "category": "entertainment"},
                {"time": "07:30 PM", "title": "Gourmet Dinner Buffet & Live DJ", "description": "Hot buffet dining, interactive games, and high-energy dance floor.", "category": "catering"},
                {"time": "10:00 PM", "title": "Return Gifts & Celebration Sign-off", "description": "Favor distribution, memorable group portraits, and wrap-up.", "category": "venue"},
            ],
        },
        "corporate_gala": {
            "name": "💼 Corporate Gala & Keynote Summit",
            "milestones": [
                {"time": "08:00 AM", "title": "AV & Stage Tech Check", "description": "Microphone testing, 4K projector calibration, and registration desk setup.", "category": "venue"},
                {"time": "09:30 AM", "title": "Delegate Arrival & Networking Breakfast", "description": "Fresh brew coffee/tea, pastries, and smart badge check-in.", "category": "catering"},
                {"time": "10:30 AM", "title": "Keynote Address & Product Unveiling", "description": "Executive keynote, visual keynote deck, and livestream broadcast.", "category": "entertainment"},
                {"time": "01:00 PM", "title": "Executive Networking Lunch", "description": "Curated lunch buffet and B2B breakout lounge access.", "category": "catering"},
                {"time": "02:30 PM", "title": "Panel Discussions & Interactive Q&A", "description": "Industry expert panel, roving mic Q&A, and audience polls.", "category": "venue"},
                {"time": "05:00 PM", "title": "High Tea, Awards & Closing Remarks", "description": "Felicitation ceremony, high tea refreshments, and departure.", "category": "catering"},
            ],
        },
    }


@router.get("/status/{event_id}")
async def get_status(event_id: str) -> dict[str, Any]:
    event_state = _get_event(event_id)
    if not event_state:
        return {
            "event_id": event_id,
            "status": "idle",
            "timeline": [],
            "run_of_show": [],
            "alert": None,
            "booked_vendors": [],
        }

    booking_data = event_state.get("booking_data", {})
    monitoring_data = event_state.get("monitoring_data") or {
        "event_id": event_id,
        "status": event_state.get("status", "waiting_for_approval"),
        "timeline": event_state.get("timeline", []),
        "run_of_show": booking_data.get("run_of_show", []),
        "alert": None,
        "backup_suggestions": [],
    }

    return {
        "event_id": event_id,
        "status": monitoring_data.get("status", event_state.get("status", "waiting_for_approval")),
        "timeline": monitoring_data.get("timeline", event_state.get("timeline", [])),
        "run_of_show": monitoring_data.get("run_of_show", booking_data.get("run_of_show", [])),
        "alert": monitoring_data.get("alert"),
        "backup_suggestions": monitoring_data.get("backup_suggestions", []),
        "booked_vendors": booking_data.get("approved_vendors", []),
        "total_spend": booking_data.get("total_spend", 0),
        "budget_remaining": booking_data.get("budget_remaining", 0),
        "agent_logs": event_state.get("agent_logs", []),
    }


@router.post("/replan")
async def replan_event(payload: dict[str, Any]) -> dict[str, Any]:
    event_id = payload.get("event_id")
    category = payload.get("category", "catering")
    if not event_id:
        raise HTTPException(status_code=400, detail="event_id is required.")

    replan_data, replan_log = await engine.replan_category(event_id, category)
    event_state = _get_event(event_id) or {}
    event_state["status"] = "replan_triggered"
    event_state["replan"] = replan_data
    event_state.setdefault("agent_logs", []).append(replan_log)
    memory.set(f"event:{event_id}", event_state)

    return {
        "event_id": event_id,
        "status": "replan_triggered",
        "category": category,
        "alert": replan_data.get("alert"),
        "message": f"Contingency Agent initiated recovery search for '{category}'. Replacement options ready.",
        "recommendations": replan_data.get("recommendations", {}),
        "agent_log": replan_log,
    }


# ============================================================================
# OPTION 4: AUTOMATED WHATSAPP & EMAIL NOTIFICATION DISPATCH
# ============================================================================

@router.post("/notify/preview")
async def preview_notifications(payload: dict[str, Any]) -> dict[str, Any]:
    """Generates preview RFPs and WhatsApp dispatch links for all booked vendors and client."""
    from agents.notification_agent import NotificationAgent

    event_id = payload.get("event_id")
    event_state = _get_event(event_id) if event_id else None
    if not event_state:
        # Fallback to current event or mock
        event_state = memory.get("current_event") or {}

    requirements = event_state.get("requirements", payload.get("requirements", {}))
    booking_data = event_state.get("booking_data", {})
    booked_vendors = booking_data.get("approved_vendors", payload.get("booked_vendors", []))
    run_of_show = booking_data.get("run_of_show", event_state.get("run_of_show", []))

    notifier = NotificationAgent()
    vendor_rfps = [
        notifier.generate_vendor_rfp(vendor, requirements)
        for vendor in booked_vendors
    ]
    client_summary = notifier.generate_client_summary(requirements, booked_vendors, run_of_show)

    return {
        "event_id": event_id,
        "vendor_rfps": vendor_rfps,
        "client_summary": client_summary,
        "total_vendors": len(vendor_rfps),
    }


@router.post("/notify/dispatch-all")
async def dispatch_all_notifications(payload: dict[str, Any]) -> dict[str, Any]:
    """Dispatches email notifications and generates instant WhatsApp launch links."""
    from agents.notification_agent import NotificationAgent

    event_id = payload.get("event_id")
    event_state = _get_event(event_id) if event_id else None
    if not event_state:
        event_state = memory.get("current_event") or {}

    requirements = event_state.get("requirements", payload.get("requirements", {}))
    booking_data = event_state.get("booking_data", {})
    booked_vendors = booking_data.get("approved_vendors", payload.get("booked_vendors", []))
    run_of_show = booking_data.get("run_of_show", event_state.get("run_of_show", []))
    client_email = payload.get("client_email") or requirements.get("user_email", "client@example.com")

    notifier = NotificationAgent()
    vendor_rfps = [
        notifier.generate_vendor_rfp(vendor, requirements)
        for vendor in booked_vendors
    ]
    client_summary = notifier.generate_client_summary(requirements, booked_vendors, run_of_show)

    # Dispatch email if client email provided
    email_sent = notifier.dispatch_email(
        to_email=client_email,
        subject=f"Confirmed Event Itinerary: {requirements.get('event_type', 'Event')} in {requirements.get('location', 'Bangalore')}",
        body_text=client_summary["message"],
    )

    return {
        "event_id": event_id,
        "dispatched": True,
        "email_sent": email_sent,
        "client_email": client_email,
        "vendor_rfps": vendor_rfps,
        "client_summary": client_summary,
        "message": f"Successfully prepared {len(vendor_rfps)} supplier RFPs and sent confirmation to {client_email}.",
    }


# ============================================================================
# OPTION 3: AUTONOMOUS BACKGROUND SENTINEL WATCHDOG
# ============================================================================

@router.post("/sentinel/watchdog/toggle")
async def toggle_sentinel_watchdog(payload: dict[str, Any]) -> dict[str, Any]:
    """Enables or disables autonomous background health monitoring."""
    from agents.sentinel_agent import SentinelWatchdog

    event_id = payload.get("event_id", "evt_default")
    enable = payload.get("enable", True)
    watchdog = SentinelWatchdog()
    active = watchdog.set_watchdog_active(event_id, enable)

    return {
        "event_id": event_id,
        "watchdog_active": active,
        "message": f"Sentinel Auto-Pilot Watchdog {'Activated' if active else 'Deactivated'}.",
    }


@router.get("/sentinel/audit-log/{event_id}")
async def get_sentinel_audit_log(event_id: str) -> dict[str, Any]:
    """Returns autonomous sentinel incident detection and recovery audit logs."""
    from agents.sentinel_agent import SentinelWatchdog

    watchdog = SentinelWatchdog()
    logs = watchdog.get_event_audit_log(event_id)
    active = watchdog.is_watchdog_active(event_id)

    return {
        "event_id": event_id,
        "watchdog_active": active,
        "total_incidents": len(logs),
        "audit_logs": logs,
    }


@router.post("/sentinel/auto-recover")
async def sentinel_auto_recover(payload: dict[str, Any]) -> dict[str, Any]:
    """Simulates an autonomous background incident and performs instant self-healing recovery."""
    from agents.sentinel_agent import SentinelWatchdog

    event_id = payload.get("event_id")
    category = payload.get("category", "catering")
    reason = payload.get("reason", "Supplier unresponsiveness detected by Sentinel Watchdog")

    if not event_id:
        raise HTTPException(status_code=400, detail="event_id is required.")

    watchdog = SentinelWatchdog()
    result = await watchdog.auto_recover_vendor(event_id, category, reason)
    logs = watchdog.get_event_audit_log(event_id)

    return {
        "event_id": event_id,
        "recovery_result": result,
        "latest_audit_logs": logs,
        "message": f"Sentinel autonomously resolved '{category}' supplier incident and updated contract.",
    }


# ==============================================================================
# User Authentication & Account Management Endpoints
# ==============================================================================

@router.post("/auth/signup")
async def auth_signup(payload: dict[str, Any]) -> dict[str, Any]:
    """Register a new user account with unique email validation and session creation."""
    from agents.auth_agent import auth_manager

    name = payload.get("name", "")
    email = payload.get("email", "")
    phone = payload.get("phone", "")
    password = payload.get("password", "")
    role = payload.get("role", "Host / Planner")

    try:
        result = auth_manager.register_user(
            name=name,
            email=email,
            phone=phone,
            password=password,
            role=role,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Account registration failed.")


@router.post("/auth/login")
async def auth_login(payload: dict[str, Any]) -> dict[str, Any]:
    """Authenticate user with email/phone and password."""
    from agents.auth_agent import auth_manager

    email_or_phone = payload.get("email_or_phone") or payload.get("email", "")
    password = payload.get("password", "")

    try:
        result = auth_manager.authenticate_user(
            email_or_phone=email_or_phone,
            password=password,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Sign in failed.")


@router.post("/auth/demo-login")
async def auth_demo_login() -> dict[str, Any]:
    """Instant 1-click login with pre-configured VIP planner demo profile."""
    from agents.auth_agent import auth_manager

    try:
        result = auth_manager.demo_login()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Demo sign in failed.")


@router.get("/auth/me")
async def auth_get_me(token: str | None = None) -> dict[str, Any]:
    """Fetch profile and past event history for the authenticated session."""
    from agents.auth_agent import auth_manager

    if not token:
        raise HTTPException(status_code=401, detail="Authentication token required.")

    user = auth_manager.get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Session expired or invalid. Please sign in again.")

    return {
        "authenticated": True,
        "user": user,
    }


@router.post("/auth/logout")
async def auth_logout(payload: dict[str, Any]) -> dict[str, Any]:
    """Terminate user session."""
    from agents.auth_agent import auth_manager

    token = payload.get("token", "")
    auth_manager.logout_user(token)
    return {
        "authenticated": False,
        "message": "Signed out successfully.",
    }


@router.get("/evaluation")
@router.get("/metrics")
async def get_evaluation_metrics() -> dict[str, Any]:
    """Retrieve the multi-agent academic evaluation metrics benchmark report."""
    import json
    from pathlib import Path

    report_path = Path(__file__).resolve().parent.parent / "evaluation_report.json"
    if not report_path.exists():
        from evaluate_agents import FlowGenieAgentEvaluator
        evaluator = FlowGenieAgentEvaluator()
        return evaluator.run_all()

    try:
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load evaluation report: {str(e)}")



