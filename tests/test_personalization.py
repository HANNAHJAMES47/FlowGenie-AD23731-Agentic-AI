#!/usr/bin/env python3
"""
Test script for FlowGenie personalization features.
Tests all personalization functionality end-to-end using TestClient.
"""

import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_frontend_loads():
    """Test that frontend loads with personalization features."""
    print("Testing: Frontend loads with personalization features...")
    response = client.get("/")
    assert response.status_code == 200, f"Frontend failed to load: {response.status_code}"

    # Check for personalization elements
    assert "profileBtn" in response.text, "Profile button not found"
    assert "profileDrawer" in response.text, "Profile drawer not found"
    assert "suggestionsCard" in response.text, "Suggestions card not found"
    assert "eventHistoryList" in response.text, "Event history container not found"

    print("  [OK] Frontend loads with all personalization UI elements")


def test_app_js_has_features():
    """Test that app.js contains all personalization logic."""
    print("\nTesting: app.js has personalization logic...")
    response = client.get("/static/app.js")
    assert response.status_code == 200

    required_functions = [
        "loadFromLocalStorage",
        "saveToLocalStorage",
        "updateGreeting",
        "renderProfileDrawer",
        "showPersonalizedSuggestions",
        "toggleFavoritesView",
    ]

    for func in required_functions:
        assert func in response.text, f"Function {func} not found in app.js"

    # Check for state tracking
    assert "state.user" in response.text, "User state not found"
    assert "state.favorites" in response.text, "Favorites state not found"
    assert "state.eventHistory" in response.text, "Event history state not found"
    assert "state.preferences" in response.text, "Preferences state not found"

    print("  [OK] app.js contains all personalization functions and state")


def test_api_endpoints():
    """Test that all API endpoints work."""
    print("\nTesting: All API endpoints work...")

    # Health check
    response = client.get("/health")
    assert response.status_code == 200, "Health check failed"
    print("  [OK] /health endpoint works")

    # Plan endpoint
    plan_payload = {
        "event_type": "Wedding",
        "guest_count": 150,
        "location": "Bangalore",
        "date": (datetime.now() + timedelta(days=30)).isoformat()[:10],
        "budget": 350000,
        "preferences": {
            "cuisine": "Italian",
            "decor_style": "Modern",
        },
    }
    response = client.post("/plan", json=plan_payload)
    assert response.status_code == 200, f"Plan endpoint failed: {response.status_code}"
    plan_data = response.json()
    assert "event_id" in plan_data, "event_id not in response"
    assert "recommendations" in plan_data, "recommendations not in response"
    event_id = plan_data["event_id"]
    print(f"  [OK] /plan endpoint works (event_id: {event_id})")

    # Get first category recommendations for testing
    first_category = list(plan_data["recommendations"].keys())[0]
    selected_vendor = plan_data["recommendations"][first_category][0]

    # Approve endpoint
    approved_vendors = [selected_vendor]
    approve_payload = {
        "event_id": event_id,
        "decision": "approve",
        "approved_vendors": approved_vendors,
    }
    response = client.post("/approve", json=approve_payload)
    assert response.status_code == 200, f"Approve endpoint failed: {response.status_code}"
    approve_data = response.json()
    assert approve_data.get("status") == "booked", f"Event not booked: {approve_data}"
    assert "run_of_show" in approve_data, "run_of_show schedule not returned"
    print("  [OK] /approve endpoint works with run-of-show schedule")

    # Status endpoint
    response = client.get(f"/status/{event_id}")
    assert response.status_code == 200, f"Status endpoint failed: {response.status_code}"
    print("  [OK] /status endpoint works")

    # Replan endpoint
    response = client.post("/replan", json={"event_id": event_id, "category": first_category})
    assert response.status_code == 200, f"Replan failed: {response.status_code}"
    print("  [OK] /replan endpoint works with contingency recovery")


def test_styles_css():
    """Test that styles.css has personalization and agent console styling."""
    print("\nTesting: styles.css has styles...")
    response = client.get("/static/styles.css")
    assert response.status_code == 200

    required_classes = [
        ".profile-drawer",
        ".drawer-header",
        ".profile-section",
        ".suggestions-card",
        ".favorite-btn",
        ".audit-details",
        ".schedule-card",
    ]

    for cls in required_classes:
        assert cls in response.text, f"CSS class {cls} not found"

    print("  [OK] styles.css contains all styling")


def main():
    """Run all tests."""
    print("=" * 60)
    print("FlowGenie Personalization & 5-Agent Pipeline - Test Suite")
    print("=" * 60)

    try:
        test_frontend_loads()
        test_app_js_has_features()
        test_styles_css()
        test_api_endpoints()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! [OK]")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n[FAIL] ERROR: {e}")
        exit(1)


if __name__ == "__main__":
    main()
