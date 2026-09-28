import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.budget_agent import BudgetPlanningAgent
from agents.requirement_agent import RequirementAnalysisAgent
from workflow.graph import EventWorkflowEngine


class TestCustomCategorySystem(unittest.TestCase):
    def setUp(self):
        self.req_agent = RequirementAnalysisAgent()
        self.budget_agent = BudgetPlanningAgent()
        self.engine = EventWorkflowEngine()

    def test_extract_room_stay_requirement(self):
        prompt = "Plan a wedding for 150 guests in Bangalore with a budget of 500000. I want rooms for my guests to stay."
        reqs, log = self.req_agent.run(prompt)

        self.assertIsNotNone(reqs.get("custom_category"))
        custom_cat = reqs["custom_category"]
        self.assertEqual(custom_cat["key"], "stay")
        self.assertIn("Room", custom_cat["title"])
        print(f"  [OK] Extracted stay category: {custom_cat['title']} (key: {custom_cat['key']})")

    def test_budget_rekeys_to_custom_category(self):
        reqs = {
            "event_type": "Wedding",
            "guest_count": 150,
            "budget": 600000,
            "custom_category": {
                "key": "stay",
                "title": "Guest Accommodation & Rooms",
                "search_term": "guest accommodation hotel rooms",
                "type": "stay",
            },
        }
        b_plan, log = self.budget_agent.run(reqs)
        allocations = b_plan["category_allocations"]
        titles = b_plan["category_titles"]

        self.assertIn("stay", allocations)
        self.assertNotIn("others", allocations)
        self.assertGreater(allocations["stay"], 0)
        self.assertEqual(titles["stay"], "Guest Accommodation & Rooms")
        print(f"  [OK] Budget allocated INR {allocations['stay']} to custom category 'stay' with title '{titles['stay']}'.")

    def test_extract_custom_cake_and_transport(self):
        prompt_cake = "Birthday party with budget 50000. Need a 5-tier designer wedding cake."
        reqs_cake, _ = self.req_agent.run(prompt_cake)
        self.assertEqual(reqs_cake["custom_category"]["key"], "cake")

        prompt_trans = "Corporate gala for 200 guests with vintage car transport fleet."
        reqs_trans, _ = self.req_agent.run(prompt_trans)
        self.assertEqual(reqs_trans["custom_category"]["key"], "transport")
        print("  [OK] Successfully extracted cake & transport custom categories.")

    def test_full_pipeline_custom_category(self):
        prompt = "Plan a Wedding for 100 guests in Bangalore budget 400000. Note: need rooms for guests to stay."
        result = asyncio.run(self.engine.run_full_pipeline(prompt, auto_approve=True))

        recs = result["recommendations"]
        self.assertIn("stay", recs)
        self.assertEqual(len(recs["stay"]), 3)
        for v in recs["stay"]:
            self.assertIn("stay", v["id"])
            self.assertGreater(v["price"], 0)
            self.assertTrue(bool(v["name"]))

        # Check budget plan titles
        self.assertIn("stay", result["budget_plan"]["category_allocations"])
        self.assertEqual(result["budget_plan"]["category_titles"]["stay"], "Guest Accommodation & Rooms")
        print(f"  [OK] Pipeline generated 3 tailored stay recommendations: {[v['name'] for v in recs['stay']]}")


if __name__ == "__main__":
    unittest.main()
