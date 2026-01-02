# Todo App

A command-line interface todo application with in-memory storage.

## Overview

This is a simple CLI-based todo application that allows users to manage tasks through command-line interface. All data is stored in-memory during a single session and is not persisted between runs.

## Features

- Add new tasks
- View all tasks
- Mark tasks as complete/incomplete
- Update task descriptions
- Delete tasks

## Prerequisites

- Python 3.13+

## Installation

No installation required. The application runs directly from the source code.

## Usage

### Add a Task
```bash
python -m src.todo_app add "Task description here"
```

### View All Tasks
```bash
python -m src.todo_app view
```

### Mark Task as Complete
```bash
python -m src.todo_app complete [task_id]
```

### Mark Task as Incomplete
```bash
python -m src.todo_app incomplete [task_id]
```

### Update Task Description
```bash
python -m src.todo_app update [task_id] "New description here"
```

### Delete a Task
```bash
python -m src.todo_app delete [task_id]
```

## Example

```bash
# Add tasks
python -m src.todo_app add "Buy groceries"
python -m src.todo_app add "Walk the dog"

# View all tasks
python -m src.todo_app view

# Mark a task as complete
python -m src.todo_app complete 1

# Update a task description
python -m src.todo_app update 2 "Walk the golden retriever"

# Delete a task
python -m src.todo_app delete 2

# View tasks again
python -m src.todo_app view
```

## Architecture

The application follows a modular design:

- `src/todo_app/core/` - Contains core data models and business logic
- `src/todo_app/cli/` - Contains command-line interface components
- `src/todo_app/main.py` - Application entry point

## Data Model

Each task has:
- ID: A unique identifier (sequential integer)
- Description: The text content of the task
- Completion status: Boolean indicating if the task is complete

## Limitations

- Data is stored only in memory and does not persist between sessions
- Single-user application
- No external dependencies beyond Python standard library