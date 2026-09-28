import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_customizable_schedule():
    print("Testing: Customizable Hour-by-Hour Timeline Schedule System...")

    # 1. Fetch Schedule Presets
    response = client.get("/schedule/presets")
    assert response.status_code == 200
    presets = response.json()
    assert "south_indian" in presets
    assert "sangeet_north" in presets
    assert "christian_wedding" in presets
    print("  [OK] /schedule/presets returned authentic tradition presets.")

    # 2. Plan Event
    plan_payload = {
        "event_type": "Wedding",
        "guest_count": 150,
        "location": "Bangalore",
        "budget": 450000,
        "cuisine": "South Indian Vegetarian",
        "decor_style": "Traditional Floral",
    }
    response = client.post("/plan", json=plan_payload)
    assert response.status_code == 200
    plan_data = response.json()
    event_id = plan_data["event_id"]
    assert event_id is not None
    print(f"  [OK] Event planned with ID: {event_id}")

    # 3. Approve with Custom Run-of-Show
    custom_milestones = [
        {"time": "06:00 AM", "title": "Traditional Kolam & Nadaswaram Arrival", "description": "Musicians welcome family with morning ragas.", "category": "ceremony"},
        {"time": "07:30 AM", "title": "Ganesh & Kashi Yatra Pooja", "description": "Family rituals and auspicious blessings.", "category": "ceremony"},
        {"time": "09:15 AM", "title": "Auspicious Muhurtham & Mangalsutra Dharana", "description": "Sacred vows and floral shower.", "category": "ceremony"},
        {"time": "11:30 AM", "title": "Kalyana Virundhu Traditional Feast", "description": "Authentic plantain leaf 24-dish vegetarian feast.", "category": "catering"},
        {"time": "06:30 PM", "title": "Grand Reception & Carnatic Fusion", "description": "Stage greetings and live orchestra.", "category": "entertainment"},
    ]

    top_vendors = [v[0] for v in plan_data["recommendations"].values() if v]
    approve_payload = {
        "event_id": event_id,
        "decision": "approve",
        "approved_vendors": top_vendors,
        "run_of_show": custom_milestones,
    }
    response = client.post("/approve", json=approve_payload)
    assert response.status_code == 200
    approve_data = response.json()
    returned_ros = approve_data.get("run_of_show", [])
    assert len(returned_ros) == 5
    assert returned_ros[0]["title"] == "Traditional Kolam & Nadaswaram Arrival"
    assert returned_ros[2]["time"] == "09:15 AM"
    print("  [OK] /approve successfully saved and returned custom schedule milestones.")

    # 4. Update Schedule Dynamically
    custom_milestones.append({
        "time": "10:30 PM",
        "title": "Custom Couple Send-off & Transport",
        "description": "Decorated vintage car exit and guest favor distribution.",
        "category": "venue"
    })
    update_payload = {
        "event_id": event_id,
        "run_of_show": custom_milestones,
    }
    response = client.post("/schedule/update", json=update_payload)
    assert response.status_code == 200
    update_data = response.json()
    assert update_data["status"] == "updated"
    assert len(update_data["run_of_show"]) == 6
    print("  [OK] /schedule/update added custom 6th milestone successfully.")

    # 5. Verify in Live Status
    response = client.get(f"/status/{event_id}")
    assert response.status_code == 200
    status_data = response.json()
    assert len(status_data.get("run_of_show", [])) == 6
    assert status_data["run_of_show"][-1]["title"] == "Custom Couple Send-off & Transport"
    print("  [OK] /status endpoint successfully reflects all 6 customized milestones.")

    print("\n============================================================")
    print("ALL CUSTOMIZABLE SCHEDULE TESTS PASSED! [OK]")
    print("============================================================")


if __name__ == "__main__":
    test_customizable_schedule()
