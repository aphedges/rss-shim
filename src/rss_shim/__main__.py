"""A service to create RSS feeds for sites that do not support them."""
import random
import time

from rss_shim.shims import ComicsKingdomShim
from rss_shim.utils import get_logger

logger = get_logger(__name__)


def main() -> None:
    """Scrape sites repeatedly, handling errors and waiting as needed."""
    shims = [
        ComicsKingdomShim("rae-the-doe", "Rae the Doe"),
    ]
    while True:
        for shim in shims:
            shim.run()
        sleep_time = int((30 + random.uniform(-2, 2)) * 60)
        logger.info("Sleeping for %d seconds", sleep_time)
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
