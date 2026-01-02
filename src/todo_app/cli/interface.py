"""
CLI Interface

Handles command-line argument parsing and execution for the todo application.
"""

import argparse
import sys
from typing import Optional
from .formatter import TaskFormatter
from ..core.task_manager import TaskManager
from ..core.errors import InvalidTaskDescriptionError


class CLIInterface:
    """
    Command parser and executor for the todo application.

    Parses command-line arguments and routes to appropriate TaskManager methods.
    Handles user input validation and error messages.
    """

    def __init__(self, task_manager: TaskManager):
        """
        Initialize the CLI Interface with a TaskManager instance.

        Args:
            task_manager (TaskManager): The task manager to operate on
        """
        self.task_manager = task_manager
        self.formatter = TaskFormatter()

    def parse_and_execute(self, args: Optional[list] = None):
        """
        Parse command-line arguments and execute the corresponding action.

        Args:
            args (Optional[list]): Command-line arguments to parse (default: sys.argv[1:])
        """
        if args is None:
            args = sys.argv[1:]

        parser = argparse.ArgumentParser(
            prog="python -m src.todo_app",
            description="A command-line interface todo application"
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("description", nargs="+", help="Task description")
        add_parser.add_argument("--priority", help="Task priority (high/medium/low)")
        add_parser.add_argument("--tags", help="Comma-separated tags (e.g., work,urgent)")
        add_parser.add_argument("--due-date", help="Due date in YYYY-MM-DD format")
        add_parser.add_argument("--recurrence", help="Recurrence pattern (daily/weekly/monthly)")

        # View command
        view_parser = subparsers.add_parser("view", help="View all tasks")

        # Complete command
        complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
        complete_parser.add_argument("task_id", type=int, help="ID of the task to complete")

        # Incomplete command
        incomplete_parser = subparsers.add_parser("incomplete", help="Mark a task as incomplete")
        incomplete_parser.add_argument("task_id", type=int, help="ID of the task to mark as incomplete")

        # Update command
        update_parser = subparsers.add_parser("update", help="Update a task description")
        update_parser.add_argument("task_id", type=int, help="ID of the task to update")
        update_parser.add_argument("new_description", nargs="+", help="New task description")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")

        # Search command
        search_parser = subparsers.add_parser("search", help="Search tasks by keyword")
        search_parser.add_argument("keyword", help="Keyword to search for in task descriptions")

        # Filter command
        filter_parser = subparsers.add_parser("filter", help="Filter tasks by criteria")
        filter_parser.add_argument("--status", choices=["complete", "incomplete", "completed", "pending"],
                                  help="Filter by completion status")
        filter_parser.add_argument("--priority", choices=["high", "medium", "low"],
                                  help="Filter by priority level")
        filter_parser.add_argument("--due-date", help="Filter by due date in YYYY-MM-DD format")

        # Sort command
        sort_parser = subparsers.add_parser("sort", help="Sort tasks by criteria")
        sort_parser.add_argument("--by", required=True, choices=["priority", "due_date", "title"],
                                help="Sort by criteria: priority, due_date, or title")
        sort_parser.add_argument("--reverse", action="store_true",
                                help="Reverse sort order")

        # Parse the arguments
        try:
            parsed_args = parser.parse_args(args)
        except SystemExit:
            # argparse calls sys.exit() on error, so we'll let it handle the error message
            return

        # Execute the corresponding command
        if parsed_args.command == "add":
            self._handle_add(" ".join(parsed_args.description),
                           priority=parsed_args.priority,
                           tags=parsed_args.tags,
                           due_date=parsed_args.due_date,
                           recurrence=parsed_args.recurrence)
        elif parsed_args.command == "view":
            self._handle_view()
        elif parsed_args.command == "complete":
            self._handle_complete(parsed_args.task_id)
        elif parsed_args.command == "incomplete":
            self._handle_incomplete(parsed_args.task_id)
        elif parsed_args.command == "update":
            self._handle_update(parsed_args.task_id, " ".join(parsed_args.new_description))
        elif parsed_args.command == "delete":
            self._handle_delete(parsed_args.task_id)
        elif parsed_args.command == "search":
            self._handle_search(parsed_args.keyword)
        elif parsed_args.command == "filter":
            self._handle_filter(status=parsed_args.status,
                              priority=parsed_args.priority,
                              due_date=parsed_args.due_date)
        elif parsed_args.command == "sort":
            self._handle_sort(by=parsed_args.by,
                            reverse=parsed_args.reverse)
        elif parsed_args.command is None:
            parser.print_help()
        else:
            print(f"Error: Unknown command '{parsed_args.command}'")
            parser.print_help()

    def _handle_add(self, description: str, priority: str = None, tags: str = None, due_date: str = None, recurrence: str = None):
        """
        Handle the add command.

        Args:
            description (str): Description of the task to add
            priority (str): Priority level (high/medium/low)
            tags (str): Comma-separated tags as string
            due_date (str): Due date in YYYY-MM-DD format
            recurrence (str): Recurrence pattern (daily/weekly/monthly)
        """
        try:
            # Process tags from comma-separated string to list
            tags_list = None
            if tags:
                tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

            # Process due date from string to datetime
            from datetime import datetime
            parsed_due_date = None
            if due_date:
                try:
                    parsed_due_date = datetime.fromisoformat(due_date)
                except ValueError:
                    print(f"Error: Invalid date format: {due_date}. Use YYYY-MM-DD format.")
                    return

            # Validate priority if provided
            if priority:
                try:
                    from ..core.task import Priority
                    if priority not in Priority.VALUES:
                        print(f"Error: Priority must be one of: {', '.join(Priority.VALUES)}")
                        return
                except ValueError as e:
                    print(f"Error: {e}")
                    return

            # Validate recurrence if provided
            if recurrence:
                try:
                    from ..core.task import Recurrence
                    if recurrence not in Recurrence.VALUES:
                        print(f"Error: Recurrence must be one of: {', '.join(Recurrence.VALUES)}")
                        return
                except ValueError as e:
                    print(f"Error: {e}")
                    return

            task = self.task_manager.add_task(description, priority=priority, tags=tags_list, due_date=parsed_due_date, recurrence=recurrence)
            print(f"Added task #{task.id}: {task.description}")
        except InvalidTaskDescriptionError as e:
            print(f"Error: {e}")

    def _handle_view(self):
        """
        Handle the view command.
        """
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("No tasks in the list")
        else:
            formatted_output = self.formatter.format_tasks(tasks)
            print(formatted_output)

    def _handle_complete(self, task_id: int):
        """
        Handle the complete command.

        Args:
            task_id (int): ID of the task to mark as complete
        """
        # Check if task exists first
        task = self.task_manager.get_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} does not exist")
            return

        success = self.task_manager.mark_complete(task_id)
        if success:
            print(f"Task #{task_id} marked as complete")
        else:
            print(f"Error: Task with ID {task_id} does not exist")

    def _handle_incomplete(self, task_id: int):
        """
        Handle the incomplete command.

        Args:
            task_id (int): ID of the task to mark as incomplete
        """
        # Check if task exists first
        task = self.task_manager.get_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} does not exist")
            return

        success = self.task_manager.mark_incomplete(task_id)
        if success:
            print(f"Task #{task_id} marked as incomplete")
        else:
            print(f"Error: Task with ID {task_id} does not exist")

    def _handle_update(self, task_id: int, new_description: str):
        """
        Handle the update command.

        Args:
            task_id (int): ID of the task to update
            new_description (str): New description for the task
        """
        try:
            # Check if task exists first
            task = self.task_manager.get_task_by_id(task_id)
            if task is None:
                print(f"Error: Task with ID {task_id} does not exist")
                return

            success = self.task_manager.update_task(task_id, new_description)
            if success:
                print(f"Task #{task_id} updated to: {new_description}")
            else:
                print(f"Error: Task with ID {task_id} does not exist")
        except InvalidTaskDescriptionError as e:
            print(f"Error: {e}")

    def _handle_delete(self, task_id: int):
        """
        Handle the delete command.

        Args:
            task_id (int): ID of the task to delete
        """
        # Check if task exists first
        task = self.task_manager.get_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} does not exist")
            return

        success = self.task_manager.delete_task(task_id)
        if success:
            print(f"Task #{task_id} deleted")
        else:
            print(f"Error: Task with ID {task_id} does not exist")

    def _handle_search(self, keyword: str):
        """
        Handle the search command.

        Args:
            keyword (str): Keyword to search for in task descriptions
        """
        results = self.task_manager.search_tasks(keyword)
        if results:
            formatted_output = self.formatter.format_tasks(results)
            print(formatted_output)
        else:
            print(f"No tasks found containing '{keyword}'")

    def _handle_filter(self, status: str = None, priority: str = None, due_date: str = None):
        """
        Handle the filter command.

        Args:
            status (str): Filter by completion status (complete/incomplete)
            priority (str): Filter by priority level (high/medium/low)
            due_date (str): Filter by due date in YYYY-MM-DD format
        """
        # Process due date from string to datetime
        from datetime import datetime
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date)
            except ValueError:
                print(f"Error: Invalid date format: {due_date}. Use YYYY-MM-DD format.")
                return

        # Prepare filter criteria
        criteria = {}
        if status:
            criteria['status'] = status
        if priority:
            criteria['priority'] = priority
        if parsed_due_date:
            criteria['due_date'] = parsed_due_date

        # Perform filtering
        results = self.task_manager.filter_tasks(**criteria)
        if results:
            formatted_output = self.formatter.format_tasks(results)
            print(formatted_output)
        else:
            if criteria:
                print(f"No tasks match the filter criteria")
            else:
                print("No tasks match the filter criteria")

    def _handle_sort(self, by: str, reverse: bool = False):
        """
        Handle the sort command.

        Args:
            by (str): Sort by criteria (priority, due_date, title)
            reverse (bool): Whether to reverse the sort order
        """
        try:
            results = self.task_manager.sort_tasks(by=by, reverse=reverse)
            if results:
                formatted_output = self.formatter.format_tasks(results)
                print(formatted_output)
            else:
                print("No tasks to sort")
        except ValueError as e:
            print(f"Error: {e}")

    def run(self, args: Optional[list] = None):
        """
        Run the CLI interface with the provided arguments.

        Args:
            args (Optional[list]): Command-line arguments to parse (default: sys.argv[1:])
        """
        self.parse_and_execute(args)