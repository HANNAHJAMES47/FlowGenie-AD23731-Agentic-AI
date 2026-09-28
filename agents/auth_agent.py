"""User Authentication & Account Management Agent for FlowGenie.

Manages user registration, secure password hashing with salt, session tokens,
and associating planned event itineraries and favorites with user profiles.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import time
from typing import Any
from memory.store import get_memory


class AuthManager:
    """Manages persistent user accounts, authentication tokens, and profile history."""

    def __init__(self) -> None:
        self.memory = get_memory()
        self.secret_key = os.getenv("AUTH_SECRET_KEY", "flowgenie-secure-secret-key-2026")

    def _hash_password(self, password: str, salt: str | None = None) -> tuple[str, str]:
        """Generate SHA-256 password hash with unique salt."""
        if not salt:
            salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256(f"{salt}{password}{self.secret_key}".encode("utf-8"))
        password_hash = hash_obj.hexdigest()
        return password_hash, salt

    def _verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify provided password against stored hash."""
        computed_hash, _ = self._hash_password(password, salt)
        return hmac.compare_digest(computed_hash, password_hash)

    def _get_users_dict(self) -> dict[str, Any]:
        """Retrieve all registered users from shared memory."""
        users = self.memory.get("auth_users")
        if not isinstance(users, dict):
            users = {}
            self.memory.set("auth_users", users)
        return users

    def _save_users_dict(self, users: dict[str, Any]) -> None:
        """Persist registered users in shared memory."""
        self.memory.set("auth_users", users)

    def _get_sessions_dict(self) -> dict[str, Any]:
        """Retrieve active sessions from shared memory."""
        sessions = self.memory.get("auth_sessions")
        if not isinstance(sessions, dict):
            sessions = {}
            self.memory.set("auth_sessions", sessions)
        return sessions

    def _save_sessions_dict(self, sessions: dict[str, Any]) -> None:
        """Persist active sessions in shared memory."""
        self.memory.set("auth_sessions", sessions)

    def register_user(
        self,
        name: str,
        email: str,
        phone: str,
        password: str,
        role: str = "Host / Planner",
    ) -> dict[str, Any]:
        """Register a new user account with unique email validation."""
        name = name.strip()
        email = email.strip().lower()
        phone = phone.strip()

        if not name or not email or not password:
            raise ValueError("Name, email, and password are required.")

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")

        users = self._get_users_dict()
        if email in users:
            raise ValueError("An account with this email already exists. Please sign in.")

        user_id = f"usr_{secrets.token_hex(6)}"
        password_hash, salt = self._hash_password(password)

        user_profile = {
            "id": user_id,
            "name": name,
            "email": email,
            "phone": phone or "+91 98450 12345",
            "role": role,
            "password_hash": password_hash,
            "salt": salt,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "event_history": [],
            "favorites": {},
            "preferences": {},
        }

        users[email] = user_profile
        self._save_users_dict(users)

        # Generate active session token
        token = self._create_session(user_profile)

        # Return safe profile (without password hash and salt)
        safe_profile = self._sanitize_profile(user_profile)
        return {
            "token": token,
            "user": safe_profile,
            "message": f"Welcome to FlowGenie, {name}!",
        }

    def authenticate_user(self, email_or_phone: str, password: str) -> dict[str, Any]:
        """Authenticate user by email or phone and return session token."""
        query = email_or_phone.strip().lower()
        users = self._get_users_dict()

        target_user = None
        for user in users.values():
            if user.get("email") == query or user.get("phone") == query:
                target_user = user
                break

        if not target_user:
            raise ValueError("No account found with this email or phone.")

        if not self._verify_password(password, target_user["password_hash"], target_user["salt"]):
            raise ValueError("Incorrect password. Please try again.")

        token = self._create_session(target_user)
        safe_profile = self._sanitize_profile(target_user)

        return {
            "token": token,
            "user": safe_profile,
            "message": f"Welcome back, {target_user['name']}!",
        }

    def demo_login(self) -> dict[str, Any]:
        """Instant 1-click login with a pre-configured demo VIP planner profile."""
        demo_email = "demo.planner@flowgenie.ai"
        users = self._get_users_dict()

        if demo_email not in users:
            return self.register_user(
                name="Ananya Roy",
                email=demo_email,
                phone="+91 98450 99887",
                password="demopassword123",
                role="Bride & Event Host",
            )
        else:
            demo_user = users[demo_email]
            token = self._create_session(demo_user)
            return {
                "token": token,
                "user": self._sanitize_profile(demo_user),
                "message": "Signed in with Demo VIP Account!",
            }

    def _create_session(self, user: dict[str, Any]) -> str:
        """Create a new session token for the user."""
        token = f"fg_sess_{secrets.token_hex(20)}"
        sessions = self._get_sessions_dict()
        sessions[token] = {
            "user_id": user["id"],
            "email": user["email"],
            "created_at": time.time(),
        }
        self._save_sessions_dict(sessions)
        return token

    def get_user_by_token(self, token: str) -> dict[str, Any] | None:
        """Retrieve user profile from session token."""
        if not token:
            return None
        sessions = self._get_sessions_dict()
        session = sessions.get(token)
        if not session:
            return None

        user_email = session.get("email")
        users = self._get_users_dict()
        user = users.get(user_email)
        return self._sanitize_profile(user) if user else None

    def logout_user(self, token: str) -> bool:
        """Invalidate a session token."""
        sessions = self._get_sessions_dict()
        if token in sessions:
            del sessions[token]
            self._save_sessions_dict(sessions)
            return True
        return False

    def link_event_to_user(self, token_or_email: str, event_summary: dict[str, Any]) -> bool:
        """Link a newly planned or confirmed event to the user's history."""
        users = self._get_users_dict()
        target_user = None

        if token_or_email in users:
            target_user = users[token_or_email]
        else:
            sessions = self._get_sessions_dict()
            session = sessions.get(token_or_email)
            if session and session.get("email") in users:
                target_user = users[session["email"]]

        if target_user:
            event_id = event_summary.get("event_id")
            existing_ids = [e.get("event_id") for e in target_user.get("event_history", [])]
            if event_id not in existing_ids:
                target_user.setdefault("event_history", []).append(event_summary)
                self._save_users_dict(users)
                return True
        return False

    def _sanitize_profile(self, user: dict[str, Any]) -> dict[str, Any]:
        """Remove sensitive password hash and salt from user object."""
        return {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "phone": user.get("phone"),
            "role": user.get("role", "Event Host"),
            "created_at": user.get("created_at"),
            "event_history": user.get("event_history", []),
            "favorites": user.get("favorites", {}),
            "preferences": user.get("preferences", {}),
        }


auth_manager = AuthManager()

__all__ = ["AuthManager", "auth_manager"]
