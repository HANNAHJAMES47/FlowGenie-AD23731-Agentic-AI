import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_timing_and_catering_slots():
    print("Testing: Event Timing & Catering Meal Slot System...")

    # Test 1: Morning Event with Breakfast Catering
    morning_payload = {
        "event_type": "Wedding Pooja",
        "guest_count": 100,
        "location": "Bangalore",
        "date": "2026-11-20",
        "budget": 300000,
        "event_time_slot": "Morning (8:00 AM - 1:00 PM)",
        "event_start_time": "08:00 AM",
        "catering_meal_slot": "Morning (Breakfast / Brunch / Morning Pooja)",
        "preferences": {
            "cuisine": "Traditional South Indian",
            "decor_style": "Traditional Floral",
            "event_time_slot": "Morning (8:00 AM - 1:00 PM)",
            "event_start_time": "08:00 AM",
            "catering_meal_slot": "Morning (Breakfast / Brunch / Morning Pooja)",
        },
    }
    response = client.post("/plan", json=morning_payload)
    assert response.status_code == 200
    data = response.json()
    event_id = data["event_id"]
    assert event_id is not None
    print("  [OK] Morning event planned successfully.")

    # Approve and check generated run-of-show
    top_vendors = [v[0] for v in data["recommendations"].values() if v]
    approve_payload = {
        "event_id": event_id,
        "decision": "approve",
        "approved_vendors": top_vendors,
    }
    response = client.post("/approve", json=approve_payload)
    assert response.status_code == 200
    approve_data = response.json()
    ros = approve_data.get("run_of_show", [])
    assert len(ros) > 0
    # Check that morning breakfast is included
    has_morning_meal = any(
        "breakfast" in m["title"].lower()
        or "brunch" in m["title"].lower()
        or "morning" in m["title"].lower()
        for m in ros
    )
    assert has_morning_meal, "Schedule did not include morning meal!"
    print("  [OK] Hour-by-Hour schedule properly generated with Morning Breakfast checkpoints.")

    # Check WhatsApp RFP Preview contains timing
    response = client.post("/notify/preview", json={"event_id": event_id})
    assert response.status_code == 200
    preview_data = response.json()
    briefs = preview_data.get("vendor_rfps", [])
    assert len(briefs) > 0
    catering_brief = next((b for b in briefs if b["category"].lower() == "catering"), None)
    assert catering_brief is not None
    assert "Meal Service Timing: Morning" in catering_brief["message"]
    print("  [OK] WhatsApp brief for caterer explicitly states: Meal Service Timing: Morning.")

    # Test 2: Afternoon Event with Lunch Feast
    afternoon_payload = {
        "event_type": "Corporate Gala",
        "guest_count": 120,
        "location": "Mumbai",
        "date": "2026-12-05",
        "budget": 500000,
        "event_time_slot": "Afternoon (12:00 PM - 5:00 PM)",
        "event_start_time": "12:30 PM",
        "catering_meal_slot": "Afternoon (Lunch Feast / High Tea)",
        "preferences": {
            "cuisine": "Multi-Cuisine",
            "decor_style": "Modern",
            "event_time_slot": "Afternoon (12:00 PM - 5:00 PM)",
            "event_start_time": "12:30 PM",
            "catering_meal_slot": "Afternoon (Lunch Feast / High Tea)",
        },
    }
    response = client.post("/plan", json=afternoon_payload)
    assert response.status_code == 200
    aft_data = response.json()
    aft_id = aft_data["event_id"]

    top_vendors = [v[0] for v in aft_data["recommendations"].values() if v]
    response = client.post(
        "/approve",
        json={"event_id": aft_id, "decision": "approve", "approved_vendors": top_vendors},
    )
    assert response.status_code == 200

    response = client.post("/notify/preview", json={"event_id": aft_id})
    assert response.status_code == 200
    aft_preview = response.json()
    briefs = aft_preview.get("vendor_rfps", [])
    catering_brief = next((b for b in briefs if b["category"].lower() == "catering"), None)
    assert catering_brief is not None
    assert "Meal Service Timing: Afternoon" in catering_brief["message"]
    print("  [OK] WhatsApp brief for afternoon caterer explicitly states: Meal Service Timing: Afternoon.")

    # Test 3: Night Event with Dinner Buffet
    night_payload = {
        "event_type": "Anniversary Gala",
        "guest_count": 80,
        "location": "Delhi",
        "date": "2026-10-15",
        "budget": 250000,
        "event_time_slot": "Evening / Night (5:00 PM - 11:30 PM)",
        "event_start_time": "07:00 PM",
        "catering_meal_slot": "Night (Dinner Buffet / Reception Banquet)",
        "preferences": {
            "cuisine": "North Indian",
            "decor_style": "Royal",
            "event_time_slot": "Evening / Night (5:00 PM - 11:30 PM)",
            "event_start_time": "07:00 PM",
            "catering_meal_slot": "Night (Dinner Buffet / Reception Banquet)",
        },
    }
    response = client.post("/plan", json=night_payload)
    assert response.status_code == 200
    night_data = response.json()
    night_id = night_data["event_id"]

    top_vendors = [v[0] for v in night_data["recommendations"].values() if v]
    response = client.post(
        "/approve",
        json={"event_id": night_id, "decision": "approve", "approved_vendors": top_vendors},
    )
    assert response.status_code == 200

    response = client.post("/notify/preview", json={"event_id": night_id})
    assert response.status_code == 200
    night_preview = response.json()
    briefs = night_preview.get("vendor_rfps", [])
    catering_brief = next((b for b in briefs if b["category"].lower() == "catering"), None)
    assert catering_brief is not None
    assert "Meal Service Timing: Night" in catering_brief["message"]
    print("  [OK] WhatsApp brief for night caterer explicitly states: Meal Service Timing: Night.")

    print("\n============================================================")
    print("ALL TIMING & CATERING MEAL SLOT TESTS PASSED! [OK]")
    print("============================================================")


if __name__ == "__main__":
    test_timing_and_catering_slots()
