# Quickstart Guide: The Evolution of Todo – Phase II (Intermediate Level)

**Created**: 2025-12-31
**Feature**: /specs/todo-app-intermediate/spec.md

## Overview

This quickstart guide provides immediate hands-on instructions for implementing and using the Phase II features (priorities, tags, search, filter, sort) in the Todo CLI application.

## Setup

### Prerequisites
- Python 3.13+
- UV package manager
- Virtual environment (recommended)

### Environment Setup
```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install project in development mode
uv pip install -e .
```

## Implementation Quickstart

### 1. Enhanced Task Model

Create the enhanced Task model with priority, tags, and due_date:

```python
# src/todo_app/core/task.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Priority:
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VALUES = [HIGH, MEDIUM, LOW]

@dataclass
class Task:
    id: int
    description: str
    completed: bool = False
    priority: str = Priority.MEDIUM  # Default to medium
    tags: List[str] = None  # List of tags
    due_date: Optional[datetime] = None  # Optional due date

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
```

### 2. Enhanced TaskManager

Implement search, filter, and sort functionality:

```python
# src/todo_app/core/task_manager.py
from typing import List, Dict, Any, Optional
from datetime import datetime
from .task import Task, Priority

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, description: str, priority: str = Priority.MEDIUM,
                 tags: List[str] = None, due_date: Optional[datetime] = None) -> Task:
        if tags is None:
            tags = []
        if priority not in Priority.VALUES:
            raise ValueError(f"Priority must be one of {Priority.VALUES}")

        task = Task(
            id=self.next_id,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in description (case-insensitive)."""
        keyword = keyword.lower()
        return [task for task in self.tasks if keyword in task.description.lower()]

    def filter_tasks(self, **criteria) -> List[Task]:
        """Filter tasks by various criteria."""
        filtered_tasks = self.tasks

        if 'status' in criteria:
            status = criteria['status']
            if status in ['complete', 'completed']:
                filtered_tasks = [task for task in filtered_tasks if task.completed]
            elif status in ['incomplete', 'pending']:
                filtered_tasks = [task for task in filtered_tasks if not task.completed]

        if 'priority' in criteria:
            priority = criteria['priority']
            if priority in Priority.VALUES:
                filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        if 'due_date' in criteria:
            due_date = criteria['due_date']
            filtered_tasks = [task for task in filtered_tasks
                             if task.due_date and task.due_date.date() == due_date.date()]

        return filtered_tasks

    def sort_tasks(self, by: str, reverse: bool = False) -> List[Task]:
        """Sort tasks by specified criteria."""
        if by == 'priority':
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            return sorted(self.tasks,
                         key=lambda task: priority_order[task.priority],
                         reverse=reverse)
        elif by == 'due_date':
            return sorted(self.tasks,
                         key=lambda task: (task.due_date is None, task.due_date),
                         reverse=reverse)
        elif by == 'title':
            return sorted(self.tasks,
                         key=lambda task: task.description.lower(),
                         reverse=reverse)
        else:
            return self.tasks.copy()
```

### 3. CLI Extensions

Add new commands to the CLI interface:

```python
# src/todo_app/cli/interface.py
from typing import List
import argparse
from datetime import datetime
from ..core.task_manager import TaskManager
from ..core.task import Priority

class TodoCLI:
    def __init__(self):
        self.task_manager = TaskManager()

    def add_task(self, args):
        """Add a task with optional priority, tags, and due date."""
        priority = args.priority or Priority.MEDIUM
        tags = args.tags.split(',') if args.tags else []
        due_date = None
        if args.due_date:
            try:
                due_date = datetime.fromisoformat(args.due_date)
            except ValueError:
                print(f"Invalid date format: {args.due_date}. Use YYYY-MM-DD format.")
                return

        task = self.task_manager.add_task(
            description=args.description,
            priority=priority,
            tags=tags,
            due_date=due_date
        )
        print(f"Added task #{task.id}: {task.description}")

    def search_tasks(self, args):
        """Search tasks by keyword."""
        results = self.task_manager.search_tasks(args.keyword)
        if results:
            for task in results:
                self.display_task(task)
        else:
            print("No tasks found matching your search.")

    def filter_tasks(self, args):
        """Filter tasks by criteria."""
        criteria = {}
        if args.status:
            criteria['status'] = args.status
        if args.priority:
            criteria['priority'] = args.priority
        if args.due_date:
            try:
                criteria['due_date'] = datetime.fromisoformat(args.due_date)
            except ValueError:
                print(f"Invalid date format: {args.due_date}. Use YYYY-MM-DD format.")
                return

        results = self.task_manager.filter_tasks(**criteria)
        if results:
            for task in results:
                self.display_task(task)
        else:
            print("No tasks match your filter criteria.")

    def sort_tasks(self, args):
        """Sort tasks by specified criteria."""
        results = self.task_manager.sort_tasks(by=args.by, reverse=args.reverse)
        for task in results:
            self.display_task(task)

    def setup_arg_parser(self):
        """Set up command-line argument parser."""
        parser = argparse.ArgumentParser(description="Todo CLI Application")
        subparsers = parser.add_subparsers(dest='command')

        # Add task with priority/tags/due_date support
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('description', help='Task description')
        add_parser.add_argument('--priority', choices=Priority.VALUES,
                               help='Task priority (high/medium/low)')
        add_parser.add_argument('--tags', help='Comma-separated tags (e.g., work,urgent)')
        add_parser.add_argument('--due-date', help='Due date in YYYY-MM-DD format')

        # Search command
        search_parser = subparsers.add_parser('search', help='Search tasks by keyword')
        search_parser.add_argument('keyword', help='Keyword to search for')

        # Filter command
        filter_parser = subparsers.add_parser('filter', help='Filter tasks')
        filter_parser.add_argument('--status', choices=['complete', 'incomplete', 'completed', 'pending'],
                                  help='Filter by completion status')
        filter_parser.add_argument('--priority', choices=Priority.VALUES,
                                  help='Filter by priority')
        filter_parser.add_argument('--due-date', help='Filter by due date (YYYY-MM-DD)')

        # Sort command
        sort_parser = subparsers.add_parser('sort', help='Sort tasks')
        sort_parser.add_argument('--by', choices=['priority', 'due_date', 'title'],
                                required=True, help='Sort by criteria')
        sort_parser.add_argument('--reverse', action='store_true',
                                help='Reverse sort order')

        return parser
```

## Usage Examples

### Adding Tasks with New Features
```bash
# Add a high priority task with tags
python -m src.todo_app.main add "Complete project proposal" --priority high --tags work,important

# Add a task with due date
python -m src.todo_app.main add "Buy groceries" --due-date 2025-01-15

# Add a task with all features
python -m src.todo_app.main add "Prepare presentation" --priority medium --tags work,presentation --due-date 2025-01-10
```

### Searching Tasks
```bash
# Search for tasks containing "project"
python -m src.todo_app.main search "project"

# Search is case-insensitive
python -m src.todo_app.main search "PROJECT"
```

### Filtering Tasks
```bash
# Filter by completion status
python -m src.todo_app.main filter --status complete

# Filter by priority
python -m src.todo_app.main filter --priority high

# Filter by due date
python -m src.todo_app.main filter --due-date 2025-01-15

# Combine filters
python -m src.todo_app.main filter --status incomplete --priority high
```

### Sorting Tasks
```bash
# Sort by priority (high to low)
python -m src.todo_app.main sort --by priority

# Sort by due date (chronological)
python -m src.todo_app.main sort --by due_date

# Sort alphabetically by title
python -m src.todo_app.main sort --by title

# Reverse sort order
python -m src.todo_app.main sort --by priority --reverse
```

## Testing Quickstart

Run the tests to verify implementation:

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/unit/test_task.py
pytest tests/unit/test_task_manager.py
pytest tests/unit/test_cli.py
```

## Validation Checklist

- [ ] Task model supports priority, tags, and due_date
- [ ] Search functionality works by keyword
- [ ] Filter functionality works by status, priority, and date
- [ ] Sort functionality works by priority, due_date, and title
- [ ] All existing functionality continues to work
- [ ] Help system includes new commands
- [ ] Error messages are user-friendly
- [ ] Performance is acceptable (sub-second operations)