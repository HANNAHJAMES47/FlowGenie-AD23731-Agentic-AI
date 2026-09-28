import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.routes import router
from agents.auth_agent import auth_manager

app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestAuthSystem(unittest.TestCase):
    def setUp(self):
        # Reset auth data for clean test runs
        auth_manager.memory.set("auth_users", {})
        auth_manager.memory.set("auth_sessions", {})

    def test_01_user_registration_and_validation(self):
        """Test registration endpoint with valid data and duplicate handling."""
        # 1. Valid registration
        res = client.post(
            "/auth/signup",
            json={
                "name": "Priya Sharma",
                "email": "priya.sharma@example.com",
                "phone": "+91 98450 11223",
                "password": "securepassword123",
                "role": "Bride & Event Host",
            },
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("token", data)
        self.assertEqual(data["user"]["name"], "Priya Sharma")
        self.assertEqual(data["user"]["email"], "priya.sharma@example.com")
        self.assertNotIn("password_hash", data["user"])

        # 2. Duplicate registration check
        dup_res = client.post(
            "/auth/signup",
            json={
                "name": "Priya Duplicate",
                "email": "priya.sharma@example.com",
                "phone": "+91 98450 99999",
                "password": "anotherpassword",
            },
        )
        self.assertEqual(dup_res.status_code, 400)
        self.assertIn("already exists", dup_res.json()["detail"])

    def test_02_user_login_and_invalid_credentials(self):
        """Test authentication endpoint with valid and invalid credentials."""
        # Register user
        client.post(
            "/auth/signup",
            json={
                "name": "Vikram Malhotra",
                "email": "vikram@example.com",
                "phone": "+91 98450 44556",
                "password": "corporatepass2026",
                "role": "Corporate Event Organizer",
            },
        )

        # Valid login with email
        login_res = client.post(
            "/auth/login",
            json={
                "email_or_phone": "vikram@example.com",
                "password": "corporatepass2026",
            },
        )
        self.assertEqual(login_res.status_code, 200)
        token = login_res.json()["token"]
        self.assertTrue(token.startswith("fg_sess_"))

        # Valid login with phone
        phone_login_res = client.post(
            "/auth/login",
            json={
                "email_or_phone": "+91 98450 44556",
                "password": "corporatepass2026",
            },
        )
        self.assertEqual(phone_login_res.status_code, 200)

        # Invalid password
        bad_pass_res = client.post(
            "/auth/login",
            json={
                "email_or_phone": "vikram@example.com",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(bad_pass_res.status_code, 401)

    def test_03_demo_login_and_session_me(self):
        """Test 1-click Demo Login and /auth/me profile fetching."""
        demo_res = client.post("/auth/demo-login")
        self.assertEqual(demo_res.status_code, 200)
        token = demo_res.json()["token"]

        # Fetch session
        me_res = client.get(f"/auth/me?token={token}")
        self.assertEqual(me_res.status_code, 200)
        me_data = me_res.json()
        self.assertTrue(me_data["authenticated"])
        self.assertEqual(me_data["user"]["name"], "Ananya Roy")

        # Logout
        logout_res = client.post("/auth/logout", json={"token": token})
        self.assertEqual(logout_res.status_code, 200)

        # Fetch after logout should fail
        me_after_res = client.get(f"/auth/me?token={token}")
        self.assertEqual(me_after_res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
