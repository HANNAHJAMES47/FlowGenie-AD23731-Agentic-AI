import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.routes import router
from agents.auth_agent import auth_manager

app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestLandingAndAuthGate(unittest.TestCase):
    def setUp(self):
        auth_manager.memory.set("auth_users", {})
        auth_manager.memory.set("auth_sessions", {})
        self.frontend_dir = Path(__file__).parent.parent / "frontend"

    def test_01_landing_html_structure(self):
        """Verify landingView section, 5 agents showcase, and CTAs in index.html."""
        index_html_path = self.frontend_dir / "index.html"
        self.assertTrue(index_html_path.exists(), "frontend/index.html must exist")

        content = index_html_path.read_text(encoding="utf-8")

        # 1. Landing View container
        self.assertIn('id="landingView"', content)
        self.assertIn('class="panel active"', content)

        # 2. Prompt View should be gated / hidden by default
        self.assertIn('id="promptView"', content)
        self.assertIn('id="promptView" class="panel hidden"', content)

        # 3. 5 Agents showcase
        self.assertIn("Requirement Analyst Agent", content)
        self.assertIn("Budget & Finance Strategist", content)
        self.assertIn("Autonomous Vendor Discovery", content)
        self.assertIn("MCDA Ranking & Aggregator", content)
        self.assertIn("Booking, Traditions & Sentinel Watchdog", content)

        # 4. CTAs
        self.assertIn('id="landingGetStartedBtn"', content)
        self.assertIn('id="landingSignInBtn"', content)
        self.assertIn('id="landingDemoBtn"', content)
        self.assertIn('id="navHomeTab"', content)
        self.assertIn('id="authModal"', content)
        self.assertIn('id="plannerUserBanner"', content)

    def test_02_landing_css_styles(self):
        """Verify CSS tokens and responsive rules for the landing page."""
        styles_css_path = self.frontend_dir / "styles.css"
        self.assertTrue(styles_css_path.exists(), "frontend/styles.css must exist")

        css_content = styles_css_path.read_text(encoding="utf-8")
        self.assertIn(".landing-hero-card", css_content)
        self.assertIn(".landing-agents-grid", css_content)
        self.assertIn(".landing-agent-card", css_content)
        self.assertIn(".landing-features-grid", css_content)
        self.assertIn(".landing-stats-grid", css_content)
        self.assertIn(".planner-user-banner", css_content)

    def test_03_landing_js_gating_logic(self):
        """Verify app.js handles landing routing and auth gating."""
        app_js_path = self.frontend_dir / "app.js"
        self.assertTrue(app_js_path.exists(), "frontend/app.js must exist")

        js_content = app_js_path.read_text(encoding="utf-8")
        self.assertIn("landing: document.getElementById('landingView')", js_content)
        self.assertIn("landingGetStartedBtn", js_content)
        self.assertIn("openAuthModal", js_content)
        self.assertIn("showView(state.auth && state.auth.isLoggedIn ? 'prompt' : 'landing')", js_content)

    def test_04_auth_endpoints_enable_planner_unlock(self):
        """Verify backend authentication flow that unlocks the prompt planner."""
        # 1. Sign up new planner user
        signup_res = client.post(
            "/auth/signup",
            json={
                "name": "Karan Mehra",
                "email": "karan.planner@example.com",
                "phone": "+91 98765 43210",
                "password": "weddingpass2026",
                "role": "Host & Planner",
            },
        )
        self.assertEqual(signup_res.status_code, 200)
        token = signup_res.json()["token"]

        # 2. Verify session active
        me_res = client.get(f"/auth/me?token={token}")
        self.assertEqual(me_res.status_code, 200)
        self.assertTrue(me_res.json()["authenticated"])
        self.assertEqual(me_res.json()["user"]["name"], "Karan Mehra")


if __name__ == "__main__":
    unittest.main()
