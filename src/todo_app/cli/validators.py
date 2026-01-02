"""
Input Validators

Handles validation for user input including priority, tags, and dates.
"""

from datetime import datetime
from typing import List


def validate_priority(priority: str) -> str:
    """
    Validate priority value.

    Args:
        priority (str): Priority value to validate

    Returns:
        str: Validated priority value

    Raises:
        ValueError: If priority is not one of the allowed values
    """
    from ..core.task import Priority

    if priority not in Priority.VALUES:
        raise ValueError(f"Priority must be one of: {', '.join(Priority.VALUES)}")
    return priority


def validate_tags(tags: List[str]) -> List[str]:
    """
    Validate tags list.

    Args:
        tags (List[str]): List of tags to validate

    Returns:
        List[str]: Validated list of tags

    Raises:
        ValueError: If any tag contains commas or is empty after stripping
    """
    validated_tags = []
    for tag in tags:
        if tag.strip():  # Non-empty after stripping whitespace
            if ',' in tag:
                raise ValueError(f"Tag cannot contain commas: {tag}")
            validated_tags.append(tag.strip())
    return validated_tags


def validate_date(date_str: str) -> datetime:
    """
    Validate date string in ISO format.

    Args:
        date_str (str): Date string to validate

    Returns:
        datetime: Parsed datetime object

    Raises:
        ValueError: If date string is not in valid ISO format
    """
    try:
        # Try parsing as YYYY-MM-DD format
        return datetime.fromisoformat(date_str)
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD format.")