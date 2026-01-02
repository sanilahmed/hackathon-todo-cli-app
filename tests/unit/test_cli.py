"""
Unit tests for CLI functionality, specifically testing viewing tasks with priority and tags.
"""
import pytest
from io import StringIO
from contextlib import redirect_stdout
from src.todo_app.cli.interface import CLIInterface
from src.todo_app.core.task_manager import TaskManager


class TestCLI:
    """Tests for the CLI interface functionality."""

    def setup_method(self):
        """Set up a fresh TaskManager and CLIInterface for each test."""
        self.task_manager = TaskManager()
        self.cli = CLIInterface(self.task_manager)

    def test_view_tasks_with_priority_and_tags(self):
        """Test viewing tasks with priority and tags displays correctly."""
        # Add a task with priority and tags
        self.task_manager.add_task("Test task", priority="high", tags=["work", "urgent"], due_date=None)

        # Capture the output when viewing tasks
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            self.cli._handle_view()

        output = captured_output.getvalue()

        # Check that the output contains the task with priority and tags
        assert "Test task" in output
        assert "HIGH" in output  # Priority should be displayed
        assert "work,urgent" in output  # Tags should be displayed

    def test_view_tasks_with_all_attributes(self):
        """Test viewing tasks with all attributes (priority, tags, due_date)."""
        from datetime import datetime

        # Add a task with all attributes
        due_date = datetime(2023, 12, 25)
        self.task_manager.add_task("Complete project",
                                 priority="high",
                                 tags=["work", "important"],
                                 due_date=due_date)

        # Capture the output when viewing tasks
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            self.cli._handle_view()

        output = captured_output.getvalue()

        # Check that the output contains all attributes
        assert "Complete project" in output
        assert "HIGH" in output  # Priority
        assert "work,important" in output  # Tags
        assert "2023-12-25" in output  # Due date

    def test_view_tasks_mixed_attributes(self):
        """Test viewing a mix of tasks with and without attributes."""
        from datetime import datetime

        # Add tasks with different combinations of attributes
        due_date = datetime(2023, 12, 25)
        self.task_manager.add_task("Simple task")  # No priority, tags, or due_date
        self.task_manager.add_task("High priority task", priority="high")  # Only priority
        self.task_manager.add_task("Task with tags", tags=["personal"])  # Only tags
        self.task_manager.add_task("Complete task", priority="low", tags=["work"], due_date=due_date)  # All

        # Capture the output when viewing tasks
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            self.cli._handle_view()

        output = captured_output.getvalue()

        # Check that all tasks are displayed with appropriate values
        assert "Simple task" in output
        assert "High priority task" in output
        assert "Task with tags" in output
        assert "Complete task" in output

        # Check that default values are displayed appropriately
        assert "MEDI" in output  # Default priority for simple task
        assert "HIGH" in output  # High priority task
        assert "LOW" in output   # Low priority task
        assert "personal" in output  # Tags for one task
        assert "work" in output      # Tags for another task
        assert "2023-12-25" in output  # Due date for one task