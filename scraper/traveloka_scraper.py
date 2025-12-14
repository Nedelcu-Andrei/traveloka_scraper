from playwright.sync_api import sync_playwright, TimeoutError
import logging

# Set logger
log = logging.getLogger(__name__)

READY = '[data-testid="overview_cheapest_price"]'  # <--- if price appears, we are ready
CAPTCHA = "#aws-captcha"                           # <--- if captcha appears, solve it & save session

class TravelokaScraper:
    def __init__(self, headless=False, profile="pw_profile"):
        log.info("Initializing Traveloka Scraper")
        self.headless = headless
        self.profile = profile
        self.playwright = None
        self.context = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            self.profile,
            headless=self.headless,
        )
        self.page = self.context.new_page()

    def goto_with_captcha_handling(self, url: str) -> None:
        """ If captcha is detected, solve it -> save to session, if already solved, scrape the page directly"""
        self.page.goto(url, wait_until="domcontentloaded")

        try:
            self.page.wait_for_selector(READY, state="visible", timeout=8000)
            log.info("Page ready, no captcha!")
        except TimeoutError:
            try:
                self.page.wait_for_selector(CAPTCHA, state="visible", timeout=5000)
                log.warning("Captcha detected — solve it, then Resume")
            except TimeoutError:
                log.error("Page not ready — inspect manually")

            # After manual solve
            self.page.goto(url, wait_until="domcontentloaded")
            self.page.wait_for_selector(READY, state="visible", timeout=15000)
            log.info("Page ready after captcha")

    def get_html(self) -> str:
        """ Return the html from the page """
        return self.page.content()

    def close(self):
        self.context.close()
        self.playwright.stop()














# def start_crawl(url: str):
#     with sync_playwright() as p:
#         context = p.chromium.launch_persistent_context(
#             "pw_profile",
#             headless=False,
#         )
#         page = context.new_page()
#
#         page.goto(url, wait_until="domcontentloaded")
#
#         try:
#             # if this appears, captcha is already solved
#             page.wait_for_selector(READY, state="visible", timeout=8000)
#             print("✅ Page ready (no captcha)")
#         except TimeoutError:
#             # likely captcha
#             try:
#                 page.wait_for_selector(CAPTCHA, state="visible", timeout=5000)
#                 print("🧩 Captcha detected — solve it, then Resume")
#             except TimeoutError:
#                 print("⚠️ Page not ready — inspect manually")
#
#             # page.pause()
#
#             # try again after manual solve
#             page.goto(url, wait_until="domcontentloaded")
#             page.wait_for_selector(READY, state="visible", timeout=15000)
#             print("✅ Page ready after captcha")
#
#         # test scrape
#         print("Value:", page.locator(READY).inner_text())
#
#         html_page = page.content()
#         context.close()
#
#         return html_page