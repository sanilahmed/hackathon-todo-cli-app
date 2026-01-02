"""
Unit tests for TaskManager functionality.
"""
import pytest
from datetime import timedelta
from src.todo_app.core.task_manager import TaskManager
from src.todo_app.core.task import Task
from src.todo_app.core.errors import InvalidTaskDescriptionError, TaskNotFoundError


class TestTaskManager:
    """Tests for the TaskManager class."""

    def setup_method(self):
        """Set up a fresh TaskManager for each test."""
        self.task_manager = TaskManager()

    def test_add_task_success(self):
        """Test adding a task successfully."""
        task = self.task_manager.add_task("Test task")
        assert task.id == 1
        assert task.description == "Test task"
        assert task.completed is False

        # Verify the task is in the manager
        tasks = self.task_manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 1

    def test_add_task_with_empty_description(self):
        """Test adding a task with empty description raises error."""
        with pytest.raises(InvalidTaskDescriptionError):
            self.task_manager.add_task("")

        with pytest.raises(InvalidTaskDescriptionError):
            self.task_manager.add_task("   ")

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        # Initially empty
        tasks = self.task_manager.get_all_tasks()
        assert len(tasks) == 0

        # Add tasks
        self.task_manager.add_task("Task 1")
        self.task_manager.add_task("Task 2")

        tasks = self.task_manager.get_all_tasks()
        assert len(tasks) == 2

    def test_get_task_by_id(self):
        """Test getting a task by ID."""
        task = self.task_manager.add_task("Test task")
        found_task = self.task_manager.get_task_by_id(task.id)

        assert found_task is not None
        assert found_task.id == task.id
        assert found_task.description == task.description
        assert found_task.completed == task.completed

        # Test non-existent task
        not_found = self.task_manager.get_task_by_id(999)
        assert not_found is None

    def test_update_task_success(self):
        """Test updating a task description."""
        task = self.task_manager.add_task("Original task")
        initial_id = task.id

        success = self.task_manager.update_task(initial_id, "Updated task")
        assert success is True

        updated_task = self.task_manager.get_task_by_id(initial_id)
        assert updated_task.description == "Updated task"

    def test_update_task_not_found(self):
        """Test updating a non-existent task returns False."""
        success = self.task_manager.update_task(999, "New description")
        assert success is False

    def test_update_task_with_empty_description(self):
        """Test updating a task with empty description raises error."""
        task = self.task_manager.add_task("Test task")

        with pytest.raises(InvalidTaskDescriptionError):
            self.task_manager.update_task(task.id, "")

        with pytest.raises(InvalidTaskDescriptionError):
            self.task_manager.update_task(task.id, "   ")

    def test_delete_task_success(self):
        """Test deleting a task."""
        task = self.task_manager.add_task("Test task")
        initial_id = task.id

        success = self.task_manager.delete_task(initial_id)
        assert success is True

        tasks = self.task_manager.get_all_tasks()
        assert len(tasks) == 0

        # Verify task is truly gone
        deleted_task = self.task_manager.get_task_by_id(initial_id)
        assert deleted_task is None

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task returns False."""
        success = self.task_manager.delete_task(999)
        assert success is False

    def test_mark_complete_success(self):
        """Test marking a task as complete."""
        task = self.task_manager.add_task("Test task")
        initial_id = task.id

        success = self.task_manager.mark_complete(initial_id)
        assert success is True

        completed_task = self.task_manager.get_task_by_id(initial_id)
        assert completed_task.completed is True

    def test_mark_complete_not_found(self):
        """Test marking a non-existent task as complete returns False."""
        success = self.task_manager.mark_complete(999)
        assert success is False

    def test_mark_incomplete_success(self):
        """Test marking a task as incomplete."""
        task = self.task_manager.add_task("Test task")
        initial_id = task.id

        # First mark as complete
        self.task_manager.mark_complete(initial_id)
        completed_task = self.task_manager.get_task_by_id(initial_id)
        assert completed_task.completed is True

        # Then mark as incomplete
        success = self.task_manager.mark_incomplete(initial_id)
        assert success is True

        incomplete_task = self.task_manager.get_task_by_id(initial_id)
        assert incomplete_task.completed is False

    def test_mark_incomplete_not_found(self):
        """Test marking a non-existent task as incomplete returns False."""
        success = self.task_manager.mark_incomplete(999)
        assert success is False

    def test_id_generation(self):
        """Test sequential ID generation."""
        task1 = self.task_manager.add_task("Task 1")
        task2 = self.task_manager.add_task("Task 2")
        task3 = self.task_manager.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_delete_task_preserves_other_ids(self):
        """Test deleting a task doesn't affect other task IDs."""
        task1 = self.task_manager.add_task("Task 1")
        task2 = self.task_manager.add_task("Task 2")
        task3 = self.task_manager.add_task("Task 3")

        # Delete middle task
        self.task_manager.delete_task(task2.id)

        # Other tasks should still exist with same IDs
        remaining_tasks = self.task_manager.get_all_tasks()
        assert len(remaining_tasks) == 2

        found_task1 = self.task_manager.get_task_by_id(task1.id)
        found_task3 = self.task_manager.get_task_by_id(task3.id)

        assert found_task1 is not None
        assert found_task3 is not None
        assert found_task1.id == 1
        assert found_task3.id == 3

    def test_search_tasks_success(self):
        """Test searching for tasks by keyword."""
        self.task_manager.add_task("Buy groceries")
        self.task_manager.add_task("Complete project")
        self.task_manager.add_task("Buy milk")
        self.task_manager.add_task("Call doctor")

        # Search for "buy"
        results = self.task_manager.search_tasks("buy")
        assert len(results) == 2
        descriptions = [task.description for task in results]
        assert "Buy groceries" in descriptions
        assert "Buy milk" in descriptions

        # Search for "project"
        results = self.task_manager.search_tasks("project")
        assert len(results) == 1
        assert results[0].description == "Complete project"

    def test_search_tasks_case_insensitive(self):
        """Test case-insensitive search functionality."""
        self.task_manager.add_task("Buy Groceries")
        self.task_manager.add_task("Complete PROJECT")
        self.task_manager.add_task("call doctor")

        # Search with different cases
        results = self.task_manager.search_tasks("GROCERIES")
        assert len(results) == 1
        assert results[0].description == "Buy Groceries"

        results = self.task_manager.search_tasks("project")
        assert len(results) == 1
        assert results[0].description == "Complete PROJECT"

        results = self.task_manager.search_tasks("CALL")
        assert len(results) == 1
        assert results[0].description == "call doctor"

    def test_search_tasks_no_matches(self):
        """Test searching for non-existent keyword."""
        self.task_manager.add_task("Buy groceries")
        self.task_manager.add_task("Complete project")

        results = self.task_manager.search_tasks("xyz")
        assert len(results) == 0

    def test_search_tasks_empty_keyword(self):
        """Test searching with empty keyword."""
        self.task_manager.add_task("Buy groceries")

        results = self.task_manager.search_tasks("")
        assert len(results) == 0

    def test_filter_tasks_by_status(self):
        """Test filtering tasks by completion status."""
        task1 = self.task_manager.add_task("Task 1")
        task2 = self.task_manager.add_task("Task 2")
        task3 = self.task_manager.add_task("Task 3")

        # Mark one task as complete
        self.task_manager.mark_complete(task1.id)

        # Filter by complete status
        results = self.task_manager.filter_tasks(status="complete")
        assert len(results) == 1
        assert results[0].id == task1.id
        assert results[0].completed is True

        # Filter by incomplete status
        results = self.task_manager.filter_tasks(status="incomplete")
        assert len(results) == 2
        for task in results:
            assert task.completed is False

    def test_filter_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        from src.todo_app.core.task import Priority

        task1 = self.task_manager.add_task("Task 1", priority=Priority.HIGH)
        task2 = self.task_manager.add_task("Task 2", priority=Priority.MEDIUM)
        task3 = self.task_manager.add_task("Task 3", priority=Priority.LOW)
        task4 = self.task_manager.add_task("Task 4", priority=Priority.HIGH)

        # Filter by high priority
        results = self.task_manager.filter_tasks(priority=Priority.HIGH)
        assert len(results) == 2
        for task in results:
            assert task.priority == Priority.HIGH

        # Filter by medium priority
        results = self.task_manager.filter_tasks(priority=Priority.MEDIUM)
        assert len(results) == 1
        assert results[0].priority == Priority.MEDIUM

    def test_filter_tasks_by_date(self):
        """Test filtering tasks by due date."""
        from datetime import datetime

        due_date = datetime(2023, 12, 25)
        task1 = self.task_manager.add_task("Task 1", due_date=due_date)
        task2 = self.task_manager.add_task("Task 2", due_date=datetime(2023, 12, 26))
        task3 = self.task_manager.add_task("Task 3")  # No due date

        results = self.task_manager.filter_tasks(due_date=due_date)
        assert len(results) == 1
        assert results[0].id == task1.id
        assert results[0].due_date == due_date

    def test_filter_tasks_multiple_criteria(self):
        """Test filtering tasks by multiple criteria."""
        from datetime import datetime
        from src.todo_app.core.task import Priority

        due_date = datetime(2023, 12, 25)
        task1 = self.task_manager.add_task("Task 1", priority=Priority.HIGH, due_date=due_date)
        task2 = self.task_manager.add_task("Task 2", priority=Priority.HIGH)  # Different date
        task3 = self.task_manager.add_task("Task 3", due_date=due_date)  # Different priority

        # Mark one task as complete
        self.task_manager.mark_complete(task1.id)

        # Filter by high priority AND complete status
        results = self.task_manager.filter_tasks(priority=Priority.HIGH, status="complete")
        assert len(results) == 1
        assert results[0].id == task1.id
        assert results[0].priority == Priority.HIGH
        assert results[0].completed is True

    def test_sort_tasks_by_priority(self):
        """Test sorting tasks by priority."""
        from src.todo_app.core.task import Priority

        # Add tasks with different priorities
        task1 = self.task_manager.add_task("Task 1", priority=Priority.MEDIUM)
        task2 = self.task_manager.add_task("Task 2", priority=Priority.HIGH)
        task3 = self.task_manager.add_task("Task 3", priority=Priority.LOW)
        task4 = self.task_manager.add_task("Task 4", priority=Priority.HIGH)

        # Sort by priority (high first by default)
        results = self.task_manager.sort_tasks(by="priority")
        expected_order = [Priority.HIGH, Priority.HIGH, Priority.MEDIUM, Priority.LOW]
        actual_order = [task.priority for task in results]
        assert actual_order == expected_order

        # Sort by priority in reverse (low first)
        results = self.task_manager.sort_tasks(by="priority", reverse=True)
        expected_order = [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.HIGH]
        actual_order = [task.priority for task in results]
        assert actual_order == expected_order

    def test_sort_tasks_by_due_date(self):
        """Test sorting tasks by due date."""
        from datetime import datetime

        date1 = datetime(2023, 12, 25)
        date2 = datetime(2023, 12, 24)
        date3 = datetime(2023, 12, 26)

        task1 = self.task_manager.add_task("Task 1", due_date=date1)
        task2 = self.task_manager.add_task("Task 2", due_date=date2)
        task3 = self.task_manager.add_task("Task 3", due_date=date3)
        task4 = self.task_manager.add_task("Task 4")  # No due date

        # Sort by due date (None values come first by default)
        results = self.task_manager.sort_tasks(by="due_date")
        # None should come first, then earliest date
        assert results[0].due_date is None  # task4 (no due date)
        assert results[1].due_date == date2  # 2023-12-24 (earliest)
        assert results[2].due_date == date1  # 2023-12-25
        assert results[3].due_date == date3  # 2023-12-26 (latest)

        # Sort by due date in reverse
        results = self.task_manager.sort_tasks(by="due_date", reverse=True)
        # Latest date should come first, then None
        assert results[0].due_date == date3  # 2023-12-26 (latest)
        assert results[1].due_date == date1  # 2023-12-25
        assert results[2].due_date == date2  # 2023-12-24 (earliest)
        assert results[3].due_date is None  # task4 (no due date)

    def test_sort_tasks_by_title(self):
        """Test sorting tasks by title."""
        task1 = self.task_manager.add_task("Zebra")
        task2 = self.task_manager.add_task("Apple")
        task3 = self.task_manager.add_task("Mango")

        # Sort by title (alphabetical)
        results = self.task_manager.sort_tasks(by="title")
        expected_order = ["Apple", "Mango", "Zebra"]
        actual_order = [task.description for task in results]
        assert actual_order == expected_order

        # Sort by title in reverse
        results = self.task_manager.sort_tasks(by="title", reverse=True)
        expected_order = ["Zebra", "Mango", "Apple"]
        actual_order = [task.description for task in results]
        assert actual_order == expected_order

    def test_sort_tasks_invalid_criteria(self):
        """Test sorting with invalid criteria raises ValueError."""
        with pytest.raises(ValueError):
            self.task_manager.sort_tasks(by="invalid")

    def test_add_task_with_recurrence(self):
        """Test adding a task with recurrence."""
        from datetime import datetime
        from src.todo_app.core.task import Recurrence

        due_date = datetime(2023, 12, 25)
        task = self.task_manager.add_task("Recurring task", recurrence=Recurrence.DAILY, due_date=due_date)

        assert task.recurrence == Recurrence.DAILY
        assert task.due_date == due_date
        assert task.description == "Recurring task"

    def test_add_task_with_invalid_recurrence(self):
        """Test adding a task with invalid recurrence raises ValueError."""
        from src.todo_app.core.task import Recurrence

        with pytest.raises(ValueError):
            self.task_manager.add_task("Task", recurrence="yearly")

    def test_get_overdue_tasks(self):
        """Test getting overdue tasks."""
        from datetime import datetime, timedelta
        from src.todo_app.core.task import Recurrence

        # Add a task with a past due date
        past_due_date = datetime.now() - timedelta(days=1)
        task1 = self.task_manager.add_task("Overdue task", due_date=past_due_date)

        # Add a task with a future due date
        future_due_date = datetime.now() + timedelta(days=1)
        task2 = self.task_manager.add_task("Future task", due_date=future_due_date)

        # Add a task without due date
        task3 = self.task_manager.add_task("No due date task")

        # Add a recurring overdue task
        task4 = self.task_manager.add_task("Recurring overdue task", due_date=past_due_date, recurrence=Recurrence.DAILY)

        overdue_tasks = self.task_manager.get_overdue_tasks()
        assert len(overdue_tasks) == 2  # task1 and task4 are overdue

        overdue_descriptions = [task.description for task in overdue_tasks]
        assert "Overdue task" in overdue_descriptions
        assert "Recurring overdue task" in overdue_descriptions

    def test_get_upcoming_tasks(self):
        """Test getting upcoming tasks."""
        from datetime import datetime, timedelta
        from src.todo_app.core.task import Recurrence

        # Add a task due in 12 hours (should be upcoming)
        upcoming_due_date = datetime.now() + timedelta(hours=12)
        task1 = self.task_manager.add_task("Upcoming task", due_date=upcoming_due_date)

        # Add a task due in 2 days (should not be upcoming)
        future_due_date = datetime.now() + timedelta(days=2)
        task2 = self.task_manager.add_task("Future task", due_date=future_due_date)

        # Add a task due yesterday (should not be upcoming)
        past_due_date = datetime.now() - timedelta(days=1)
        task3 = self.task_manager.add_task("Past task", due_date=past_due_date)

        # Add a task without due date
        task4 = self.task_manager.add_task("No due date task")

        upcoming_tasks = self.task_manager.get_upcoming_tasks()
        assert len(upcoming_tasks) == 1  # Only task1 is upcoming
        assert upcoming_tasks[0].description == "Upcoming task"

    def test_reschedule_recurring_task_daily(self):
        """Test rescheduling a daily recurring task."""
        from datetime import datetime, timedelta
        from src.todo_app.core.task import Recurrence

        due_date = datetime.now()
        task = self.task_manager.add_task("Daily recurring task", recurrence=Recurrence.DAILY, due_date=due_date)

        new_task = self.task_manager.reschedule_recurring_task(task)

        assert new_task is not None
        assert new_task.description == "Daily recurring task"
        assert new_task.recurrence == Recurrence.DAILY
        assert new_task.due_date == due_date + timedelta(days=1)
        assert new_task.completed is False

    def test_reschedule_recurring_task_weekly(self):
        """Test rescheduling a weekly recurring task."""
        from datetime import datetime, timedelta
        from src.todo_app.core.task import Recurrence

        due_date = datetime.now()
        task = self.task_manager.add_task("Weekly recurring task", recurrence=Recurrence.WEEKLY, due_date=due_date)

        new_task = self.task_manager.reschedule_recurring_task(task)

        assert new_task is not None
        assert new_task.description == "Weekly recurring task"
        assert new_task.recurrence == Recurrence.WEEKLY
        assert new_task.due_date == due_date + timedelta(weeks=1)

    def test_reschedule_recurring_task_monthly(self):
        """Test rescheduling a monthly recurring task."""
        from datetime import datetime
        from src.todo_app.core.task import Recurrence

        due_date = datetime(2023, 1, 15)  # January 15
        task = self.task_manager.add_task("Monthly recurring task", recurrence=Recurrence.MONTHLY, due_date=due_date)

        new_task = self.task_manager.reschedule_recurring_task(task)

        assert new_task is not None
        assert new_task.description == "Monthly recurring task"
        assert new_task.recurrence == Recurrence.MONTHLY
        # The new due date should be February 15
        assert new_task.due_date.month == 2
        assert new_task.due_date.day == 15

    def test_reschedule_non_recurring_task(self):
        """Test rescheduling a non-recurring task returns None."""
        from datetime import datetime

        due_date = datetime.now()
        task = self.task_manager.add_task("Non-recurring task", due_date=due_date)

        new_task = self.task_manager.reschedule_recurring_task(task)

        assert new_task is None

    def test_mark_complete_creates_next_occurrence_for_recurring_task(self):
        """Test that marking a recurring task as complete creates the next occurrence."""
        from datetime import datetime
        from src.todo_app.core.task import Recurrence

        initial_task_count = len(self.task_manager.get_all_tasks())
        assert initial_task_count == 0  # Fresh manager

        due_date = datetime.now()
        recurring_task = self.task_manager.add_task("Daily recurring task", recurrence=Recurrence.DAILY, due_date=due_date)

        # After adding task, count should be 1
        assert len(self.task_manager.get_all_tasks()) == 1

        # Mark the recurring task as complete
        success = self.task_manager.mark_complete(recurring_task.id)
        assert success is True

        # Check that the original task is marked complete
        completed_task = self.task_manager.get_task_by_id(recurring_task.id)
        assert completed_task.completed is True

        # Check that a new task has been created for the next occurrence
        all_tasks = self.task_manager.get_all_tasks()
        assert len(all_tasks) == 2  # Original (completed) + new occurrence

        # Find the new task (should not be the same ID as the completed one)
        new_task = None
        for task in all_tasks:
            if task.id != recurring_task.id and task.description == "Daily recurring task":
                new_task = task
                break

        assert new_task is not None
        assert new_task.completed is False
        assert new_task.recurrence == Recurrence.DAILY
        assert new_task.due_date == due_date + timedelta(days=1)

    def test_mark_complete_non_recurring_task(self):
        """Test that marking a non-recurring task as complete doesn't create new tasks."""
        from datetime import datetime

        initial_task_count = len(self.task_manager.get_all_tasks())
        assert initial_task_count == 0  # Fresh manager

        due_date = datetime.now()
        task = self.task_manager.add_task("Non-recurring task", due_date=due_date)

        # After adding task, count should be 1
        assert len(self.task_manager.get_all_tasks()) == 1

        # Mark the non-recurring task as complete
        success = self.task_manager.mark_complete(task.id)
        assert success is True

        # Check that the task is marked complete
        completed_task = self.task_manager.get_task_by_id(task.id)
        assert completed_task.completed is True

        # Check that no new task was created (count should still be 1)
        all_tasks = self.task_manager.get_all_tasks()
        assert len(all_tasks) == 1  # Same count as after adding (no new task created)

    def test_backward_compatibility_with_existing_tasks(self):
        """Test that existing tasks without priority/tags/due_date work with new functionality."""
        # Add a task using the old interface (without priority/tags/due_date)
        old_task = self.task_manager.add_task("Old task")

        # All new functionality should work with this task
        # Search should find it
        results = self.task_manager.search_tasks("old")
        assert len(results) == 1
        assert results[0].id == old_task.id

        # Filter by default priority should work
        from src.todo_app.core.task import Priority
        results = self.task_manager.filter_tasks(priority=Priority.MEDIUM)
        assert len(results) == 1
        assert results[0].id == old_task.id

        # Sort should work
        results = self.task_manager.sort_tasks(by="priority")
        assert len(results) == 1
        assert results[0].id == old_task.id