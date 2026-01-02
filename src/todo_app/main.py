"""
Main Application Entry Point

Orchestrates the todo application components.
"""

import sys
from todo_app.core.task_manager import TaskManager
from todo_app.cli.interface import CLIInterface


def main():
    """
    Main function to run the todo application.
    Supports both command-line arguments and interactive mode.
    """
    task_manager = TaskManager()
    cli_interface = CLIInterface(task_manager)

    # Check if command-line arguments were provided
    if len(sys.argv) > 1:
        # Run with command-line arguments
        cli_interface.parse_and_execute(sys.argv[1:])
    else:
        # Run in interactive mode
        print("Welcome to the Todo App!")
        print("Available commands:")
        print("  add [task description]     - Add a new task")
        print("  view                       - View all tasks")
        print("  complete [task_id]         - Mark a task as complete")
        print("  incomplete [task_id]       - Mark a task as incomplete")
        print("  update [task_id] [new description] - Update task description")
        print("  delete [task_id]           - Delete a task")
        print("  priority [task_id] [low|medium|high] - Set task priority")
        print("  tag add [task_id] [tag]    - Add tag to task")
        print("  tag remove [task_id] [tag] - Remove tag from task")
        print("  search [keyword]           - Search tasks by keyword")
        print("  filter [options]           - Filter tasks (use --status or --priority)")
        print("  sort [priority|alpha]      - Sort tasks by priority or alphabetically")
        print("  help                       - Show this help message")
        print("  exit or quit               - Exit the application")
        print()

        # Interactive command loop
        while True:
            try:
                # Prompt user for command
                command_input = input("todo> ").strip()

                if not command_input:
                    continue

                # Split the command into parts
                parts = command_input.split()
                command = parts[0].lower()

                # Handle exit/quit commands
                if command in ['exit', 'quit']:
                    print("Goodbye!")
                    break

                # Handle help command
                elif command == 'help':
                    print("Available commands:")
                    print("  add [task description]     - Add a new task")
                    print("  view                       - View all tasks")
                    print("  complete [task_id]         - Mark a task as complete")
                    print("  incomplete [task_id]       - Mark a task as incomplete")
                    print("  update [task_id] [new description] - Update task description")
                    print("  delete [task_id]           - Delete a task")
                    print("  priority [task_id] [low|medium|high] - Set task priority")
                    print("  tag add [task_id] [tag]    - Add tag to task")
                    print("  tag remove [task_id] [tag] - Remove tag from task")
                    print("  search [keyword]           - Search tasks by keyword")
                    print("  filter [options]           - Filter tasks (use --status or --priority)")
                    print("  sort [priority|alpha]      - Sort tasks by priority or alphabetically")
                    print("  help                       - Show this help message")
                    print("  exit or quit               - Exit the application")
                    print()

                # Handle add command
                elif command == 'add':
                    if len(parts) < 2:
                        print("Error: Please provide a task description. Usage: add [task description]")
                    else:
                        description = ' '.join(parts[1:])
                        try:
                            task = task_manager.add_task(description)
                            print(f"Added task #{task.id}: {task.description}")
                        except Exception as e:
                            print(f"Error: {e}")

                # Handle view command
                elif command == 'view':
                    tasks = task_manager.get_all_tasks()
                    if not tasks:
                        print("No tasks in the list")
                    else:
                        formatted_output = cli_interface.formatter.format_tasks(tasks)
                        print(formatted_output)

                # Handle complete command
                elif command == 'complete':
                    if len(parts) != 2:
                        print("Error: Please provide a task ID. Usage: complete [task_id]")
                    else:
                        try:
                            task_id = int(parts[1])
                            success = task_manager.mark_complete(task_id)
                            if success:
                                print(f"Task #{task_id} marked as complete")
                            else:
                                print(f"Error: Task with ID {task_id} does not exist")
                        except ValueError:
                            print("Error: Task ID must be a number")

                # Handle incomplete command
                elif command == 'incomplete':
                    if len(parts) != 2:
                        print("Error: Please provide a task ID. Usage: incomplete [task_id]")
                    else:
                        try:
                            task_id = int(parts[1])
                            success = task_manager.mark_incomplete(task_id)
                            if success:
                                print(f"Task #{task_id} marked as incomplete")
                            else:
                                print(f"Error: Task with ID {task_id} does not exist")
                        except ValueError:
                            print("Error: Task ID must be a number")

                # Handle update command
                elif command == 'update':
                    if len(parts) < 3:
                        print("Error: Please provide a task ID and new description. Usage: update [task_id] [new description]")
                    else:
                        try:
                            task_id = int(parts[1])
                            new_description = ' '.join(parts[2:])

                            # Validate task exists first
                            task = task_manager.get_task_by_id(task_id)
                            if task is None:
                                print(f"Error: Task with ID {task_id} does not exist")
                            else:
                                success = task_manager.update_task(task_id, new_description)
                                if success:
                                    print(f"Task #{task_id} updated to: {new_description}")
                                else:
                                    print(f"Error: Task with ID {task_id} does not exist")
                        except ValueError:
                            print("Error: Task ID must be a number")

                # Handle delete command
                elif command == 'delete':
                    if len(parts) != 2:
                        print("Error: Please provide a task ID. Usage: delete [task_id]")
                    else:
                        try:
                            task_id = int(parts[1])
                            success = task_manager.delete_task(task_id)
                            if success:
                                print(f"Task #{task_id} deleted")
                            else:
                                print(f"Error: Task with ID {task_id} does not exist")
                        except ValueError:
                            print("Error: Task ID must be a number")

                # Handle priority command
                elif command == 'priority':
                    if len(parts) != 3:
                        print("Error: Please provide task ID and priority. Usage: priority [task_id] [low|medium|high]")
                    else:
                        try:
                            task_id = int(parts[1])
                            priority = parts[2].lower()

                            # Validate priority value
                            if priority not in ['low', 'medium', 'high']:
                                print("Error: Priority must be one of: low, medium, high")
                                continue

                            # Get the task and update its priority
                            task = task_manager.get_task_by_id(task_id)
                            if task is None:
                                print(f"Error: Task with ID {task_id} does not exist")
                            else:
                                task.priority = priority
                                print(f"Task #{task_id} priority set to {priority}")
                        except ValueError:
                            print("Error: Task ID must be a number")

                # Handle tag command
                elif command == 'tag':
                    if len(parts) < 3:
                        print("Error: Please provide tag action, task ID, and tag. Usage: tag add [task_id] [tag] or tag remove [task_id] [tag]")
                    else:
                        tag_action = parts[1].lower()
                        try:
                            task_id = int(parts[2])
                            tag = parts[3] if len(parts) > 3 else None

                            if tag_action not in ['add', 'remove']:
                                print("Error: Tag action must be 'add' or 'remove'")
                                continue

                            if not tag:
                                print("Error: Please provide a tag name")
                                continue

                            # Get the task and modify its tags
                            task = task_manager.get_task_by_id(task_id)
                            if task is None:
                                print(f"Error: Task with ID {task_id} does not exist")
                            elif tag_action == 'add':
                                if tag not in task.tags:
                                    task.tags = task.tags + [tag]  # Create new list to avoid direct mutation issues
                                    print(f"Tag '{tag}' added to task #{task_id}")
                                else:
                                    print(f"Tag '{tag}' already exists on task #{task_id}")
                            elif tag_action == 'remove':
                                if tag in task.tags:
                                    new_tags = [t for t in task.tags if t != tag]
                                    task.tags = new_tags
                                    print(f"Tag '{tag}' removed from task #{task_id}")
                                else:
                                    print(f"Tag '{tag}' does not exist on task #{task_id}")
                        except ValueError:
                            print("Error: Task ID must be a number")

                # Handle search command
                elif command == 'search':
                    if len(parts) < 2:
                        print("Error: Please provide a keyword to search for. Usage: search [keyword]")
                    else:
                        keyword = ' '.join(parts[1:])
                        results = task_manager.search_tasks(keyword)
                        if not results:
                            print(f"No tasks found containing '{keyword}'")
                        else:
                            formatted_output = cli_interface.formatter.format_tasks(results)
                            print(formatted_output)

                # Handle filter command
                elif command == 'filter':
                    # Parse filter options
                    status = None
                    priority_filter = None

                    i = 1
                    while i < len(parts):
                        if parts[i] == '--status' and i + 1 < len(parts):
                            status = parts[i + 1].lower()
                            if status not in ['complete', 'incomplete', 'completed', 'pending']:
                                print("Error: Status must be one of: complete, incomplete, completed, pending")
                                break
                            i += 2
                        elif parts[i] == '--priority' and i + 1 < len(parts):
                            priority_filter = parts[i + 1].lower()
                            if priority_filter not in ['low', 'medium', 'high']:
                                print("Error: Priority must be one of: low, medium, high")
                                break
                            i += 2
                        else:
                            print("Error: Unknown filter option. Use --status or --priority")
                            break
                    else:
                        # If loop completed without break
                        criteria = {}
                        if status:
                            criteria['status'] = status
                        if priority_filter:
                            criteria['priority'] = priority_filter

                        results = task_manager.filter_tasks(**criteria)
                        if not results:
                            print("No tasks match the filter criteria")
                        else:
                            formatted_output = cli_interface.formatter.format_tasks(results)
                            print(formatted_output)

                # Handle sort command
                elif command == 'sort':
                    if len(parts) < 2:
                        print("Error: Please provide sort criteria. Usage: sort [priority|alpha]")
                    else:
                        sort_by = parts[1].lower()
                        if sort_by not in ['priority', 'alpha']:
                            print("Error: Sort criteria must be 'priority' or 'alpha'")
                        else:
                            # Map alpha to title for consistency with TaskManager
                            by_param = 'priority' if sort_by == 'priority' else 'title'
                            results = task_manager.sort_tasks(by=by_param)
                            if not results:
                                print("No tasks to sort")
                            else:
                                formatted_output = cli_interface.formatter.format_tasks(results)
                                print(formatted_output)

                # Handle unknown command
                else:
                    print(f"Error: Unknown command '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break


if __name__ == "__main__":
    main()