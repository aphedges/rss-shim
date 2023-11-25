"""Paths to common directories and files."""

import os
from pathlib import Path

# High-level directories
DATA_DIR = Path(os.getenv("DATA_DIR", "data")).resolve()

# Data directories
CACHE_DIR = DATA_DIR / "cache"
FEED_DIR = DATA_DIR / "feeds"

# Automatically create directories
dirs = [
    CACHE_DIR,
    FEED_DIR,
]
for directory in dirs:
    directory.mkdir(parents=True, exist_ok=True)
