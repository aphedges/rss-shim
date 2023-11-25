"""Handling of deployment-specific settings."""

import os

FEED_URL_ORIGIN = os.getenv("FEED_URL_ORIGIN", "https://example.org")
# Needed for `urljoin()` to work properly
if FEED_URL_ORIGIN and not FEED_URL_ORIGIN.endswith("/"):
    FEED_URL_ORIGIN += "/"
