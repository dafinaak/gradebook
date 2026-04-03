"""JSON file persistence for the gradebook application."""

import json
import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "gradebook.json"
)


def load_data(path: str = None) -> dict:
    """Load gradebook data from a JSON file.

    Args:
        path: Path to the JSON file. Defaults to DEFAULT_PATH.

    Returns:
        Dictionary with keys 'students', 'courses', 'enrollments'.
    """
    if path is None:
        path = DEFAULT_PATH
    empty = {"students": [], "courses": [], "enrollments": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info("Data loaded from %s", path)
        return data
    except FileNotFoundError:
        logger.info("No data file found at %s — starting empty.", path)
        return empty
    except json.JSONDecodeError as e:
        logger.error(
            "Corrupted JSON in %s: %s — starting empty.",
            path, e
        )
        print(
            f"Warning: Could not parse {path}"
            " (invalid JSON). Starting with empty data."
        )
        return empty


def save_data(data: dict, path: str = None) -> None:
    """Save gradebook data to a JSON file.

    Args:
        data: Dictionary with keys 'students', 'courses', 'enrollments'.
        path: Path to the JSON file. Defaults to DEFAULT_PATH.
    """
    if path is None:
        path = DEFAULT_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info("Data saved to %s", path)
    except OSError as e:
        logger.error("Failed to save data to %s: %s", path, e)
        raise
