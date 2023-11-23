"""A module for generating RSS feeds."""
import datetime as dt
from typing import Any
import xml.etree.ElementTree as ET

# Based on example code from https://docs.python.org/3.11/library/time.html#time.strftime
RFC822_FORMAT = "%a, %d %b %Y %H:%M:%S %z"


def to_rfc822_datetime(date: dt.datetime) -> str:
    """Convert datetime to RFC-822 formatted string.

    For example, "2023-11-22T00:00:00+00:00" would be
    formatted as "Wed, 22 Nov 2023 00:00:00 +0000".

    See https://datatracker.ietf.org/doc/html/rfc822#autoid-58 for more information.
    """
    return date.strftime(RFC822_FORMAT)


def generate_feed(feed_data: dict[str, Any]) -> str:
    """Generate an RSS 2.0 feed from properly formatted data.

    Args:
        feed_data: Data to format as RSS.

    Returns:
        Well-formed RSS.
    """
    xml_items = []
    for item in feed_data["items"]:
        xml_item = ET.Element("item")
        ET.SubElement(xml_item, "title").text = item["title"]
        ET.SubElement(xml_item, "description").text = item["description"]
        ET.SubElement(xml_item, "link").text = item["link"]
        ET.SubElement(xml_item, "guid", attrib={"isPermaLink": "true"}).text = item["link"]
        ET.SubElement(xml_item, "pubDate").text = to_rfc822_datetime(item["pubDate"])
        xml_items.append(xml_item)

    rss = ET.Element("rss", attrib={"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = feed_data["title"]
    ET.SubElement(channel, "description").text = feed_data["description"]
    ET.SubElement(channel, "link").text = feed_data["link"]
    ET.SubElement(channel, "copyright").text = feed_data["copyright"]
    ET.SubElement(channel, "lastBuildDate").text = feed_data["lastBuildDate"]
    ET.SubElement(channel, "pubDate").text = feed_data["pubDate"]
    ET.SubElement(channel, "ttl").text = feed_data["ttl"]
    channel.extend(xml_items)

    # Pretty print XML
    ET.indent(rss)
    rss_feed = ET.tostring(rss, encoding="unicode", xml_declaration=True)
    rss_feed += "\n"

    return rss_feed
