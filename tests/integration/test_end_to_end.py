"""
End-to-end integration tests for CLI functionality.
"""
import pytest
import sys
from io import StringIO
from contextlib import redirect_stdout
from src.todo_app.cli.interface import CLIInterface
from src.todo_app.core.task_manager import TaskManager


class TestEndToEnd:
    """End-to-end integration tests for CLI functionality."""

    def setup_method(self):
        """Set up a fresh TaskManager and CLIInterface for each test."""
        self.task_manager = TaskManager()
        self.cli = CLIInterface(self.task_manager)

    def test_cli_add_task_with_priority_tags_due_date(self):
        """Test adding a task with priority, tags, and due_date via CLI."""
        # Capture stdout to check output
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            self.cli.parse_and_execute(["add", "Test task", "--priority", "high", "--tags", "work,urgent", "--due-date", "2023-12-25"])

        output = captured_output.getvalue()
        assert "Added task" in output
        assert "Test task" in output

        # Verify task was added with correct attributes
        tasks = self.task_manager.get_all_tasks()
        assert len(tasks) == 1
        task = tasks[0]
        assert task.description == "Test task"
        assert task.priority == "high"
        assert "work" in task.tags
        assert "urgent" in task.tags

    def test_cli_search_functionality(self):
        """Test search functionality via CLI."""
        # Add some tasks
        self.cli.parse_and_execute(["add", "Buy groceries"])
        self.cli.parse_and_execute(["add", "Complete project"])
        self.cli.parse_and_execute(["add", "Buy milk"])

        # Capture search output
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            self.cli.parse_and_execute(["search", "buy"])

        output = captured_output.getvalue()
        # Should contain both "Buy groceries" and "Buy milk" (case insensitive search)
        assert "Buy groceries" in output
        assert "Buy milk" in output
        # Count occurrences of the search term in the original case in the output
        assert output.lower().count("buy") >= 2

    def test_cli_filter_functionality(self):
        """Test filter functionality via CLI."""
        # Add tasks with different priorities
        self.cli.parse_and_execute(["add", "High priority task", "--priority", "high"])
        self.cli.parse_and_execute(["add", "Medium priority task", "--priority", "medium"])
        self.cli.parse_and_execute(["add", "Low priority task", "--priority", "low"])

        # Mark one as complete
        self.cli.parse_and_execute(["complete", "1"])

        # Filter by high priority
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            self.cli.parse_and_execute(["filter", "--priority", "high"])

        output = captured_output.getvalue()
        assert "High priority task" in output
        assert "high" in output.lower()

    def test_cli_sort_functionality(self):
        """Test sort functionality via CLI."""
        # Add tasks with different priorities
        self.cli.parse_and_execute(["add", "Medium priority", "--priority", "medium"])
        self.cli.parse_and_execute(["add", "High priority", "--priority", "high"])
        self.cli.parse_and_execute(["add", "Low priority", "--priority", "low"])

        # Sort by priority
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            self.cli.parse_and_execute(["sort", "--by", "priority"])

        output = captured_output.getvalue()
        # High priority should appear first (high priority comes first in sorting)
        assert "HIGH" in output
        assert "High priority" in output
        # Check that output contains sorted tasks
        lines = output.split('\n')
        # Find the task lines (skip header)
        task_lines = [line for line in lines if line.strip() and not line.startswith('ID |') and not line.startswith('---')]
        # The first task line should contain high priority
        if task_lines:
            first_task_line = task_lines[0]
            assert "HIGH" in first_task_line or "High priority" in first_task_line

    def test_cli_view_with_priority_tags(self):
        """Test viewing tasks with priority and tags."""
        # Add a task with priority and tags
        self.cli.parse_and_execute(["add", "Test task", "--priority", "high", "--tags", "work,important"])

        # View tasks
        captured_output = StringIO()

        with redirect_stdout(captured_output):
            self.cli.parse_and_execute(["view"])

        output = captured_output.getvalue()
        assert "HIGH" in output
        assert "work,important" in output
        assert "Test task" in output

    def test_cli_workflow_complete(self):
        """Test a complete workflow of adding, viewing, searching, filtering, and sorting tasks."""
        # Add multiple tasks with different attributes
        self.cli.parse_and_execute(["add", "Urgent work task", "--priority", "high", "--tags", "work,urgent"])
        self.cli.parse_and_execute(["add", "Low priority personal", "--priority", "low", "--tags", "personal"])
        self.cli.parse_and_execute(["add", "Medium priority project", "--priority", "medium", "--tags", "work"])

        # Complete one task
        self.cli.parse_and_execute(["complete", "1"])

        # Search for "work" - should find tasks with "work" in description or tags
        captured_output = StringIO()
        with redirect_stdout(captured_output):
            self.cli.parse_and_execute(["search", "work"])
        search_output = captured_output.getvalue()
        assert "Urgent work task" in search_output  # "work" in description
        assert "Medium priority project" in search_output  # "work" in tags

        # Filter by priority high
        captured_output = StringIO()
        with redirect_stdout(captured_output):
            self.cli.parse_and_execute(["filter", "--priority", "high"])
        filter_output = captured_output.getvalue()
        assert "Urgent work task" in filter_output
        assert "high" in filter_output.lower()

        # Sort by priority
        captured_output = StringIO()
        with redirect_stdout(captured_output):
            self.cli.parse_and_execute(["sort", "--by", "priority"])
        sort_output = captured_output.getvalue()
        # Should show tasks sorted by priority (high first)
        assert "HIGH" in sort_output
        assert "MEDI" in sort_output
        assert "LOW" in sort_output