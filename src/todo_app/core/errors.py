"""
Custom Error Classes

Defines custom exception classes for the todo application.
"""


class TaskError(Exception):
    """
    Base exception class for task-related errors.
    """
    pass


class TaskNotFoundError(TaskError):
    """
    Raised when a task with a specified ID is not found.
    """
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} does not exist")


class InvalidTaskDescriptionError(TaskError):
    """
    Raised when a task description is invalid (empty or whitespace-only).
    """
    def __init__(self):
        super().__init__("Task description cannot be empty or contain only whitespace")


class TaskOperationError(TaskError):
    """
    Raised when a task operation fails.
    """
    pass