"""
Task Manager

Manages in-memory storage and operations for Task objects.
"""

from datetime import datetime
from typing import List, Optional
from .task import Task
from .errors import InvalidTaskDescriptionError, TaskNotFoundError


class TaskManager:
    """
    Singleton class managing in-memory task storage.

    Methods include:
    - add_task()
    - get_all_tasks()
    - get_task_by_id()
    - update_task()
    - delete_task()
    - mark_complete()
    - mark_incomplete()
    """

    def __init__(self):
        """
        Initialize the TaskManager with an empty task list and next ID counter.
        """
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, description: str, priority: str = None, tags: List[str] = None,
                 due_date: Optional[datetime] = None, recurrence: Optional[str] = None) -> Task:
        """
        Add a new task with the given description and optional attributes.

        Args:
            description (str): Description of the new task
            priority (str): Priority level (high/medium/low), defaults to medium if not specified
            tags (List[str]): List of tags, defaults to empty list if not specified
            due_date (Optional[datetime]): Due date, defaults to None if not specified
            recurrence (Optional[str]): Recurrence pattern (daily/weekly/monthly), defaults to None if not specified

        Returns:
            Task: The newly created Task object

        Raises:
            InvalidTaskDescriptionError: If description is empty or contains only whitespace
        """
        if not description or not description.strip():
            raise InvalidTaskDescriptionError()

        # Set default priority if not provided
        from .task import Priority, Recurrence
        priority = priority if priority else Priority.MEDIUM

        # Validate recurrence if provided
        if recurrence is not None and recurrence not in Recurrence.VALUES:
            raise ValueError(f"Recurrence must be one of {Recurrence.VALUES}")

        task = Task(self._next_id, description, completed=False, priority=priority,
                   tags=tags, due_date=due_date, recurrence=recurrence)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the collection.

        Returns:
            List[Task]: List of all Task objects
        """
        return self._tasks.copy()

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in description, tags, and due_date (case-insensitive).

        Args:
            keyword (str): Search term to find in task descriptions, tags, and due_date

        Returns:
            List[Task]: List of tasks containing the keyword
        """
        if not keyword:
            return []

        keyword_lower = keyword.lower()
        matching_tasks = []

        for task in self._tasks:
            # Check description
            if keyword_lower in task.description.lower():
                matching_tasks.append(task)
                continue  # Don't check other fields if already matched

            # Check tags
            if task.tags:
                for tag in task.tags:
                    if keyword_lower in tag.lower():
                        matching_tasks.append(task)
                        break  # Don't add the same task twice

            # Check due_date if keyword looks like a date
            if task.due_date and keyword_lower in task.due_date.strftime("%Y-%m-%d").lower():
                if task not in matching_tasks:  # Don't add if already matched
                    matching_tasks.append(task)

        return matching_tasks

    def filter_tasks(self, **criteria) -> List[Task]:
        """
        Filter tasks by various criteria.

        Args:
            **criteria: Filter criteria (status, priority, due_date)

        Returns:
            List[Task]: List of tasks matching all criteria

        Supported criteria:
            status: "complete", "incomplete", "completed", "pending"
            priority: "high", "medium", "low"
            due_date: datetime object to match
        """
        filtered_tasks = self._tasks.copy()

        # Filter by status
        if 'status' in criteria:
            status = criteria['status']
            if status in ['complete', 'completed']:
                filtered_tasks = [task for task in filtered_tasks if task.completed]
            elif status in ['incomplete', 'pending']:
                filtered_tasks = [task for task in filtered_tasks if not task.completed]

        # Filter by priority
        if 'priority' in criteria:
            priority = criteria['priority']
            from .task import Priority
            if priority in Priority.VALUES:
                filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        # Filter by due date
        if 'due_date' in criteria:
            due_date = criteria['due_date']
            if due_date:
                # Compare just the date part (not time)
                filtered_tasks = [task for task in filtered_tasks
                                if task.due_date and task.due_date.date() == due_date.date()]

        return filtered_tasks

    def sort_tasks(self, by: str, reverse: bool = False) -> List[Task]:
        """
        Sort tasks by specified criteria.

        Args:
            by (str): Sort criteria ("priority", "due_date", "title")
            reverse (bool): Whether to reverse the sort order (optional, defaults to False)

        Returns:
            List[Task]: Sorted list of tasks (does not modify original order)

        Raises:
            ValueError: If 'by' is not a valid sort criteria
        """
        from .task import Priority

        # Define priority order for sorting (high first)
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}

        if by == "priority":
            return sorted(self._tasks,
                         key=lambda task: priority_order[task.priority],
                         reverse=reverse)
        elif by == "due_date":
            # Sort by due date, with None values coming first
            # Using not (task.due_date is None) so that None values (True) come first
            return sorted(self._tasks,
                         key=lambda task: (task.due_date is not None, task.due_date),
                         reverse=reverse)
        elif by == "title":
            return sorted(self._tasks,
                         key=lambda task: task.description.lower(),
                         reverse=reverse)
        else:
            raise ValueError(f"Invalid sort criteria: {by}. Valid options: 'priority', 'due_date', 'title'")

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Task: The Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def get_task_by_id_or_raise(self, task_id: int) -> Task:
        """
        Get a task by its ID or raise an exception if not found.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            Task: The Task object if found

        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def update_task(self, task_id: int, new_description: str) -> bool:
        """
        Update the description of an existing task.

        Args:
            task_id (int): ID of the task to update
            new_description (str): New description for the task

        Returns:
            bool: True if task was updated, False if task not found

        Raises:
            InvalidTaskDescriptionError: If new description is empty or contains only whitespace
        """
        if not new_description or not new_description.strip():
            raise InvalidTaskDescriptionError()

        task = self.get_task_by_id(task_id)
        if task:
            task.update_description(new_description)
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete. If the task is recurring, create a new instance for the next occurrence.

        Args:
            task_id (int): ID of the task to mark as complete

        Returns:
            bool: True if task was marked complete, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()

            # If the task is recurring, create a new instance for the next occurrence
            if task.recurrence:
                self.reschedule_recurring_task(task)

            return True
        return False

    def mark_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): ID of the task to mark as incomplete

        Returns:
            bool: True if task was marked incomplete, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_incomplete()
            return True
        return False

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all tasks that are overdue (due date is in the past).

        Returns:
            List[Task]: List of overdue Task objects
        """
        return [task for task in self._tasks if task.is_overdue()]

    def get_upcoming_tasks(self) -> List[Task]:
        """
        Get all tasks that are due soon (within 24 hours).

        Returns:
            List[Task]: List of upcoming Task objects
        """
        return [task for task in self._tasks if task.is_upcoming()]

    def reschedule_recurring_task(self, task: Task) -> Optional[Task]:
        """
        Create a new task instance based on a recurring task's next occurrence.

        Args:
            task (Task): The recurring task to reschedule

        Returns:
            Optional[Task]: New task instance with next occurrence date, or None if not recurring
        """
        if task.recurrence is None:
            return None

        try:
            # Import the utility function for calculating next occurrence
            from .utils import calculate_next_occurrence

            next_due_date = calculate_next_occurrence(task.due_date or datetime.now(), task.recurrence)
            if next_due_date is None:
                return None

            # Create a new task with the same properties but updated due date
            new_task = Task(
                self._next_id,
                task.description,
                completed=False,  # New occurrence is not completed
                priority=task.priority,
                tags=task.tags.copy(),  # Copy the tags
                due_date=next_due_date,
                recurrence=task.recurrence  # Keep the same recurrence pattern
            )

            self._tasks.append(new_task)
            self._next_id += 1
            return new_task
        except Exception:
            # If there's an error in rescheduling, return None to indicate failure
            # This prevents breaking the completion flow if recurrence calculation fails
            return None

    def get_next_id(self) -> int:
        """
        Get the next available task ID without creating a task.

        Returns:
            int: The next available ID
        """
        return self._next_id

    def clear_all_tasks(self):
        """
        Clear all tasks from the manager.
        """
        self._tasks.clear()
        self._next_id = 1