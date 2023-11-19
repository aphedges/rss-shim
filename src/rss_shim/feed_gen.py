"""A module for generating RSS feeds."""
from typing import Any


def generate_feed(feed_data: dict[str, Any]) -> str:
    """Generate an RSS 2.0 feed from properly formatted data.

    Args:
        feed_data: Data to format as RSS.

    Returns:
        Well-formed RSS.
    """
    xml_items = []
    for item in feed_data["items"]:
        xml_items.append(
            f"""
         <item>
      <id>{item['id']}</id>
      <title>{item['title']}</title>
      <description>{item['description']}</description>
      <link>{item['link']}</link>
      <pubDate>{item['pubDate']}</pubDate>
     </item>
     """
        )

    joined_items = "\n".join(xml_items)

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
     <title>{feed_data['title']}</title>
     <description>{feed_data['description']}</description>
     <link>{feed_data['link']}</link>
     <copyright>{feed_data['copyright']}</copyright>
     <lastBuildDate>{feed_data['lastBuildDate']}</lastBuildDate>
     <pubDate>{feed_data['pubDate']}</pubDate>
     <ttl>{feed_data['ttl']}</ttl>

     {joined_items}

    </channel>
    </rss>
    """
    return rss_feed
