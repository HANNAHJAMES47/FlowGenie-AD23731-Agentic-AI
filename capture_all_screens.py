import asyncio
import os
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

ARTIFACT_DIR = Path(r"C:\Users\HP\.gemini\antigravity-ide\brain\293e68df-2595-458a-b534-b34e277f675c")
OUTPUT_DIR = Path(r"d:\Agentic ai project\screenshots")
ARTIFACT_SCREENSHOTS_DIR = ARTIFACT_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

async def capture_perfect_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 1000},
            device_scale_factor=2,
        )
        page = await context.new_page()

        print("1. Loading FlowGenie Application...")
        await page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
        await asyncio.sleep(1)

        # ----------------------------------------------------
        # SCREENSHOT 1: Planning Console
        # ----------------------------------------------------
        print("Capturing 01_planning_console.png...")
        await page.select_option("#eventTimeSlot", "Morning (8:00 AM - 1:00 PM)")
        await page.fill("#eventStartTime", "08:00 AM")
        await page.fill("#guestCount", "150")
        await page.fill("#location", "Bangalore")
        await page.fill("#budget", "450000")
        await page.select_option("#cateringMealSlot", "Morning (Breakfast / Brunch / Morning Pooja)")
        await page.select_option("#cuisine", "South Indian")
        await page.select_option("#decorStyle", "Royal")
        await page.fill("#customNotes", "Need live acoustic Nadaswaram, traditional floral mandap, candid photography & drone footage")
        
        # Scroll to top smoothly
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(0.5)

        # Capture Planning Console hero + form
        form_card = await page.query_selector(".form-card-container")
        if form_card:
            # We hide the topbar temporarily or scroll so it doesn't overlap
            await page.evaluate("document.querySelector('.topbar').style.position = 'static'")
            await form_card.screenshot(path=str(OUTPUT_DIR / "01_planning_console.png"))
            await page.evaluate("document.querySelector('.topbar').style.position = 'sticky'")

        # ----------------------------------------------------
        # Trigger Multi-Agent AI Planning Execution
        # ----------------------------------------------------
        print("Submitting Multi-Agent Form...")
        submit_btn = await page.query_selector("#submitPromptBtn")
        if submit_btn:
            await submit_btn.click()

        # Wait for recommendation view to load
        await page.wait_for_selector("#recommendationView:not(.hidden)", timeout=35000)
        await asyncio.sleep(2)

        # ----------------------------------------------------
        # SCREENSHOT 2: Thought Console (Agent Activities & Decision Summaries)
        # ----------------------------------------------------
        print("Capturing 02_thought_console.png...")
        audit_details = await page.query_selector("details.audit-details")
        if audit_details:
            await page.evaluate("el => el.setAttribute('open', 'true')", audit_details)
            await asyncio.sleep(0.5)
            await page.evaluate("document.querySelector('.topbar').style.display = 'none'")
            await page.evaluate("document.querySelector('.bottom-bar')?.remove()")
            await audit_details.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            await audit_details.screenshot(path=str(OUTPUT_DIR / "02_thought_console.png"))
            await page.evaluate("document.querySelector('.topbar').style.display = 'flex'")

        # ----------------------------------------------------
        # SCREENSHOT 3: Vendor Deck (Interactive Vendor Cards)
        # ----------------------------------------------------
        print("Capturing 03_vendor_deck.png...")
        # Scroll to first category section (e.g. Venue & Mandap or Catering)
        first_category = await page.query_selector(".category-block") or await page.query_selector("#recommendationContent")
        if first_category:
            await page.evaluate("document.querySelector('.topbar').style.display = 'none'")
            # Remove sticky floating bar for clean screenshot
            await page.evaluate("""() => {
                const floatingBar = document.querySelector('.bottom-floating-bar') || document.querySelector('.floating-confirm-bar');
                if (floatingBar) floatingBar.style.display = 'none';
            }""")
            await first_category.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            await first_category.screenshot(path=str(OUTPUT_DIR / "03_vendor_deck.png"))
            await page.evaluate("document.querySelector('.topbar').style.display = 'flex'")

        # ----------------------------------------------------
        # SCREENSHOT 4: Schedule Editor (Hour-by-Hour Run-of-Show & Presets)
        # ----------------------------------------------------
        print("Capturing 04_schedule_editor.png...")
        schedule_card = await page.query_selector("#scheduleCustomizerCard")
        if schedule_card:
            await page.evaluate("document.querySelector('.topbar').style.display = 'none'")
            await schedule_card.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            await schedule_card.screenshot(path=str(OUTPUT_DIR / "04_schedule_editor.png"))
            await page.evaluate("document.querySelector('.topbar').style.display = 'flex'")

        # ----------------------------------------------------
        # SCREENSHOT 5: Sentinel Hub (Real-time Watchdog & Simulation)
        # ----------------------------------------------------
        print("Locking booking & capturing 05_sentinel_hub.png...")
        # Advance to Confirmed / Live Status
        await page.evaluate("""() => {
            if (typeof submitApproval === 'function') {
                submitApproval();
            }
        }""")
        await asyncio.sleep(2)

        # Switch to Live Status Tab
        await page.evaluate("""() => {
            showView('status');
            if (typeof loadSentinelAuditLogs === 'function') {
                loadSentinelAuditLogs(state.eventId || 'evt_default');
            }
        }""")
        await asyncio.sleep(1)

        # Trigger auto-recovery simulation
        sim_btn = await page.query_selector("#simulateAutoRecoverBtn")
        if sim_btn:
            await sim_btn.click()
            await asyncio.sleep(1.5)

        sentinel_card = await page.query_selector("#sentinelWatchdogCard")
        if sentinel_card:
            await page.evaluate("document.querySelector('.topbar').style.display = 'none'")
            await sentinel_card.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            await sentinel_card.screenshot(path=str(OUTPUT_DIR / "05_sentinel_hub.png"))
            await page.evaluate("document.querySelector('.topbar').style.display = 'flex'")

        # ----------------------------------------------------
        # SCREENSHOT 6: RFP Dispatcher (1-Click WhatsApp RFPs)
        # ----------------------------------------------------
        print("Capturing 06_rfp_dispatcher.png...")
        await page.evaluate("""() => {
            openRfpModal();
        }""")
        await asyncio.sleep(1.5)

        rfp_modal_card = await page.query_selector("#rfpModal .modal-card")
        if rfp_modal_card:
            await rfp_modal_card.screenshot(path=str(OUTPUT_DIR / "06_rfp_dispatcher.png"))
        else:
            await page.screenshot(path=str(OUTPUT_DIR / "06_rfp_dispatcher.png"))

        await browser.close()
        print("All 6 screenshots recaptured with perfect quality!")

        # Copy all screenshots to artifact directory
        for f in OUTPUT_DIR.glob("*.png"):
            shutil.copy2(f, ARTIFACT_SCREENSHOTS_DIR / f.name)
            print(f"Copied {f.name} to artifact directory")

if __name__ == "__main__":
    asyncio.run(capture_perfect_screenshots())
