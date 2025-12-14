import logging

from scraper.traveloka_scraper import TravelokaScraper
from scraper.traveloka_parser import TravelokaParser
from scraper.sitemap_parser import get_hotel_link_from_sitemap
from logging_config import setup_logging

setup_logging()
log = logging.getLogger(__name__)


if __name__ == "__main__":
    log.info("Starting...")
    BASE_SITEMAP = "https://www.traveloka.com/en-en/sitemap/index.xml.gz"  # <-- Starting link

    # STEP 1 --> Scrape sitemap URL for hotels details page and extract first hotel url
    parser = TravelokaParser()

    hotel_link = get_hotel_link_from_sitemap(BASE_SITEMAP)
    hotel_link_paths = parser.extract_hotel_uri_parts(hotel_link)
    final_deeplink = parser.build_deep_link(uri_paths=hotel_link_paths, check_in="16-12-2025", check_out="18-12-2025", adults="2",
                                            rooms="1") # <--- Input here any desired parameter for the hotel details.

    # STEP 2 ---> Scrape the hotel detail page with Playwright and get all the HTML data
    scraper = TravelokaScraper(headless=False)
    scraper.start()
    scraper.goto_with_captcha_handling(final_deeplink)
    html_page = scraper.get_html()
    scraper.close()

    # STEP 3 ---> Parse all the rooms data and save it to a json file
    parser.parse_hotel_info(html_page, final_deeplink)

    log.info(f"Scraping completed successfully. Saved to rates.json\nPAGE LINK: {final_deeplink}")