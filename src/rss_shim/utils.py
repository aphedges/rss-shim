"""General utilities to make programming easier."""

import datetime as dt
import json
import logging
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

LOGGING_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Returns a logger with the desired configuration.

    Args:
        name: Name of logger.

    Returns:
        A logger.
    """
    logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger


def now() -> dt.datetime:
    """Retrieve the current date and time."""
    # Always use UTC as time zone because `datetime.now()`
    # returns "naive" (non-TZ-aware) `datetime`s
    return dt.datetime.now(dt.UTC)


def pretty_print_xml(xml: ET.Element) -> str:
    """Convert an XML element to well-formatted text."""
    ET.indent(xml)
    xml_text = ET.tostring(xml, encoding="unicode", xml_declaration=True)
    xml_text += "\n"
    return xml_text


def write_json(obj: Any, filename: Path, **kwargs: Any) -> None:
    """Dump JSON value into file.

    Args:
        obj: JSON-serializable object to write to file.
        filename: Path to file.
        kwargs: Additional parameters to pass to `json.dumps()`.
    """
    output = json.dumps(obj, ensure_ascii=False, indent=2, **kwargs) + "\n"
    filename.write_text(output, encoding="utf-8")
