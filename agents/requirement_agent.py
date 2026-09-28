from __future__ import annotations

import json
import os
import re
from typing import Any
import requests
from dotenv import load_dotenv

from agents.logger import AgentLogger, safe_int
from memory.store import SharedMemory

load_dotenv()


class RequirementAnalysisAgent:
    """1. Requirement Analysis Agent: Analyzes natural-language briefs using Groq LLM with heuristic fallback."""

    def __init__(self, memory: SharedMemory | None = None):
        self.memory = memory or SharedMemory()
        self.agent_name = "Requirement Analyst Agent"
        self.groq_api_key = os.getenv("GROQ_API_KEY")

    def _call_groq(self, prompt: str) -> dict[str, Any] | None:
        if not self.groq_api_key:
            return None
        try:
            system_prompt = (
                "You are an expert AI Event Planning Requirements Analyst. "
                "Analyze the user's event brief and output a valid JSON object only with keys: "
                "event_type (e.g. Wedding, Birthday, Corporate, Anniversary, Conference), "
                "guest_count (integer), location (string), date (YYYY-MM-DD or string), "
                "budget (integer in INR), preferences (object with cuisine, decor_style, vibe, notes), "
                "and reasoning (brief sentence on how requirements were deduced)."
            )
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                },
                timeout=12,
            )
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
                return json.loads(content)
        except Exception:
            pass
        return None

    def _extract_custom_category(self, text: str) -> dict[str, str] | None:
        """Extracts and normalizes custom user requests from notes (e.g. rooms/stay, transport, cake, emcee)."""
        t = text.lower()
        if re.search(r"\b(room|rooms|stay|hotel|accommodation|lodging|cottage|villa|resort stay)\b", t):
            return {
                "key": "stay",
                "title": "Guest Accommodation & Rooms",
                "search_term": "guest accommodation hotel rooms",
                "type": "stay",
            }
        if re.search(r"\b(transport|shuttle|bus|cars?|vintage car|chauffeur|valet|fleet|travelers?)\b", t):
            return {
                "key": "transport",
                "title": "Guest Transport & Luxury Fleet",
                "search_term": "guest transport luxury car fleet",
                "type": "transport",
            }
        if re.search(r"\b(cake|wedding cake|pastry|bakery|patisserie|desserts?)\b", t):
            return {
                "key": "cake",
                "title": "Wedding Cake & Patisserie",
                "search_term": "custom wedding cake designer patisserie",
                "type": "cake",
            }
        if re.search(r"\b(emcee|anchor|mc|host|anchoring|moderator)\b", t):
            return {
                "key": "emcee",
                "title": "Anchor & Event Emcee",
                "search_term": "event emcee anchor host",
                "type": "emcee",
            }
        if re.search(r"\b(mehendi|henna|mehndi)\b", t):
            return {
                "key": "mehendi",
                "title": "Mehendi & Henna Artistry",
                "search_term": "bridal mehendi henna artist",
                "type": "mehendi",
            }
        if re.search(r"\b(return gifts?|favors?|hampers?|welcome kits?|gift box(?:es)?)\b", t):
            return {
                "key": "favors",
                "title": "Luxury Favors & Gift Hampers",
                "search_term": "luxury event return gifts hampers",
                "type": "favors",
            }
        if re.search(r"\b(invitations?|invites?|wedding cards?|stationery)\b", t):
            return {
                "key": "invites",
                "title": "Invitations & Custom Stationery",
                "search_term": "custom wedding invitations stationery",
                "type": "invites",
            }
        if re.search(r"\b(drone show|fireworks|pyro(?:technics)?|cold pyro|sparklers?)\b", t):
            return {
                "key": "pyro",
                "title": "Drone Show & Special FX",
                "search_term": "event drone show pyrotechnics special fx",
                "type": "pyro",
            }

        # Check for arbitrary custom requirement phrases
        req_match = re.search(r"(?:want|need|looking for|require|add|special requirement:?)\s+([a-zA-Z0-9\s&,]{3,30})(?:\.|$|,)", t)
        if req_match:
            raw_phrase = req_match.group(1).strip()
            clean_phrase = re.sub(r"^(?:a|an|the|some)\s+", "", raw_phrase, flags=re.IGNORECASE).strip().title()
            if len(clean_phrase) >= 3 and not re.search(r"\b(budget|guests?|bangalore|mumbai|delhi|wedding|birthday|party)\b", clean_phrase, flags=re.IGNORECASE):
                clean_key = re.sub(r"[^a-zA-Z0-9]+", "_", clean_phrase.lower()).strip("_")
                return {
                    "key": clean_key or "custom_req",
                    "title": clean_phrase,
                    "search_term": clean_phrase,
                    "type": "custom",
                }

        return None

    def _fallback_parse(self, prompt: str) -> dict[str, Any]:
        text = prompt.lower()
        guest_match = re.search(r"for\s+(\d+)\s+guests|(?:\b)(\d+)\s+guests?", text)
        budget_match = re.search(r"budget\s*(?:of)?\s*₹?\s*([0-9,]+)|(?:₹|inr)\s*([0-9,]+)", text)
        date_match = re.search(
            r"(?:on|for)\s+([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+[0-9]{4}|[a-z]+\s+[0-9]{1,2},?\s+[0-9]{4})",
            text,
        )
        location_match = re.search(r"in\s+([a-zA-Z][a-zA-Z\s]+?)(?:\s+on\s+|\s+for\s+|\s+with\s+|\s+preferences|\.|$)", text)
        event_type_match = re.search(
            r"\b(wedding|birthday|corporate|anniversary|engagement|festival|conference|product launch|party|reception)\b",
            text,
        )
        cuisine_match = re.search(
            r"\b(vegetarian|non-veg|north indian|south indian|italian|chinese|continental|multi-cuisine|vegan|seafood|bbq|rajasthani|none)\b",
            text,
        )
        decor_match = re.search(
            r"\b(none|modern|classic|royal|traditional|bohemian|minimal|floral|garden|luxury|elegant|vintage|rustic)\b",
            text,
        )

        decor_value = decor_match.group(1).title() if decor_match else "Modern"
        if "no decor" in text or ("none" in text and "decor" in text):
            decor_value = "None"

        custom_cat = self._extract_custom_category(prompt)
        custom_reason = f" Tailored custom category: {custom_cat['title']}." if custom_cat else ""

        return {
            "event_type": event_type_match.group(1).title() if event_type_match else "Wedding",
            "guest_count": safe_int(guest_match.group(1) if guest_match and guest_match.group(1) else (guest_match.group(2) if guest_match else 50), 50),
            "location": location_match.group(1).strip().title() if location_match else "Bangalore",
            "date": date_match.group(1).strip() if date_match else "2026-12-15",
            "budget": safe_int((budget_match.group(1) or budget_match.group(2) or "150000").replace(",", "") if budget_match else "150000", 150000),
            "custom_category": custom_cat,
            "preferences": {
                "cuisine": cuisine_match.group(1).title() if cuisine_match else "Multi-Cuisine",
                "decor_style": decor_value,
                "vibe": "Celebratory & Elegant",
                "custom_category": custom_cat,
            },
            "reasoning": f"Extracted key parameters.{custom_reason}",
        }

    def run(self, prompt: str) -> tuple[dict[str, Any], dict[str, str]]:
        llm_result = self._call_groq(prompt)
        used_llm = llm_result is not None
        reqs = llm_result or self._fallback_parse(prompt)
        reqs["source_prompt"] = prompt

        if not reqs.get("custom_category"):
            reqs["custom_category"] = self._extract_custom_category(prompt)
        if reqs.get("custom_category"):
            reqs.setdefault("preferences", {})["custom_category"] = reqs["custom_category"]

        custom_cat_info = reqs.get("custom_category")
        custom_thought = f" Identified custom category: {custom_cat_info['title']}." if custom_cat_info else ""
        custom_summary = f" | Custom: {custom_cat_info['title']}" if custom_cat_info else ""

        log = AgentLogger.create_log(
            agent_name=self.agent_name,
            step="Requirement Analysis",
            thought=f"Analyzing brief for '{reqs.get('event_type')}' event in {reqs.get('location')}. Using {'Groq Llama 3 LLM' if used_llm else 'Heuristic Parser'}.{custom_thought}",
            action="Parsed guest count, budget limits, location, aesthetic preferences, and custom requirements.",
            result_summary=f"Event: {reqs.get('event_type')} | Guests: {reqs.get('guest_count')} | Budget: INR {reqs.get('budget'):,} | Location: {reqs.get('location')}{custom_summary}",
        )
        self.memory.set("requirement_analysis", reqs)
        return reqs, log


__all__ = ["RequirementAnalysisAgent"]
