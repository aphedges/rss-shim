"""Abstract base class for shims."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any
import urllib.parse

from rss_shim.config import FEED_URL_ORIGIN
from rss_shim.feed_gen import RssFeed
from rss_shim.paths import CACHE_DIR, FEED_DIR
from rss_shim.utils import get_logger, pretty_print_xml

logger = get_logger(__name__)


@dataclass
class BaseShim(ABC):
    """Abstract base class for shims."""

    def __post_init__(self) -> None:
        """Initialize filesystem for shim."""
        self.init_files()

    @property
    @abstractmethod
    def shim_path(self) -> str:
        """Location for files within the data directory."""
        raise NotImplementedError

    @property
    def cache_file(self) -> Path:
        """JSON cache file path."""
        return CACHE_DIR / f"{self.shim_path}.json"

    @property
    def feed_file(self) -> Path:
        """RSS 2.0 feed file path."""
        return FEED_DIR / f"{self.shim_path}.rss"

    @property
    def feed_url(self) -> str | None:
        """URL feed will be served at."""
        if FEED_URL_ORIGIN:
            return urllib.parse.urljoin(FEED_URL_ORIGIN, str(self.feed_file.relative_to(FEED_DIR)))
        else:
            return None

    def init_files(self) -> None:
        """Initialize directories that files will be stored in."""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.feed_file.parent.mkdir(parents=True, exist_ok=True)

    def load_cache(self) -> Any:
        """Load cache data from cache file.

        Returns:
            Deserialized JSON contents of the cache file.
        """
        if self.cache_file.is_file():
            return json.loads(self.cache_file.read_text(encoding="utf-8"))
        else:
            return None

    @abstractmethod
    def generate_feed(self) -> RssFeed:
        """Generate an RSS feed, retrieving data as needed.

        Returns:
            An instantiated RssFeed object.
        """
        raise NotImplementedError

    def run(self) -> None:
        """Generate an RSS feed and write it to the disk."""
        try:
            feed = self.generate_feed()
            rss_text = pretty_print_xml(feed.to_xml())
            self.feed_file.write_text(rss_text, encoding="utf-8")
        except Exception:  # pylint: disable=broad-exception-caught
            logger.exception("Scraping failed with error:")
