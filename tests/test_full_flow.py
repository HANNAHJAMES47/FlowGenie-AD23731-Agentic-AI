import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=" * 60)
print("FLOWGENIE HUMAN-IN-THE-LOOP MULTI-AGENT WORKFLOW TEST")
print("=" * 60)

# 1. Test Health Endpoint
print("\n1. Testing /health endpoint...")
resp = client.get("/health")
assert resp.status_code == 200, f"Health check failed: {resp.status_code}"
print(f"   Status: {resp.status_code}")
print(f"   Response: {resp.json()}")

# 2. Test Plan Endpoint (Agents 1-4 execute, then wait for Human Approval)
print("\n2. Testing /plan (Agents 1-4 Sourcing & Preparing User Recommendations)...")
plan_payload = {
    "event_type": "Wedding",
    "guest_count": 150,
    "location": "Bangalore",
    "date": "2026-11-20",
    "budget": 450000,
    "preferences": {"cuisine": "Royal Pure Vegetarian", "decor_style": "Royal"},
}
resp = client.post("/plan", json=plan_payload)
assert resp.status_code == 200, f"Plan endpoint failed: {resp.status_code}"
plan_data = resp.json()
event_id = plan_data.get("event_id")
print(f"   Status: {resp.status_code}")
print(f"   Event ID: {event_id}")
print(f"   Workflow Status: {plan_data.get('status')} (Awaiting Human Review)")
print(f"   Approval Required: {plan_data.get('approval_required')}")
print(f"   Recommended Categories: {list(plan_data.get('recommendations', {}).keys())}")
print(f"   Agent Thought Logs: {len(plan_data.get('agent_logs', []))} steps")
for log in plan_data.get("agent_logs", []):
    print(f"     * [{log['agent']}] {log['step']}: {log['result_summary']}")

# 3. Test Human-in-the-Loop Review & Approval Gate (/approve)
print("\n3. Testing /approve endpoint (Human Review, Customization & Final Confirmation)...")
recommendations = plan_data.get("recommendations", {})
# Simulate user picking custom vendors
user_selected_vendors = [vendors[0] for vendors in recommendations.values() if vendors]
approve_payload = {
    "event_id": event_id,
    "decision": "approve",
    "approved_vendors": user_selected_vendors,
}
resp = client.post("/approve", json=approve_payload)
assert resp.status_code == 200, f"Approve failed: {resp.status_code}"
approve_data = resp.json()
print(f"   Status: {resp.status_code}")
print(f"   Booking Status: {approve_data.get('status')}")
print(f"   Contracted Vendors: {len(approve_data.get('booking_summary', {}).get('selected', []))} certified suppliers")
print(f"   Total Spend: INR {approve_data.get('booking_summary', {}).get('total_spend'):,}")
print(f"   Budget Remaining: INR {approve_data.get('booking_summary', {}).get('budget_remaining'):,}")
print(f"   Run-of-Show Milestones Generated: {len(approve_data.get('run_of_show', []))} checkpoints")
for m in approve_data.get("run_of_show", [])[:3]:
    print(f"     * [{m['time']}] {m['title']}")

# 4. Test Status Monitoring Endpoint
print("\n4. Testing /status endpoint...")
resp = client.get(f"/status/{event_id}")
assert resp.status_code == 200, f"Status failed: {resp.status_code}"
status_data = resp.json()
print(f"   Status: {resp.status_code}")
print(f"   Monitoring status: {status_data.get('status')}")
print(f"   Timeline steps completed: {sum(1 for t in status_data.get('timeline', []) if t.get('complete'))}")

# 5. Test Replan / Contingency Endpoint (Simulating Supplier Cancellation)
print("\n5. Testing /replan endpoint (Simulating Vendor Cancellation)...")
replan_payload = {"event_id": event_id, "category": "catering"}
resp = client.post("/replan", json=replan_payload)
assert resp.status_code == 200, f"Replan failed: {resp.status_code}"
replan_data = resp.json()
print(f"   Status: {resp.status_code}")
print(f"   Replan status: {replan_data.get('status')}")
print(f"   Alert message: {replan_data.get('alert')}")
print(f"   Replacement recommendations: {len(replan_data.get('recommendations', {}).get('catering', []))} options")

# 6. Test Frontend Static Asset Serving & Images
print("\n6. Testing frontend asset serving & local images...")
resp = client.get("/")
assert resp.status_code == 200
assert "FlowGenie" in resp.text
assert "eventForm" in resp.text
print("   Frontend index.html loads successfully [OK]")

resp_js = client.get("/static/app.js")
assert resp_js.status_code == 200
assert "submitPrompt" in resp_js.text
print("   Frontend app.js loads successfully [OK]")

resp_img = client.get("/static/images/venue_1.svg")
assert resp_img.status_code == 200
print("   Frontend local SVG images load successfully [OK]")

print("\n" + "=" * 60)
print("ALL FLOWGENIE HUMAN-IN-THE-LOOP TESTS PASSED! [OK]")
print("=" * 60)
