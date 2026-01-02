"""
Task Data Model

Represents a single todo item with ID, description, completion status, priority, tags, due date, and recurrence.
"""

from datetime import datetime
from typing import List, Optional
from .errors import InvalidTaskDescriptionError


class Priority:
    """
    Priority constants for tasks.
    """
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VALUES = [HIGH, MEDIUM, LOW]


class Recurrence:
    """
    Recurrence constants for tasks.
    """
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    VALUES = [DAILY, WEEKLY, MONTHLY]


class Task:
    """
    Represents a single todo item with the following attributes:
    - ID (unique identifier)
    - Description (text content)
    - Completion Status (boolean indicating if completed)
    - Priority (high/medium/low)
    - Tags (list of string labels)
    - Due Date (optional datetime for deadlines)
    """

    def __init__(self, task_id: int, description: str, completed: bool = False,
                 priority: str = Priority.MEDIUM, tags: List[str] = None,
                 due_date: Optional[datetime] = None, recurrence: Optional[str] = None):
        """
        Initialize a Task instance.

        Args:
            task_id (int): Unique identifier for the task
            description (str): Text content of the task
            completed (bool): Completion status, defaults to False
            priority (str): Priority level, defaults to "medium"
            tags (List[str]): List of tags, defaults to empty list
            due_date (Optional[datetime]): Due date, defaults to None
            recurrence (Optional[str]): Recurrence pattern, defaults to None
        """
        self._id = task_id
        self._description = description
        self._completed = completed
        self._priority = priority if priority in Priority.VALUES else Priority.MEDIUM
        self._tags = tags if tags is not None else []
        self._due_date = due_date
        self._recurrence = recurrence if recurrence in Recurrence.VALUES or recurrence is None else None

    @property
    def id(self) -> int:
        """Get the task ID."""
        return self._id

    @property
    def description(self) -> str:
        """Get the task description."""
        return self._description

    @description.setter
    def description(self, value: str):
        """Set the task description."""
        if not value or not value.strip():
            raise InvalidTaskDescriptionError()
        self._description = value

    @property
    def completed(self) -> bool:
        """Get the completion status."""
        return self._completed

    @completed.setter
    def completed(self, value: bool):
        """Set the completion status."""
        self._completed = value

    @property
    def priority(self) -> str:
        """Get the task priority."""
        return self._priority

    @priority.setter
    def priority(self, value: str):
        """Set the task priority."""
        if value not in Priority.VALUES:
            raise ValueError(f"Priority must be one of {Priority.VALUES}")
        self._priority = value

    @property
    def tags(self) -> List[str]:
        """Get the task tags."""
        return self._tags

    @tags.setter
    def tags(self, value: List[str]):
        """Set the task tags."""
        self._tags = value if value is not None else []

    @property
    def due_date(self) -> Optional[datetime]:
        """Get the task due date."""
        return self._due_date

    @due_date.setter
    def due_date(self, value: Optional[datetime]):
        """Set the task due date."""
        self._due_date = value

    @property
    def recurrence(self) -> Optional[str]:
        """Get the task recurrence pattern."""
        return self._recurrence

    @recurrence.setter
    def recurrence(self, value: Optional[str]):
        """Set the task recurrence pattern."""
        if value is not None and value not in Recurrence.VALUES:
            raise ValueError(f"Recurrence must be one of {Recurrence.VALUES} or None")
        self._recurrence = value

    def mark_completed(self):
        """Mark the task as completed."""
        self._completed = True

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self._completed = False

    def update_description(self, new_description: str):
        """
        Update the task description.

        Args:
            new_description (str): New description for the task
        """
        if not new_description or not new_description.strip():
            raise InvalidTaskDescriptionError()
        self._description = new_description

    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: Dictionary representation of the task
        """
        return {
            "id": self._id,
            "description": self._description,
            "completed": self._completed,
            "priority": self._priority,
            "tags": self._tags,
            "due_date": self._due_date.isoformat() if self._due_date else None,
            "recurrence": self._recurrence
        }

    def __repr__(self) -> str:
        """String representation of the task."""
        status = "Complete" if self._completed else "Incomplete"
        return f"Task(id={self._id}, description='{self._description}', status={status}, priority={self._priority}, tags={self._tags}, due_date={self._due_date}, recurrence={self._recurrence})"

    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        if self._due_date is None:
            return False
        from datetime import datetime
        return self._due_date.date() < datetime.now().date()

    def is_upcoming(self) -> bool:
        """Check if the task is due soon (within 24 hours)."""
        if self._due_date is None:
            return False
        from datetime import datetime, timedelta
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        return now.date() <= self._due_date.date() < tomorrow.date()

    def is_valid_recurrence(self, recurrence_value: Optional[str]) -> bool:
        """Check if a recurrence value is valid."""
        return recurrence_value is None or recurrence_value in Recurrence.VALUES

    def validate_recurrence(self, recurrence_value: Optional[str]):
        """Validate recurrence value and raise ValueError if invalid."""
        if recurrence_value is not None and recurrence_value not in Recurrence.VALUES:
            raise ValueError(f"Recurrence must be one of {Recurrence.VALUES} or None")

    def validate_due_date(self, due_date_value: Optional[datetime]):
        """Validate due date value - currently just checks if it's a datetime or None."""
        if due_date_value is not None and not isinstance(due_date_value, datetime):
            raise ValueError("Due date must be a datetime object or None")

    def __str__(self) -> str:
        """Human-readable string representation of the task."""
        status = "✓" if self._completed else "○"
        return f"[{status}] {self._id}: {self._description}"