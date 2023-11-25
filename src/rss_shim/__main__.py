"""A service to create RSS feeds for sites that do not support them."""
import random
import time

from rss_shim.shims import ComicsKingdomShim
from rss_shim.utils import get_logger, pretty_print_xml

logger = get_logger(__name__)


def scrape_comic() -> None:
    """Scrape _Rae the Doe_ and generate an RSS feed for it."""
    shim = ComicsKingdomShim("rae-the-doe", "Rae the Doe")
    feed = shim.generate_feed()
    rss_text = pretty_print_xml(feed.to_xml())
    shim.feed_file.write_text(rss_text, encoding="utf-8")


def main() -> None:
    """Scrape sites repeatedly, handling errors and waiting as needed."""
    while True:
        try:
            scrape_comic()
        except Exception:  # pylint: disable=broad-exception-caught
            logger.exception("Scraping failed with error:")
        sleep_time = int((30 + random.uniform(-2, 2)) * 60)
        logger.info("Sleeping for %d seconds", sleep_time)
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
