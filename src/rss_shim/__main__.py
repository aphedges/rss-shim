"""A service to create RSS feeds for sites that do not support them."""
import json
import random
import time

import requests

from rss_shim.feed_gen import generate_feed
from rss_shim.paths import DATA_DIR

CACHE_FILE = DATA_DIR / "cache.json"
FEED_FILE = DATA_DIR / "feed.rss"

if CACHE_FILE.is_file():
    seen_urls = json.load(open(CACHE_FILE, encoding="utf-8"))
else:
    seen_urls = []


def scrape_comic() -> None:
    """Scrape _Rae the Doe_ and generate an RSS feed for it."""
    print(seen_urls)
    page_text = requests.get("https://comicskingdom.com/rae-the-doe", timeout=30).text
    # maybe switch to `<link rel="canonical" href="https://comicskingdom.com/rae-the-doe/2023-03-08" />` instead of `<meta property="og:url" content='https://comicskingdom.com/rae-the-doe/2023-03-08' />`
    target_tag = [
        line for line in page_text.splitlines() if line.startswith('<meta property="og:url"')
    ][0]
    comic_url = target_tag[target_tag.find("'") + 1 : target_tag.rfind("'")]
    if comic_url not in seen_urls:
        print(f"Found new URL: {comic_url!r}")
        seen_urls.insert(0, comic_url)
        json.dump(seen_urls, open(CACHE_FILE, "w", encoding="utf-8"))

    items = []
    for url in seen_urls[:10]:
        items.append(
            {
                "id": f"Rae the Doe {url[-10:]}",
                "title": f"Rae the Doe {url[-10:]}",
                "description": "Here is some text containing an interesting description.",
                "link": url,
                "pubDate": url[-10:],
            }
        )

    feed_data = {
        "title": "Rae the Doe",
        "description": "This is an example of an RSS feed",
        "link": "https://comicskingdom.com/rae-the-doe",
        "copyright": "2020 Example.com All rights reserved",
        "lastBuildDate": "Mon, 6 Sep 2010 00:01:00 +0000",
        "pubDate": "Sun, 6 Sep 2009 16:20:00 +0000",
        "ttl": "1800",
        "items": items,
    }
    rss_feed = generate_feed(feed_data)
    open(FEED_FILE, "w", encoding="utf-8").write(rss_feed)


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