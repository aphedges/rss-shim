"""Shim for Comics Kingdom, a comic strip syndication platform."""
from dataclasses import dataclass, field
import datetime as dt
import urllib.parse

from bs4 import BeautifulSoup
import requests

from rss_shim.feed_gen import RssFeed, RssFeedItem
from rss_shim.shims.base_shim import BaseShim
from rss_shim.utils import get_logger, write_json

logger = get_logger(__name__)


@dataclass
class ComicsKingdomShim(BaseShim):
    """Shim for Comics Kingdom, a comic strip syndication platform."""

    comic_id: str
    comic_name: str
    seen_urls: list[str] = field(init=False)

    def __post_init__(self) -> None:
        """Load data from cache file."""
        super().__post_init__()
        cache = self.load_cache()
        self.seen_urls = cache if cache is not None else []

    @property
    def shim_path(self) -> str:
        """Location for files within the data directory."""
        return f"comics_kingdom/{self.comic_id.replace('-', '_')}"

    @property
    def comic_url(self) -> str:
        """URL comic is available at."""
        return urllib.parse.urljoin("https://comicskingdom.com/", self.comic_id)

    def generate_feed(self) -> RssFeed:
        """Generate an RSS feed, retrieving data as needed.

        Returns:
            An instantiated RssFeed object.
        """
        logger.info("Seen URLs: %s", self.seen_urls)
        response = requests.get(self.comic_url, timeout=30)
        response.raise_for_status()
        page_text = response.text
        # Parse URL from `<link rel="canonical" href="https://comicskingdom.com/rae-the-doe/2023-03-08" />`
        soup = BeautifulSoup(page_text, features="html.parser")
        canonical_urls = [
            link["href"] for link in soup.find_all("link", attrs={"rel": "canonical"})
        ]
        if len(set(canonical_urls)) > 1:
            logger.warning("Multiple canonical URLs found: %s", canonical_urls)
        comic_strip_url = canonical_urls[0]
        if comic_strip_url not in self.seen_urls:
            logger.info("Found new URL: %s", repr(comic_strip_url))
            self.seen_urls.insert(0, comic_strip_url)
            write_json(self.seen_urls, self.cache_file)

        items = []
        for url in self.seen_urls[:10]:
            pub_date = dt.datetime.strptime(url[-10:], "%Y-%m-%d")
            pub_date = pub_date.replace(tzinfo=dt.UTC)
            items.append(
                RssFeedItem(
                    title=f"{self.comic_name} {url[-10:]}",
                    link=url,
                    pub_date=pub_date,
                )
            )

        feed = RssFeed(
            title=self.comic_name,
            description=f"Recent comic strips for {self.comic_name}",
            link=self.comic_url,
            url=self.feed_url,
            items=items,
        )
        return feed
