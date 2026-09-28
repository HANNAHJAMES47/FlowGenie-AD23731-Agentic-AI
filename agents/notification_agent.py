"""Notification and Vendor RFP Dispatch Agent for FlowGenie.

Generates structured, professional RFPs (Request For Proposals) for event
suppliers and builds direct WhatsApp Web and Email dispatch links.
"""

from __future__ import annotations

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any
import urllib.parse
from memory.store import get_memory


class NotificationAgent:
    def __init__(self) -> None:
        self.memory = get_memory()
        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_pass = os.getenv("SMTP_PASS", "")

    def clean_phone_number(self, phone: str) -> str:
        """Strip spaces, hyphens, and non-digits from phone number for wa.me links."""
        cleaned = "".join(filter(str.isdigit, str(phone)))
        if len(cleaned) == 10:
            cleaned = f"91{cleaned}"
        elif cleaned.startswith("0"):
            cleaned = f"91{cleaned[1:]}"
        return cleaned or "919845012345"

    def generate_vendor_rfp(
        self,
        vendor: dict[str, Any],
        event_info: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate a customized RFP brief for a specific vendor category."""
        category = vendor.get("category", "service").capitalize()
        vendor_name = vendor.get("name", "Valued Partner")
        event_type = event_info.get("event_type", "Event")
        event_date = event_info.get("date", "Upcoming Date")
        location = event_info.get("location", "Bangalore")
        guests = event_info.get("guest_count", 150)
        contract_budget = vendor.get("price", 0)
        event_time_slot = event_info.get("preferences", {}).get("event_time_slot") or event_info.get("event_time_slot", "Evening / Night (5:00 PM - 11:30 PM)")
        event_start_time = event_info.get("preferences", {}).get("event_start_time") or event_info.get("event_start_time", "06:00 PM")
        meal_slot = event_info.get("preferences", {}).get("catering_meal_slot") or event_info.get("catering_meal_slot", "Night (Dinner Buffet)")

        # Build category-specific bullet points
        category_specs = ""
        if category.lower() == "venue":
            category_specs = f"- Timing: {event_time_slot} (Event Starts: {event_start_time})\n- Expected Capacity: {guests} Guests\n- Hall Setup: Banquet & Cocktail Seating\n- Requirement: Full day access with power backup"
        elif category.lower() == "catering":
            cuisine = event_info.get("preferences", {}).get("cuisine", "Multi-Cuisine")
            category_specs = f"- Meal Service Timing: {meal_slot}\n- Headcount: {guests} Guests\n- Menu Style: {cuisine}\n- Service: Live Counters & Dining Service"
        elif category.lower() == "decor":
            decor = event_info.get("preferences", {}).get("decor_style", "Modern")
            category_specs = f"- Event Timing: {event_time_slot}\n- Theme: {decor}\n- Scope: Stage backdrop, entrance arch, table centerpieces & ambient lighting"
        elif category.lower() == "photography":
            category_specs = f"- Event Timing: {event_time_slot} (Call Time: {event_start_time})\n- Coverage: Full Event ({guests} guests)\n- Deliverables: Traditional + Candid Photos, Cinematic Highlight Video"
        else:
            category_specs = f"- Event Timing: {event_time_slot} (Starts: {event_start_time})\n- Deliverables: Full service package for {guests} guests on {event_date}"

        message_body = (
            f"BOOKING ENQUIRY & RFP — FLOWGENIE CONCIERGE\n\n"
            f"Dear {vendor_name},\n\n"
            f"We are pleased to confirm a booking request for an upcoming {event_type} in {location}.\n\n"
            f"Event Date: {event_date}\n"
            f"Event Timing: {event_time_slot} (Starts: {event_start_time})\n"
            f"Guest Count: {guests} Guests\n"
            f"Budget Allocation: INR {contract_budget:,.2f}\n\n"
            f"Key Requirements:\n{category_specs}\n\n"
            f"Please confirm your team's availability and acceptance of this brief. Thank you!\n\n"
            f"— FlowGenie Event Planning Concierge"
        )

        phone = vendor.get("contact", "+91 98450 12345")
        clean_phone = self.clean_phone_number(phone)
        encoded_text = urllib.parse.quote(message_body)
        whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_text}"

        return {
            "vendor_id": vendor.get("id", ""),
            "vendor_name": vendor_name,
            "category": category,
            "contact": phone,
            "whatsapp_url": whatsapp_url,
            "message": message_body,
        }

    def generate_client_summary(
        self,
        event_info: dict[str, Any],
        booked_vendors: list[dict[str, Any]],
        run_of_show: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Generate a complete event confirmation brief for the client."""
        client_name = event_info.get("user_name", "Client")
        event_type = event_info.get("event_type", "Event")
        event_date = event_info.get("date", "Upcoming Date")
        location = event_info.get("location", "Bangalore")
        guests = event_info.get("guest_count", 150)
        total_spend = sum(float(v.get("price", 0)) for v in booked_vendors)

        vendor_lines = "\n".join(
            [f"- {v.get('category', '').capitalize()}: {v.get('name')} (INR {float(v.get('price', 0)):,.2f}) — Contact: {v.get('contact', 'Verified')}"
             for v in booked_vendors]
        )

        schedule_lines = "\n".join(
            [f"[{m.get('time', 'TBD')}] {m.get('title', '')} — {m.get('description', '')}"
             for m in run_of_show[:5]]
        )

        message_body = (
            f"YOUR EVENT ITINERARY IS CONFIRMED — FLOWGENIE\n\n"
            f"Dear {client_name},\n\n"
            f"Your {event_type} in {location} for {guests} guests on {event_date} has been successfully planned and scheduled!\n\n"
            f"Total Event Cost: INR {total_spend:,.2f}\n\n"
            f"Booked Vendors:\n{vendor_lines}\n\n"
            f"Day-of-Event Schedule Preview:\n{schedule_lines}\n\n"
            f"View live updates anytime in your FlowGenie dashboard.\n\n"
            f"— FlowGenie Smart Event Planner"
        )

        client_phone = self.clean_phone_number(event_info.get("user_phone", "919845012345"))
        encoded_text = urllib.parse.quote(message_body)
        whatsapp_url = f"https://wa.me/{client_phone}?text={encoded_text}"

        return {
            "client_name": client_name,
            "event_type": event_type,
            "total_spend": total_spend,
            "message": message_body,
            "whatsapp_url": whatsapp_url,
        }

    def dispatch_email(self, to_email: str, subject: str, body_text: str) -> bool:
        """Send an email via SMTP if configured, or log to shared memory."""
        if not self.smtp_host or not self.smtp_user:
            # Fallback to in-app simulated dispatch
            self.memory.set(
                f"last_dispatched_email_{to_email}",
                {"to": to_email, "subject": subject, "body": body_text, "status": "simulated_sent"},
            )
            return True

        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_user
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body_text, "plain"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.smtp_user, to_email, msg.as_string())
            return True
        except Exception:
            return False


__all__ = ["NotificationAgent"]
