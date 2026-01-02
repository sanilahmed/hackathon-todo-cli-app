"""
Unit tests for Task functionality.
"""
import pytest
from datetime import datetime, timedelta
from src.todo_app.core.task import Task, Priority, Recurrence
from src.todo_app.core.errors import InvalidTaskDescriptionError


class TestTask:
    """Tests for the Task class."""

    def test_create_task(self):
        """Test creating a task with valid parameters."""
        task = Task(1, "Test description", False)
        assert task.id == 1
        assert task.description == "Test description"
        assert task.completed is False
        assert task.priority == Priority.MEDIUM  # Default priority
        assert task.tags == []  # Default tags
        assert task.due_date is None  # Default due_date

        # Test with completed=True
        task2 = Task(2, "Another task", True)
        assert task2.id == 2
        assert task2.description == "Another task"
        assert task2.completed is True
        assert task2.priority == Priority.MEDIUM  # Default priority
        assert task2.tags == []  # Default tags
        assert task2.due_date is None  # Default due_date

    def test_create_task_with_priority_tags_due_date(self):
        """Test creating a task with priority, tags, and due_date."""
        due_date = datetime(2023, 12, 25)
        task = Task(1, "Test task", False, priority=Priority.HIGH,
                   tags=["work", "urgent"], due_date=due_date)

        assert task.id == 1
        assert task.description == "Test task"
        assert task.completed is False
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "urgent"]
        assert task.due_date == due_date

    def test_create_task_default_priority_assignment(self):
        """Test default priority assignment when not specified."""
        task = Task(1, "Test task", False)
        assert task.priority == Priority.MEDIUM

        # Test with explicit None
        task2 = Task(2, "Test task", False, priority=None)
        assert task2.priority == Priority.MEDIUM

    def test_task_properties(self):
        """Test task property getters and setters."""
        from datetime import datetime
        due_date = datetime(2023, 12, 25)
        task = Task(1, "Test task", False, priority=Priority.HIGH,
                   tags=["work", "urgent"], due_date=due_date)

        # Test ID is read-only
        assert task.id == 1

        # Test description setter
        task.description = "New description"
        assert task.description == "New description"

        # Test completed setter
        task.completed = True
        assert task.completed is True

        task.completed = False
        assert task.completed is False

        # Test priority setter
        task.priority = Priority.LOW
        assert task.priority == Priority.LOW

        # Test tags setter
        task.tags = ["home", "personal"]
        assert task.tags == ["home", "personal"]

        # Test due_date setter
        new_due_date = datetime(2024, 1, 1)
        task.due_date = new_due_date
        assert task.due_date == new_due_date

    def test_to_dict_with_priority_tags_due_date(self):
        """Test to_dict method with priority, tags, and due_date."""
        from datetime import datetime
        due_date = datetime(2023, 12, 25)
        task = Task(1, "Test description", True, priority=Priority.HIGH,
                   tags=["work", "urgent"], due_date=due_date)
        task_dict = task.to_dict()

        expected = {
            "id": 1,
            "description": "Test description",
            "completed": True,
            "priority": Priority.HIGH,
            "tags": ["work", "urgent"],
            "due_date": "2023-12-25T00:00:00",  # ISO format string from to_dict method
            "recurrence": None  # New field added to to_dict
        }

        assert task_dict == expected

    def test_description_setter_validation(self):
        """Test that setting empty descriptions raises error."""
        task = Task(1, "Valid description", False)

        with pytest.raises(InvalidTaskDescriptionError):
            task.description = ""

        with pytest.raises(InvalidTaskDescriptionError):
            task.description = "   "

    def test_update_description_method(self):
        """Test update_description method."""
        task = Task(1, "Original description", False)

        task.update_description("New description")
        assert task.description == "New description"

    def test_update_description_validation(self):
        """Test that updating to empty descriptions raises error."""
        task = Task(1, "Valid description", False)

        with pytest.raises(InvalidTaskDescriptionError):
            task.update_description("")

        with pytest.raises(InvalidTaskDescriptionError):
            task.update_description("   ")

    def test_mark_completed(self):
        """Test mark_completed method."""
        task = Task(1, "Test task", False)
        assert task.completed is False

        task.mark_completed()
        assert task.completed is True

    def test_mark_incomplete(self):
        """Test mark_incomplete method."""
        task = Task(1, "Test task", True)
        assert task.completed is True

        task.mark_incomplete()
        assert task.completed is False

    def test_to_dict(self):
        """Test to_dict method."""
        task = Task(1, "Test description", True)
        task_dict = task.to_dict()

        expected = {
            "id": 1,
            "description": "Test description",
            "completed": True,
            "priority": Priority.MEDIUM,  # Default priority
            "tags": [],  # Default tags
            "due_date": None,  # Default due_date
            "recurrence": None  # New field added to to_dict
        }

        assert task_dict == expected

    def test_repr(self):
        """Test string representation."""
        task = Task(1, "Test description", True)
        repr_str = repr(task)
        assert "id=1" in repr_str
        assert "Test description" in repr_str
        assert "Complete" in repr_str

        task2 = Task(2, "Test description", False)
        repr_str2 = repr(task2)
        assert "Incomplete" in repr_str2

    def test_str(self):
        """Test human-readable string representation."""
        task = Task(1, "Test description", True)
        str_repr = str(task)
        assert "✓" in str_repr
        assert "1:" in str_repr
        assert "Test description" in str_repr

        task2 = Task(2, "Test description", False)
        str_repr2 = str(task2)
        assert "○" in str_repr2
        assert "2:" in str_repr2

    def test_task_creation_with_recurrence(self):
        """Test creating a task with recurrence attribute."""
        task = Task(1, "Test task", recurrence=Recurrence.DAILY)
        assert task.recurrence == Recurrence.DAILY

    def test_task_creation_without_recurrence(self):
        """Test creating a task without recurrence attribute."""
        task = Task(1, "Test task")
        assert task.recurrence is None

    def test_task_recurrence_property_setter(self):
        """Test setting recurrence via property setter."""
        task = Task(1, "Test task")
        task.recurrence = Recurrence.WEEKLY
        assert task.recurrence == Recurrence.WEEKLY

    def test_task_recurrence_property_setter_invalid(self):
        """Test setting invalid recurrence raises ValueError."""
        task = Task(1, "Test task")
        with pytest.raises(ValueError):
            task.recurrence = "yearly"

    def test_task_recurrence_property_setter_none(self):
        """Test setting recurrence to None."""
        task = Task(1, "Test task", recurrence=Recurrence.DAILY)
        assert task.recurrence == Recurrence.DAILY
        task.recurrence = None
        assert task.recurrence is None

    def test_task_to_dict_includes_recurrence(self):
        """Test that to_dict method includes recurrence field."""
        task = Task(1, "Test task", recurrence=Recurrence.MONTHLY)
        task_dict = task.to_dict()
        assert "recurrence" in task_dict
        assert task_dict["recurrence"] == Recurrence.MONTHLY

    def test_is_overdue_with_past_due_date(self):
        """Test is_overdue returns True for past due dates."""
        past_date = datetime.now() - timedelta(days=1)
        task = Task(1, "Test task", due_date=past_date)
        assert task.is_overdue() is True

    def test_is_overdue_with_future_due_date(self):
        """Test is_overdue returns False for future due dates."""
        future_date = datetime.now() + timedelta(days=1)
        task = Task(1, "Test task", due_date=future_date)
        assert task.is_overdue() is False

    def test_is_overdue_with_no_due_date(self):
        """Test is_overdue returns False when no due date is set."""
        task = Task(1, "Test task")
        assert task.is_overdue() is False

    def test_is_upcoming_with_due_date_within_24_hours(self):
        """Test is_upcoming returns True for due dates within 24 hours."""
        # Create a due date for tomorrow but within 24 hours
        tomorrow = datetime.now() + timedelta(hours=12)
        task = Task(1, "Test task", due_date=tomorrow)
        assert task.is_upcoming() is True

    def test_is_upcoming_with_due_date_beyond_24_hours(self):
        """Test is_upcoming returns False for due dates beyond 24 hours."""
        future_date = datetime.now() + timedelta(days=2)
        task = Task(1, "Test task", due_date=future_date)
        assert task.is_upcoming() is False

    def test_is_upcoming_with_no_due_date(self):
        """Test is_upcoming returns False when no due date is set."""
        task = Task(1, "Test task")
        assert task.is_upcoming() is False

    def test_is_valid_recurrence_valid_values(self):
        """Test is_valid_recurrence returns True for valid recurrence values."""
        task = Task(1, "Test task")
        assert task.is_valid_recurrence(Recurrence.DAILY) is True
        assert task.is_valid_recurrence(Recurrence.WEEKLY) is True
        assert task.is_valid_recurrence(Recurrence.MONTHLY) is True
        assert task.is_valid_recurrence(None) is True

    def test_is_valid_recurrence_invalid_values(self):
        """Test is_valid_recurrence returns False for invalid recurrence values."""
        task = Task(1, "Test task")
        assert task.is_valid_recurrence("yearly") is False
        assert task.is_valid_recurrence("invalid") is False

    def test_validate_recurrence_valid(self):
        """Test validate_recurrence doesn't raise for valid values."""
        task = Task(1, "Test task")
        # Should not raise an exception
        task.validate_recurrence(Recurrence.DAILY)
        task.validate_recurrence(None)

    def test_validate_recurrence_invalid(self):
        """Test validate_recurrence raises ValueError for invalid values."""
        task = Task(1, "Test task")
        with pytest.raises(ValueError):
            task.validate_recurrence("invalid")

    def test_validate_due_date_valid(self):
        """Test validate_due_date doesn't raise for valid values."""
        task = Task(1, "Test task")
        future_date = datetime.now() + timedelta(days=1)
        # Should not raise an exception
        task.validate_due_date(future_date)
        task.validate_due_date(None)

    def test_validate_due_date_invalid(self):
        """Test validate_due_date raises ValueError for invalid values."""
        task = Task(1, "Test task")
        with pytest.raises(ValueError):
            task.validate_due_date("not a datetime object")

    def test_task_repr_includes_recurrence(self):
        """Test that repr includes recurrence information."""
        task = Task(1, "Test task", recurrence=Recurrence.DAILY)
        repr_str = repr(task)
        assert "recurrence=" in repr_str
        assert "daily" in repr_str  # Recurrence values are stored in lowercase

    def test_task_initialization_with_all_attributes(self):
        """Test creating a task with all attributes including recurrence."""
        future_date = datetime.now() + timedelta(days=1)
        task = Task(
            task_id=1,
            description="Test task",
            completed=False,
            priority=Priority.HIGH,
            tags=["test", "important"],
            due_date=future_date,
            recurrence=Recurrence.WEEKLY
        )

        assert task.id == 1
        assert task.description == "Test task"
        assert task.completed is False
        assert task.priority == Priority.HIGH
        assert task.tags == ["test", "important"]
        assert task.due_date == future_date
        assert task.recurrence == Recurrence.WEEKLY