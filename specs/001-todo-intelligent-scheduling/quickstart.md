# Quickstart Guide: The Evolution of Todo – Phase I Advanced Level: Intelligent Features

**Feature**: The Evolution of Todo – Phase I Advanced Level: Intelligent Features
**Date**: 2025-12-31
**Branch**: `001-todo-intelligent-scheduling`

## Getting Started

This guide demonstrates how to use the new intelligent scheduling features in the CLI Todo application.

### Prerequisites
- Python 3.13+
- UV package manager (for dependency management)
- Basic familiarity with command-line interfaces

### Setup
1. Clone or navigate to the project directory
2. Create virtual environment: `uv venv`
3. Activate environment: `source .venv/bin/activate`
4. Install dependencies: `uv pip install -e .`
5. Run the application: `python -m src.todo_app.main`

## Feature Walkthrough

### 1. Adding Tasks with Due Dates

Create a task with a due date:
```bash
python -m src.todo_app.main add "Submit quarterly report" --due-date "2024-12-31"
```

Create a recurring task:
```bash
python -m src.todo_app.main add "Daily exercise" --recurrence daily
```

Create a task with both due date and recurrence:
```bash
python -m src.todo_app.main add "Weekly team meeting" --due-date "2024-12-01" --recurrence weekly
```

### 2. Viewing Tasks with Due Date Indicators

Run the view command to see all tasks:
```bash
python -m src.todo_app.main view
```

The output will show:
- Due dates in the format YYYY-MM-DD
- Overdue tasks marked with [OVERDUE] indicator
- Upcoming tasks (due within 24 hours) marked with [DUE SOON] indicator
- Recurring tasks marked with recurrence pattern (DAILY, WEEKLY, MONTHLY)

### 3. Working with Recurring Tasks

When you complete a recurring task, the system automatically creates a new instance:
```bash
python -m src.todo_app.main complete 1
```

The original task will be marked complete, and a new instance will be created with the next occurrence date based on the recurrence pattern.

### 4. Example Workflow

Here's a complete workflow demonstrating the features:

1. Add a recurring daily task:
```bash
python -m src.todo_app.main add "Morning meditation" --recurrence daily
```

2. Add a task with a due date:
```bash
python -m src.todo_app.main add "Pay electricity bill" --due-date "2024-12-15"
```

3. View all tasks:
```bash
python -m src.todo_app.main view
```

4. Complete the recurring task (this will create a new instance):
```bash
python -m src.todo_app.main complete 1
```

5. View tasks again to see the new recurring instance:
```bash
python -m src.todo_app.main view
```

## Validation and Error Handling

The system validates inputs and provides clear error messages:

Invalid date format:
```bash
python -m src.todo_app.main add "Task" --due-date "invalid-date"
# Output: Error: Invalid date format: invalid-date. Use YYYY-MM-DD format.
```

Invalid recurrence pattern:
```bash
python -m src.todo_app.main add "Task" --recurrence yearly
# Output: Error: Recurrence must be one of: daily, weekly, monthly
```

## Testing the Features

Run the existing test suite to verify all functionality:
```bash
python -m pytest tests/
```

All existing tests should pass, confirming that the new features don't break existing functionality.

## Troubleshooting

### Common Issues

1. **Date Format Errors**: Ensure dates are in YYYY-MM-DD format (e.g., "2024-12-31")

2. **Recurrence Pattern Errors**: Use only "daily", "weekly", or "monthly" for recurrence

3. **Overdue Tasks Not Showing**: Verify system date is correct and task due dates are in the past

### Verification Steps

1. Confirm recurring tasks create new instances when completed
2. Verify due date indicators appear correctly in task listings
3. Ensure overdue and upcoming tasks are properly highlighted
4. Test month-end date handling for monthly recurring tasks