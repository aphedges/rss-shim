"""Paths to common directories and files."""

import os
from pathlib import Path

# High-level directories
DATA_DIR = Path(os.getenv("DATA_DIR", "data")).resolve()

# Automatically create directories
dirs = [
    DATA_DIR,
]
for directory in dirs:
    directory.mkdir(parents=True, exist_ok=True)
