"""A module for generating RSS feeds."""
from dataclasses import dataclass, field
import datetime as dt
import importlib.metadata
import xml.etree.ElementTree as ET

from rss_shim.utils import now

# Based on example code from https://docs.python.org/3.11/library/time.html#time.strftime
RFC822_FORMAT = "%a, %d %b %Y %H:%M:%S %z"


def to_rfc822_datetime(date: dt.datetime) -> str:
    """Convert datetime to RFC-822 formatted string.

    For example, "2023-11-22T00:00:00+00:00" would be
    formatted as "Wed, 22 Nov 2023 00:00:00 +0000".

    See https://datatracker.ietf.org/doc/html/rfc822#autoid-58 for more information.
    """
    return date.strftime(RFC822_FORMAT)


@dataclass
class RssFeedItem:
    """Representation of an RSS 2.0 `<item>` element.

    For field descriptions, see https://www.rssboard.org/rss-specification.
    """

    title: str | None = None
    description: str | None = None
    link: str | None = None
    pub_date: dt.datetime | None = None

    def to_xml(self) -> ET.Element:
        """Generate an XML element."""
        xml_item = ET.Element("item")
        if self.title:
            ET.SubElement(xml_item, "title").text = self.title
        if self.description:
            ET.SubElement(xml_item, "description").text = self.description
        if self.link:
            ET.SubElement(xml_item, "link").text = self.link
            ET.SubElement(xml_item, "guid", attrib={"isPermaLink": "true"}).text = self.link
        if self.pub_date:
            ET.SubElement(xml_item, "pubDate").text = to_rfc822_datetime(self.pub_date)
        return xml_item


@dataclass
class RssFeed:
    """Representation of an RSS 2.0 `<rss>` element.

    For field descriptions, see https://www.rssboard.org/rss-specification.

    Most fields are automatically populated, but they can all be overridden.
    """

    title: str
    description: str
    link: str
    copyright: str | None = "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
    copyright_url: str | None = "https://creativecommons.org/publicdomain/zero/1.0/"
    docs: str | None = "https://www.rssboard.org/rss-specification"
    generator: str | None = f"{__package__} v{importlib.metadata.version(__package__)}"
    language: str | None = "en-us"
    last_build_date: dt.datetime | None = field(default_factory=now)
    pub_date: dt.datetime | None = None
    ttl: int | None = 30
    url: str | None = None
    items: list[RssFeedItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Initialize some fields dynamically."""
        if self.pub_date is None:
            item_pub_dates = [item.pub_date for item in self.items if item.pub_date]
            if item_pub_dates:
                self.pub_date = max(item_pub_dates)

    def to_xml(self) -> ET.Element:
        """Generate an XML element."""
        rss_attribs = {"version": "2.0"}
        if self.url:
            rss_attribs["xmlns:atom"] = "http://www.w3.org/2005/Atom"
        if self.copyright_url:
            rss_attribs[
                "xmlns:creativeCommons"
            ] = "http://backend.userland.com/creativeCommonsRssModule"
        xml_rss = ET.Element("rss", attrib=rss_attribs)
        channel = ET.SubElement(xml_rss, "channel")
        ET.SubElement(channel, "title").text = self.title
        ET.SubElement(channel, "description").text = self.description
        ET.SubElement(channel, "link").text = self.link
        if self.url:
            ET.SubElement(
                channel,
                "atom:link",
                attrib={"href": self.url, "rel": "self", "type": "application/rss+xml"},
            )
        if self.copyright:
            ET.SubElement(channel, "copyright").text = self.copyright
        if self.copyright_url:
            ET.SubElement(channel, "creativeCommons:license").text = self.copyright_url
        if self.docs:
            ET.SubElement(channel, "docs").text = self.docs
        if self.generator:
            ET.SubElement(channel, "generator").text = self.generator
        if self.language:
            ET.SubElement(channel, "language").text = self.language
        if self.last_build_date:
            ET.SubElement(channel, "lastBuildDate").text = to_rfc822_datetime(self.last_build_date)
        if self.pub_date:
            ET.SubElement(channel, "pubDate").text = to_rfc822_datetime(self.pub_date)
        if self.ttl:
            ET.SubElement(channel, "ttl").text = str(self.ttl)
        if self.items:
            xml_items = [item.to_xml() for item in self.items]
            channel.extend(xml_items)

        return xml_rss
