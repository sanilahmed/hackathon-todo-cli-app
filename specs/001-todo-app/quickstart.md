# Quickstart Guide: In-Memory Python Console Todo App

**Date**: 2025-12-28
**Feature**: 001-todo-app
**Target Audience**: Developers and users of the todo application

## Overview

This quickstart guide provides step-by-step instructions to set up, run, and use the In-Memory Python Console Todo App. The application allows you to manage tasks through a command-line interface with no data persistence.

## Prerequisites

- Python 3.13+ installed on your system
- UV package manager installed
- Basic command-line interface knowledge

## Setup Instructions

### 1. Clone or Access the Repository
```bash
# Navigate to your project directory
cd /path/to/todo-app
```

### 2. Set Up the Environment
```bash
# Install dependencies using UV (if any needed beyond standard library)
# For this project, no external dependencies are required beyond Python standard library
```

### 3. Verify Python Version
```bash
python --version
# Should show Python 3.13 or higher
```

## Running the Application

### Execute the Todo App
```bash
# Run the application using Python module syntax
python -m src.todo_app [command] [arguments]

# Or if you have a main entry point configured
python src/todo_app/main.py [command] [arguments]
```

## Core Commands

### Add a Task
```bash
python -m src.todo_app add "Task description here"
```
Example:
```bash
python -m src.todo_app add "Buy groceries"
# Output: Added task #1: Buy groceries
```

### View All Tasks
```bash
python -m src.todo_app view
```
Example:
```bash
python -m src.todo_app view
# Output:
# ID | Status    | Description
# ---|-----------|------------------
# 1  | Incomplete| Buy groceries
# 2  | Complete  | Finish report
```

### Mark Task as Complete
```bash
python -m src.todo_app complete [task_id]
```
Example:
```bash
python -m src.todo_app complete 1
# Output: Task #1 marked as complete
```

### Mark Task as Incomplete
```bash
python -m src.todo_app incomplete [task_id]
```
Example:
```bash
python -m src.todo_app incomplete 2
# Output: Task #2 marked as incomplete
```

### Update Task Description
```bash
python -m src.todo_app update [task_id] "New description"
```
Example:
```bash
python -m src.todo_app update 1 "Buy groceries and cook dinner"
# Output: Task #1 updated to: Buy groceries and cook dinner
```

### Delete a Task
```bash
python -m src.todo_app delete [task_id]
```
Example:
```bash
python -m src.todo_app delete 1
# Output: Task #1 deleted
```

## Example Workflow

Here's a complete example of using the todo app:

```bash
# Add some tasks
python -m src.todo_app add "Complete project proposal"
python -m src.todo_app add "Schedule team meeting"
python -m src.todo_app add "Review documentation"

# View all tasks
python -m src.todo_app view

# Mark a task as complete
python -m src.todo_app complete 1

# Update a task description
python -m src.todo_app update 2 "Schedule team meeting for Friday"

# View tasks again to see changes
python -m src.todo_app view

# Delete a completed task
python -m src.todo_app delete 1

# Final view
python -m src.todo_app view
```

## Error Handling

### Common Errors and Solutions

1. **Invalid Task ID**
   - Error: "Task with ID X does not exist"
   - Solution: Check the task ID exists by running `view` command first

2. **Missing Arguments**
   - Error: "Missing required arguments"
   - Solution: Ensure you provide all required arguments for each command

3. **Empty Task Description**
   - Error: "Task description cannot be empty"
   - Solution: Provide a non-empty description when adding or updating tasks

## Important Notes

- **Data Persistence**: This application stores all data in memory only. All tasks will be lost when the application exits.
- **Session-Based**: Each run of the application starts with an empty task list.
- **Task IDs**: Task IDs are sequential and unique within a session but are not reused after deletion.
- **No External Dependencies**: The application only uses Python standard library components.

## Troubleshooting

### Application Won't Start
- Verify Python 3.13+ is installed and accessible
- Check that the file paths are correct
- Ensure you're running from the correct directory

### Commands Not Working
- Verify the command syntax matches the examples above
- Ensure task IDs exist before attempting operations on them
- Check for special characters in task descriptions that might interfere with command parsing

## Next Steps

- Review the full specification in `spec.md` for detailed requirements
- Check the implementation plan in `plan.md` for architectural details
- Explore the source code in the `/src` directory for implementation details