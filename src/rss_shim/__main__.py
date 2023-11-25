"""A service to create RSS feeds for sites that do not support them."""
import datetime as dt
import json
import random
import time
import urllib.parse

from bs4 import BeautifulSoup
import requests

from rss_shim.config import FEED_URL_ORIGIN
from rss_shim.feed_gen import RssFeed, RssFeedItem
from rss_shim.paths import DATA_DIR
from rss_shim.utils import pretty_print_xml

CACHE_FILE = DATA_DIR / "cache.json"
FEED_FILE = DATA_DIR / "feed.rss"

if CACHE_FILE.is_file():
    seen_urls = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
else:
    seen_urls = []


def scrape_comic() -> None:
    """Scrape _Rae the Doe_ and generate an RSS feed for it."""
    print(seen_urls)
    page_text = requests.get("https://comicskingdom.com/rae-the-doe", timeout=30).text
    # Parse URL from `<link rel="canonical" href="https://comicskingdom.com/rae-the-doe/2023-03-08" />`
    soup = BeautifulSoup(page_text, features="html.parser")
    canonical_urls = [link["href"] for link in soup.findAll("link", attrs={"rel": "canonical"})]
    if len(set(canonical_urls)) > 1:
        print(f"WARNING! Multiple canonical URLs found: {canonical_urls}")
    comic_url = canonical_urls[0]
    if comic_url not in seen_urls:
        print(f"Found new URL: {comic_url!r}")
        seen_urls.insert(0, comic_url)
        CACHE_FILE.write_text(json.dumps(seen_urls), encoding="utf-8")

    items = []
    for url in seen_urls[:10]:
        pub_date = dt.datetime.strptime(url[-10:], "%Y-%m-%d")
        pub_date = pub_date.replace(tzinfo=dt.UTC)
        items.append(
            RssFeedItem(
                title=f"Rae the Doe {url[-10:]}",
                link=url,
                pub_date=pub_date,
            )
        )

    feed = RssFeed(
        title="Rae the Doe",
        description="Recent comic strips for Rae the Doe",
        link="https://comicskingdom.com/rae-the-doe",
        url=urllib.parse.urljoin(FEED_URL_ORIGIN, "feed.rss"),
        items=items,
    )
    rss_text = pretty_print_xml(feed.to_xml())
    FEED_FILE.write_text(rss_text, encoding="utf-8")


def main() -> None:
    """Scrape sites repeatedly, handling errors and waiting as needed."""
    while True:
        try:
            scrape_comic()
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(f"Scraping failed with error: {ex}")
        sleep_time = int((30 + random.uniform(-2, 2)) * 60)
        print(sleep_time)
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
