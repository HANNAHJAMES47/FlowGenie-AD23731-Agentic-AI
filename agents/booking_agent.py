from __future__ import annotations

from typing import Any
from agents.logger import AgentLogger
from agents.ranking_agent import RecommendationAggregatorAgent
from agents.vendor_agent import VendorSearchAgent
from memory.store import SharedMemory


class BookingMonitoringAgent:
    """5. Booking & Contingency Agent: Runs booking confirmations, run-of-show timeline, and cancellation replanning."""

    def __init__(self, memory: SharedMemory | None = None):
        self.memory = memory or SharedMemory()
        self.agent_name = "Booking & Contingency Agent"

    def _generate_run_of_show(
        self,
        event_type: str,
        preferences: dict[str, Any] | None = None,
    ) -> list[dict[str, str]]:
        """Builds a tailored event-day schedule based on event type, regional customs, and traditions."""
        event_key = (event_type or "").lower()
        prefs = preferences or {}
        cuisine = (prefs.get("cuisine") or "").lower()
        decor = (prefs.get("decor_style") or "").lower()
        customs = (prefs.get("customs") or "").lower()
        meal_slot = (prefs.get("catering_meal_slot") or "").lower()
        time_slot = (prefs.get("event_time_slot") or "").lower()
        start_time = prefs.get("event_start_time") or "06:00 PM"
        combined_text = f"{event_key} {cuisine} {decor} {customs} {meal_slot} {time_slot}"

        if "south indian" in combined_text or "muhurtham" in combined_text or "kannada" in combined_text or "tamil" in combined_text or "telugu" in combined_text:
            return [
                {"time": "06:30 AM", "title": "Mandap Setup & Floral Decoration", "description": "Traditional flower garlands, kolam / rangoli, and nadaswaram musicians arrive.", "category": "decor"},
                {"time": "07:30 AM", "title": "Ganesh & Kashi Yatra Pooja", "description": "Family rituals, mangala snanam, and pre-muhurtham blessings.", "category": "ceremony"},
                {"time": "08:00 AM", "title": "Traditional South Indian Morning Breakfast / Tiffin (Morning)", "description": "Hot idlis, medu vadas, filter coffee bar, and fresh chutneys.", "category": "catering"},
                {"time": "09:00 AM", "title": "Auspicious Muhurtham & Sapthapadi", "description": "Tying of the Mangalsutra, 7 sacred steps around the holy fire, and floral shower.", "category": "ceremony"},
                {"time": "11:30 AM", "title": "Traditional Banana Leaf Kalyana Feast (Lunch / Afternoon)", "description": "Authentic multi-course vegetarian lunch feast with live payasam service.", "category": "catering"},
                {"time": "03:00 PM", "title": "Post-Ceremony Games & Family Portraits", "description": "Traditional coconut games, ring finding, and candid bridal portrait session.", "category": "photography"},
                {"time": "06:30 PM", "title": "Evening Reception & Live Carnatic Fusion", "description": "Stage greetings, photo line, acoustic violin/flute performance, and buffet dinner.", "category": "entertainment"},
            ]
        elif "morning" in time_slot or "morning" in meal_slot or "breakfast" in meal_slot:
            return [
                {"time": "06:30 AM", "title": "Venue Access & Morning Setup", "description": "Fresh floral arrangements, seating layout, and welcoming ambiance setup.", "category": "decor"},
                {"time": "08:00 AM", "title": "Guest Arrival & Welcome Breakfast Spread (Morning)", "description": "Hot breakfast stations, fresh juices, and specialty tea/coffee bar.", "category": "catering"},
                {"time": "09:30 AM", "title": "Main Auspicious Ceremony & Rituals", "description": "Solemn customs, stage blessings, and morning photographic portraits.", "category": "ceremony"},
                {"time": "11:30 AM", "title": "Grand Festive Brunch & High Tea", "description": "Gourmet multi-cuisine brunch counters and dessert spread.", "category": "catering"},
                {"time": "01:00 PM", "title": "Celebration Wrap & Favor Distribution", "description": "Family blessings, parting gift distribution, and event conclusion.", "category": "venue"},
            ]
        elif "afternoon" in time_slot or "afternoon" in meal_slot or "lunch" in meal_slot:
            return [
                {"time": "10:30 AM", "title": "Venue Handover & Styling Setup", "description": "Table centerpieces, stage decor, and guest reception desk preparation.", "category": "decor"},
                {"time": "12:00 PM", "title": "Guests Arrival & Welcome Mocktails", "description": "Welcome drinks, photo booth, and ambient acoustic music.", "category": "catering"},
                {"time": "01:00 PM", "title": "Grand Afternoon Lunch Feast (Afternoon)", "description": "Lavish multi-course buffet lunch with live specialty food counters.", "category": "catering"},
                {"time": "03:00 PM", "title": "Keynote Celebrations, Speeches & Games", "description": "Spotlight felicitations, stage speeches, and interactive moments.", "category": "entertainment"},
                {"time": "04:30 PM", "title": "Artisanal High Tea & Dessert Lounge", "description": "Fresh gourmet chai, pastries, savory canapés, and departures.", "category": "catering"},
            ]
        elif "sangeet" in combined_text or "north indian" in combined_text or "punjabi" in combined_text or "baraat" in combined_text or "mehendi" in combined_text:
            return [
                {"time": "10:00 AM", "title": "Mehendi & Floral Jewelry Session", "description": "Bridal henna artists, folk singing, and colorful marigold cabana setup.", "category": "makeup"},
                {"time": "04:30 PM", "title": "Grand Baraat Procession with Dhol", "description": "Groom arrival with brass band, live dhol beats, and Milni welcome ceremony.", "category": "entertainment"},
                {"time": "06:00 PM", "title": "Jaimala (Varmala) Stage Exchange", "description": "Rose petal blast, stage garland exchange, and golden hour family photos.", "category": "ceremony"},
                {"time": "07:00 PM", "title": "Sangeet Dance Performances & DJ", "description": "Choreographed family dance showdown, cocktail snacks, and LED stage.", "category": "entertainment"},
                {"time": "08:30 PM", "title": "Mughlai & Royal Dinner Buffet (Night)", "description": "Live tandoor, chaat counters, biryani pots, and dessert spread.", "category": "catering"},
                {"time": "10:30 PM", "title": "Sacred Pheras & Vidaai Ceremony", "description": "Late evening Vedic pheras followed by emotional family send-off.", "category": "ceremony"},
            ]
        elif "christian" in combined_text or "church" in combined_text or "western" in combined_text:
            return [
                {"time": "11:00 AM", "title": "Bridal Dressing & First Look", "description": "Hair styling, veil setting, and bridal party first-look portraits.", "category": "makeup"},
                {"time": "03:30 PM", "title": "Church Nuptial Mass & Vows", "description": "Bridal entrance, exchange of wedding rings, solemn vows, and choir music.", "category": "ceremony"},
                {"time": "05:30 PM", "title": "Cocktail Hour & Passed Hors d'oeuvres", "description": "Welcome mocktails, canapés, and sunset acoustic string duo.", "category": "catering"},
                {"time": "06:45 PM", "title": "Grand Entrance, Toasts & First Dance", "description": "Couple entrance, best man / maid of honor speeches, and first dance.", "category": "entertainment"},
                {"time": "07:45 PM", "title": "Multi-Course Gala Dinner (Night) & Cake Cutting", "description": "Tiered wedding cake cutting and sit-down dining experience.", "category": "catering"},
                {"time": "09:30 PM", "title": "Open Dance Floor & Sparkler Send-off", "description": "DJ party, late-night bites, and sparkler illuminated exit.", "category": "entertainment"},
            ]
        elif event_key in {"birthday", "party", "anniversary"}:
            return [
                {"time": "02:00 PM", "title": "Venue Access & Decor Setup", "description": "Balloon arch installation, customized stage backdrop, and LED lighting setup.", "category": "decor"},
                {"time": "04:30 PM", "title": "Catering Live Stations & Mocktail Bar Active", "description": "Live chaat, slider stations, signature drinks, and finger foods.", "category": "catering"},
                {"time": "05:00 PM", "title": "Guests Arrival & Welcome Photography", "description": "Photo booth with instant props, red carpet backdrop, and ambient music.", "category": "photography"},
                {"time": "06:30 PM", "title": "Cake Cutting & Spotlight Toasts", "description": "Celebration fanfare, singing, confetti poppers, and champagne/sparkling toast.", "category": "entertainment"},
                {"time": "07:30 PM", "title": "Gourmet Dinner Buffet (Night) & Live DJ", "description": "Hot buffet dining, interactive games, and high-energy dance floor.", "category": "catering"},
                {"time": "10:00 PM", "title": "Return Gifts & Celebration Sign-off", "description": "Favor distribution, memorable group portraits, and wrap-up.", "category": "venue"},
            ]
        elif event_key in {"corporate", "conference", "product launch", "seminar"}:
            return [
                {"time": "08:00 AM", "title": "AV & Stage Tech Check", "description": "Microphone testing, 4K projector calibration, and registration desk setup.", "category": "venue"},
                {"time": "09:30 AM", "title": "Delegate Arrival & Networking Breakfast (Morning)", "description": "Fresh brew coffee/tea, pastries, and smart badge check-in.", "category": "catering"},
                {"time": "10:30 AM", "title": "Keynote Address & Product Unveiling", "description": "Executive keynote, visual keynote deck, and livestream broadcast.", "category": "entertainment"},
                {"time": "01:00 PM", "title": "Executive Networking Lunch (Afternoon)", "description": "Curated lunch buffet and B2B breakout lounge access.", "category": "catering"},
                {"time": "02:30 PM", "title": "Panel Discussions & Interactive Q&A", "description": "Industry expert panel, roving mic Q&A, and audience polls.", "category": "venue"},
                {"time": "05:00 PM", "title": "High Tea, Awards & Closing Remarks", "description": "Felicitation ceremony, high tea refreshments, and departure.", "category": "catering"},
            ]
        else:  # General Wedding / Grand Celebration (Night / Evening)
            return [
                {"time": "09:00 AM", "title": "Venue Handover & Decor Setup", "description": "Floral mandap construction, guest seating layout, and stage lighting.", "category": "decor"},
                {"time": "01:00 PM", "title": "Bridal Makeup & Groom Styling", "description": "Artist session, attire coordination, and touch-up prep.", "category": "makeup"},
                {"time": "03:30 PM", "title": "Pre-Ceremony Photo & Video Shoot", "description": "Golden hour portraits with family, bridesmaids, and groomsmen.", "category": "photography"},
                {"time": "05:30 PM", "title": "Guest Welcome & Refreshments", "description": "Welcome drinks, traditional musicians, and welcome gift hampers.", "category": "catering"},
                {"time": "06:30 PM", "title": "Main Ceremony & Auspicious Rituals", "description": "Solemn customs, vows, and sacred exchange with background music.", "category": "ceremony"},
                {"time": "08:30 PM", "title": "Grand Dinner Feast (Night) & Stage Greetings", "description": "Lavish multi-cuisine buffet, live counters, and celebration photos.", "category": "catering"},
                {"time": "11:00 PM", "title": "Event Wrap & Transport Logistics", "description": "Guest send-off, transport coordination, and vendor sign-off.", "category": "venue"},
            ]

    def run_booking(
        self,
        event_id: str,
        approved_vendors: list[dict[str, Any]],
        requirements: dict[str, Any] | None = None,
        budget_plan: dict[str, Any] | None = None,
        custom_run_of_show: list[dict[str, Any]] | None = None,
    ) -> tuple[dict[str, Any], dict[str, str]]:
        total_spend = sum(float(v.get("price", 0)) for v in approved_vendors)
        reqs = requirements or self.memory.get("requirement_analysis", {})
        b_plan = budget_plan or self.memory.get("budget_plan", {})
        total_budget = b_plan.get("total_budget", 150000)
        event_type = reqs.get("event_type", "Wedding")
        preferences = reqs.get("preferences", {})

        if custom_run_of_show and len(custom_run_of_show) > 0:
            run_of_show = custom_run_of_show
        else:
            run_of_show = self._generate_run_of_show(event_type, preferences)

        booking_data = {
            "event_id": event_id,
            "status": "booked",
            "approved_vendors": approved_vendors,
            "total_spend": total_spend,
            "budget_remaining": max(total_budget - total_spend, 0),
            "run_of_show": run_of_show,
            "timeline": [
                {"step": "requirements_analyzed", "complete": True},
                {"step": "budget_allocated", "complete": True},
                {"step": "vendors_shortlisted", "complete": True},
                {"step": "approved_by_user", "complete": True},
                {"step": "booking_confirmed", "complete": True},
            ],
        }

        log = AgentLogger.create_log(
            agent_name=self.agent_name,
            step="Booking Confirmation & Run-of-Show Generation",
            thought=f"Confirmed {len(approved_vendors)} vendors for event {event_id}. Total spend: INR {total_spend:,} of INR {total_budget:,}.",
            action="Generated minute-by-minute day-of-event schedule and initialized health monitoring.",
            result_summary=f"Booking confirmed. Remaining budget: INR {booking_data['budget_remaining']:,}. Schedule: {len(run_of_show)} milestone checkpoints.",
        )
        self.memory.set(f"booking_{event_id}", booking_data)
        return booking_data, log

    def run_monitoring(self, event_id: str, booking_data: dict[str, Any]) -> dict[str, Any]:
        monitoring = {
            "event_id": event_id,
            "status": "monitoring",
            "timeline": booking_data.get("timeline", []),
            "run_of_show": booking_data.get("run_of_show", []),
            "alert": None,
            "backup_suggestions": [],
        }
        self.memory.set(f"monitoring_{event_id}", monitoring)
        return monitoring

    async def handle_cancellation(self, event_id: str, category: str, requirements: dict[str, Any], budget_slice: float) -> tuple[dict[str, Any], dict[str, str]]:
        search_agent = VendorSearchAgent(category=category, memory=self.memory)
        fresh_vendors = await search_agent.run(requirements, budget_slice)
        
        aggregator = RecommendationAggregatorAgent(memory=self.memory)
        fresh_recommendations, _ = aggregator.run({category: fresh_vendors})

        status = self.memory.get(f"monitoring_{event_id}", {})
        status["alert"] = f"[ALERT] Vendor cancellation alert received for '{category}'. The Contingency Agent has automatically searched and curated replacement vendors."
        status["status"] = "replan_triggered"
        self.memory.set(f"monitoring_{event_id}", status)

        log = AgentLogger.create_log(
            agent_name=self.agent_name,
            step=f"Emergency Recovery - {category.title()} Cancellation",
            thought=f"Detected cancellation in '{category}'. Triggered autonomous discovery agent to find immediate backup vendors within INR {budget_slice:,} budget.",
            action=f"Discovered {len(fresh_vendors)} replacement candidates and ranked top recommendations.",
            result_summary=f"Replacement vendors ready for instant 1-click confirmation in {category.title()}.",
        )

        return {
            "event_id": event_id,
            "status": "replan_triggered",
            "category": category,
            "recommendations": fresh_recommendations,
            "alert": status["alert"],
        }, log


ContingencyReplanner = BookingMonitoringAgent

__all__ = ["BookingMonitoringAgent", "ContingencyReplanner"]
