"""
Output Formatter

Handles formatting of task data for console display.
"""

from ..core.task import Task


class TaskFormatter:
    """
    Formats task data for console display in a readable format.
    """

    def format_tasks(self, tasks):
        """
        Format a list of tasks for console display.

        Args:
            tasks: List of Task objects to format

        Returns:
            str: Formatted string representation of the tasks
        """
        if not tasks:
            return "No tasks in the list"

        # Create table header
        header = "ID | Status    | Priority | Tags       | Due Date   | Recurrence | Description"
        separator = "---|-----------|----------|------------|------------|------------|-------------"

        # Format each task
        task_lines = []
        for task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            priority = task.priority.upper()[:4]  # Take first 4 chars: HIGH, MEDI, LOW
            tags_str = ",".join(task.tags) if task.tags else ""
            due_date_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else ""
            recurrence_str = task.recurrence.upper() if task.recurrence else ""

            # Add overdue or upcoming indicators to description
            description = task.description
            if task.is_overdue():
                description = f"[OVERDUE] {description}"
            elif task.is_upcoming():
                description = f"[DUE SOON] {description}"

            task_line = f"{task.id:<2} | {status:<9} | {priority:<8} | {tags_str:<10} | {due_date_str:<10} | {recurrence_str:<10} | {description}"
            task_lines.append(task_line)

        # Combine all parts
        result = [header, separator] + task_lines
        return "\n".join(result)

    def format_single_task(self, task):
        """
        Format a single task for console display.

        Args:
            task: A Task object to format

        Returns:
            str: Formatted string representation of the task
        """
        status = "Complete" if task.completed else "Incomplete"

        # Add overdue or upcoming indicators to description
        description = task.description
        if task.is_overdue():
            description = f"[OVERDUE] {description}"
        elif task.is_upcoming():
            description = f"[DUE SOON] {description}"

        return f"{task.id} | {status} | {description}"