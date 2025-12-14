import logging

from scraper.traveloka_scraper import TravelokaScraper
from scraper.traveloka_parser import TravelokaParser
from scraper.sitemap_parser import get_hotel_link_from_sitemap
from logging_config import setup_logging

setup_logging()
log = logging.getLogger(__name__)


if __name__ == "__main__":
    # NOTE: Designed for single-hotel scrape; easily extendable to batch mode

    log.info("Starting...")
    BASE_SITEMAP = "https://www.traveloka.com/en-en/sitemap/index.xml.gz"  # <-- Starting link

# Configurable parameters for the rooms details
    CHECK_IN = "16-12-2025"
    CHECK_OUT = "18-12-2025"
    ADULTS = "2"
    ROOMS = "1"

    # Step 1: Extract a hotel detail URL from the sitemap
    parser = TravelokaParser()

    hotel_link = get_hotel_link_from_sitemap(BASE_SITEMAP)
    hotel_link_paths = parser.extract_hotel_uri_parts(hotel_link)
    final_deeplink = parser.build_deep_link(uri_paths=hotel_link_paths,
                                            check_in=CHECK_IN,
                                            check_out=CHECK_OUT,
                                            adults=ADULTS,
                                            rooms=ROOMS)

    # Step 2: Render hotel page, handle captcha if present, scrape the HTML
    scraper = TravelokaScraper(headless=False)
    scraper.start()
    scraper.goto_with_captcha_handling(final_deeplink)
    html_page = scraper.get_html()
    scraper.close()

    # Step 3: Parse the rooms data and save it to a json file
    parser.parse_hotel_info(html_page, final_deeplink)

    log.info(f"Scraping completed successfully" ""
             "Saved to rates.json | PAGE LINK: {final_deeplink}")