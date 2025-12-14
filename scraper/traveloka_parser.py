from typing import List, Dict, Any
from urllib.parse import quote
from lxml import html
import json
from datetime import datetime
import logging

# Set logger
log = logging.getLogger(__name__)

class TravelokaParser:
    def extract_hotel_uri_parts(self, hotel_url: str) -> dict[str, str]:
        """ Extract reusable URI components from a Traveloka hotel URL."""
        log.info("Extracting reusable URI components from Traveloka URL")

        path_parts = hotel_url.split("/")

        if len(path_parts) < 3:
            raise ValueError("Invalid Traveloka hotel URL")

        base_url = path_parts[0] + "//" +  path_parts[2] + "/" +  path_parts[3] + "/" + path_parts[4] + "/"

        locale = path_parts[3]

        hotel_slug = path_parts[-1]
        hotel_id = hotel_slug.split("-")[-1]

        hotel_name_slug = "-".join(hotel_slug.split("-")[:-1])
        hotel_name = hotel_name_slug.replace("-", " ").title()

        return {
            "base_url": base_url,
            "locale": locale,
            "hotel_id": hotel_id,
            "hotel_name": hotel_name,
        }


    def build_deep_link(self, uri_paths: dict[str, str], check_in: str, check_out: str, adults: str, rooms: str) -> str:
        """ Build a Traveloka deep-link URL for a hotel detail page to also include desired details. """
        log.info("Building Traveloka deep-link URL")

        # Calculate number of nights
        d_in = datetime.strptime(check_in, "%d-%m-%Y")
        d_out = datetime.strptime(check_out, "%d-%m-%Y")
        nights = (d_out - d_in).days

        if nights <= 0:
            raise ValueError("Checkout date must be after checkin date")

        # Build custom spec from inputs
        spec = (
                f"{check_in}.{check_out}."
                f"{adults}.{rooms}.HOTEL."
                f"{uri_paths["hotel_id"]}.{quote(uri_paths["hotel_name"])}.{adults}"
        )

        return f"{uri_paths["base_url"]}detail?spec={spec}"



    def parse_hotel_info(self, html_data: str, page_url: str) -> None:
        """ Parse hotel rooms details and pricing information from HTML. """
        log.info("Parsing Traveloka hotel details")

        if not html_data:
            log.error("Empty HTML data received — skipping parse")
            return

        response = html.fromstring(html_data) # load str html page as lxml for xpath parsing
        rooms_data: List[Dict[str, Any]] = []

        all_rooms = response.xpath('//*[@data-testid="room-list-tray"]/div')
        if not all_rooms:
            log.warning("No rooms found on page")
            return

        # Details from page level
        room_guests_num = page_url.split(".")[-1]
        rate_name = xpath_attr(response, '//*[@data-testid="price-display-config-selector"]/@value')

        for i, room in enumerate(all_rooms):
            # Room details
            room_name = xpath_text(room, './/*[starts-with(@data-testid, "room-name-")]/text()')
            breakfast = xpath_text(room, './/*[@data-testid="room_inventory_breakfast"]/text()')
            cancellation_policy = xpath_text(room, './/*[@data-testid="text_cancellation_policy"]/text()')

            # Prices
            room_original_price = xpath_text(room, './/*[starts-with(@data-testid, "inv-original-rate-")]/text()').split(" ")[-1]
            room_price_shown = xpath_text(room, './/*[@data-testid="room_inventory_cheapest_rate"]/text()').split(" ")[-1]

            room_total_price_without_tax = response.xpath('//*[contains(text(),"Price excluding tax")]/following::div[1]/text()')[i].split(" ")[-1]
            room_total_price_per_stay = response.xpath('//*[contains(text(),"Total payment")]/following::div[1]/text()')[i].split(" ")[-1]
            shown_currency = xpath_text(response, './/*[starts-with(@data-testid, "inv-original-rate-")]/text()').split(" ")[0]

            # Taxes related details
            total_sum = float(room_total_price_per_stay.split(" ")[-1])
            total_without_tax = float(room_total_price_without_tax.split(" ")[-1])
            total_taxes = str(round((total_sum - total_without_tax), 2))

            room_data = {
                "room_name": room_name,
                "rate_name": rate_name,
                "shown_currency": shown_currency,
                "shown_price": {
                    "rate_name": rate_name,
                },
                "net_price": room_price_shown,
                "cancellation_policy": cancellation_policy,
                "breakfast": breakfast,
                "number_of_guests": room_guests_num,
                "taxes_amount": total_taxes,
                "total_price": room_total_price_per_stay,
                "original_price": room_original_price,
                "shown_price_per_stay": room_total_price_without_tax,
                "net_price_per_stay": room_total_price_without_tax,
                "total_price_per_stay": room_total_price_per_stay,
            }
            rooms_data.append(room_data)

        self.save_json(rooms_data)

    def save_json(self, data: List[Dict[str, Any]], filename: str = "rates.json") -> None:
        """ Save parsed data to a JSON file. """
        log.info("Saving parsed data to JSON file")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


#--------------HELPER METHODS for default values to not bloat the code ---------------
def xpath_text(node, xpath: str, default: str = "") -> str:
    """Return first XPath text result or a default."""
    result = node.xpath(xpath)
    return result[0].strip() if result else default


def xpath_attr(node, xpath: str, default: str = "") -> str:
    """Return first XPath attribute value or a default."""
    result = node.xpath(xpath)
    return result[0] if result else default

