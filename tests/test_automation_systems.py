"""Automated Test Suite for Option 3 (Sentinel Watchdog) & Option 4 (WhatsApp/Email RFP Dispatch)."""

import os
import sys
import unittest
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app
from agents.notification_agent import NotificationAgent
from agents.sentinel_agent import SentinelWatchdog


class TestAutomationSystems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_notification_agent_rfp_generation(self):
        """Test NotificationAgent creates category-tailored RFPs with wa.me URLs."""
        agent = NotificationAgent()
        vendor = {
            "id": "catering-1",
            "name": "Royal Feast Caterers",
            "category": "catering",
            "price": 120000.0,
            "contact": "+91 98450 12345",
        }
        event_info = {
            "event_type": "Wedding",
            "location": "Bangalore",
            "date": "2026-12-20",
            "guest_count": 200,
            "preferences": {"cuisine": "North Indian"},
        }
        rfp = agent.generate_vendor_rfp(vendor, event_info)

        self.assertEqual(rfp["vendor_name"], "Royal Feast Caterers")
        self.assertIn("wa.me/919845012345", rfp["whatsapp_url"])
        self.assertIn("200 Guests", rfp["message"])
        self.assertIn("North Indian", rfp["message"])
        print("  [OK] NotificationAgent generates tailored RFPs with WhatsApp links")

    def test_02_notify_preview_and_dispatch_endpoints(self):
        """Test /notify/preview and /notify/dispatch-all REST endpoints."""
        # 1. Plan an event first
        plan_resp = self.client.post(
            "/plan",
            json={
                "event_type": "Anniversary",
                "guest_count": 80,
                "location": "Bangalore",
                "budget": 250000,
            },
        )
        self.assertEqual(plan_resp.status_code, 200)
        event_id = plan_resp.json()["event_id"]

        # 2. Approve event
        app_resp = self.client.post(
            "/approve",
            json={"event_id": event_id, "decision": "approve"},
        )
        self.assertEqual(app_resp.status_code, 200)

        # 3. Test /notify/preview
        preview_resp = self.client.post(
            "/notify/preview",
            json={"event_id": event_id},
        )
        self.assertEqual(preview_resp.status_code, 200)
        preview_data = preview_resp.json()
        self.assertGreater(len(preview_data["vendor_rfps"]), 0)
        self.assertIn("whatsapp_url", preview_data["client_summary"])
        print(f"  [OK] /notify/preview generated {len(preview_data['vendor_rfps'])} supplier RFPs")

        # 4. Test /notify/dispatch-all
        dispatch_resp = self.client.post(
            "/notify/dispatch-all",
            json={
                "event_id": event_id,
                "client_email": "testclient@example.com",
            },
        )
        self.assertEqual(dispatch_resp.status_code, 200)
        dispatch_data = dispatch_resp.json()
        self.assertTrue(dispatch_data["dispatched"])
        print("  [OK] /notify/dispatch-all dispatches RFPs and client email")

    def test_03_sentinel_watchdog_health_and_auto_recovery(self):
        """Test SentinelWatchdog background monitoring and auto-recovery."""
        # Plan & approve event
        plan_resp = self.client.post(
            "/plan",
            json={
                "event_type": "Corporate",
                "guest_count": 100,
                "location": "Bangalore",
                "budget": 300000,
            },
        )
        event_id = plan_resp.json()["event_id"]
        self.client.post("/approve", json={"event_id": event_id})

        # 1. Toggle watchdog
        toggle_resp = self.client.post(
            "/sentinel/watchdog/toggle",
            json={"event_id": event_id, "enable": True},
        )
        self.assertEqual(toggle_resp.status_code, 200)
        self.assertTrue(toggle_resp.json()["watchdog_active"])
        print("  [OK] /sentinel/watchdog/toggle enables autonomous watchdog")

        # 2. Trigger auto-recover
        recover_resp = self.client.post(
            "/sentinel/auto-recover",
            json={
                "event_id": event_id,
                "category": "catering",
                "reason": "Simulated supplier cancellation",
            },
        )
        self.assertEqual(recover_resp.status_code, 200)
        rec_data = recover_resp.json()
        self.assertEqual(rec_data["recovery_result"]["status"], "resolved")
        print(f"  [OK] Sentinel auto-recovered '{rec_data['recovery_result']['category']}' with '{rec_data['recovery_result']['new_vendor']['name']}'")

        # 3. Check audit log
        audit_resp = self.client.get(f"/sentinel/audit-log/{event_id}")
        self.assertEqual(audit_resp.status_code, 200)
        audit_data = audit_resp.json()
        self.assertGreaterEqual(audit_data["total_incidents"], 2)
        print(f"  [OK] /sentinel/audit-log recorded {audit_data['total_incidents']} autonomous incident entries")


if __name__ == "__main__":
    print("=" * 60)
    print("FLOWGENIE AUTOMATION TEST SUITE (SENTINEL & NOTIFICATIONS)")
    print("=" * 60)
    unittest.main(verbosity=2)
