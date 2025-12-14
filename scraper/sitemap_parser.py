import requests
import gzip
import io
import xml.etree.ElementTree as ET
import logging

#Set logger
log = logging.getLogger(__name__)


def download_and_parse_xml_gz(url: str) -> ET.Element:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    with gzip.GzipFile(fileobj=io.BytesIO(resp.content)) as gz:
        xml_bytes = gz.read()

    return ET.fromstring(xml_bytes)


def get_hotel_detail_sitemap_url(url: str) -> str:
    root = download_and_parse_xml_gz(url)

    for sitemap in root.findall("{*}sitemap"):
        loc = sitemap.find("{*}loc").text
        if "/sitemap/accommodation/hotel-detail/" in loc:
            return loc

    raise RuntimeError("No hotel-detail sitemap found")


def get_first_hotel_url(hotel_detail_sitemap_url: str) -> str:
    root = download_and_parse_xml_gz(hotel_detail_sitemap_url)

    for url in root.findall("{*}url"):
        loc = url.find("{*}loc").text
        return loc  # take only ONE hotel link

    raise RuntimeError("No hotel URLs found")


#-----------------------------------------------------
#----------------MAIN ENTRY POINT---------------------
#-----------------------------------------------------
def get_hotel_link_from_sitemap(base_sitemap: str ) -> str:
    hotel_detail_sitemap = get_hotel_detail_sitemap_url(base_sitemap)
    log.info("Hotel-detail sitemap: %s", hotel_detail_sitemap)

    hotel_url = get_first_hotel_url(hotel_detail_sitemap)
    log.info("Hotel initial URL: %s", hotel_url)

    return hotel_url