"""
Date Utilities Module

Provides utility functions for date calculations, particularly for handling
task recurrence patterns (daily, weekly, monthly) and due date comparisons.
"""

from datetime import datetime, timedelta
from typing import Optional
from .task import Recurrence


def calculate_next_occurrence(
    current_date: datetime,
    recurrence_pattern: str
) -> Optional[datetime]:
    """
    Calculate the next occurrence date based on the recurrence pattern.

    Args:
        current_date (datetime): The current occurrence date
        recurrence_pattern (str): The recurrence pattern ('daily', 'weekly', 'monthly')

    Returns:
        Optional[datetime]: The next occurrence date, or None if pattern is invalid
    """
    if recurrence_pattern == Recurrence.DAILY:
        return current_date + timedelta(days=1)
    elif recurrence_pattern == Recurrence.WEEKLY:
        return current_date + timedelta(weeks=1)
    elif recurrence_pattern == Recurrence.MONTHLY:
        # Calculate next month, handling month-end dates appropriately
        return _add_months(current_date, 1)
    else:
        return None


def _add_months(date: datetime, months: int) -> datetime:
    """
    Add months to a date, handling month-end dates appropriately.

    Args:
        date (datetime): The starting date
        months (int): Number of months to add

    Returns:
        datetime: The resulting date after adding months
    """
    import calendar

    # Get the target month and year
    target_month = date.month + months
    target_year = date.year + (target_month - 1) // 12
    target_month = ((target_month - 1) % 12) + 1

    # Handle month-end dates (e.g., Jan 31 -> Feb 28/29)
    max_day_in_target_month = calendar.monthrange(target_year, target_month)[1]
    target_day = min(date.day, max_day_in_target_month)

    return date.replace(year=target_year, month=target_month, day=target_day)


def is_overdue(due_date: Optional[datetime]) -> bool:
    """
    Check if a due date is overdue.

    Args:
        due_date (Optional[datetime]): The due date to check

    Returns:
        bool: True if the due date is in the past, False otherwise
    """
    if due_date is None:
        return False
    return due_date.date() < datetime.now().date()


def is_upcoming(due_date: Optional[datetime]) -> bool:
    """
    Check if a due date is upcoming (within 24 hours).

    Args:
        due_date (Optional[datetime]): The due date to check

    Returns:
        bool: True if the due date is within 24 hours from now, False otherwise
    """
    if due_date is None:
        return False
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    return now.date() <= due_date.date() < tomorrow.date()


def format_date_for_display(date: Optional[datetime]) -> str:
    """
    Format a date for display in the CLI.

    Args:
        date (Optional[datetime]): The date to format

    Returns:
        str: Formatted date string or empty string if date is None
    """
    if date is None:
        return ""
    return date.strftime("%Y-%m-%d")


def parse_date_string(date_string: str) -> Optional[datetime]:
    """
    Parse a date string in YYYY-MM-DD format to a datetime object.

    Args:
        date_string (str): Date string in YYYY-MM-DD format

    Returns:
        Optional[datetime]: Parsed datetime object or None if invalid
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return None