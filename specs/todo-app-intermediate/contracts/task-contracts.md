# Task Contracts: The Evolution of Todo – Phase II (Intermediate Level)

**Created**: 2025-12-31
**Feature**: /specs/todo-app-intermediate/spec.md

## Overview

This document defines the contracts for the enhanced Task model in Phase II, including the data structure, validation rules, and API contracts for the Task and TaskManager classes.

## Task Data Contract

### Task Class Definition

```python
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
```

### Field Specifications

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| id | int | Yes | - | > 0 | Unique identifier for the task |
| description | str | Yes | - | Non-empty | Text description of the task |
| completed | bool | No | False | Boolean | Completion status |
| priority | str | No | "medium" | One of ["high", "medium", "low"] | Priority level |
| tags | List[str] | No | [] | Each tag: non-empty, no commas | List of category tags |
| due_date | Optional[datetime] | No | None | Valid date format | Due date for the task |

### Validation Rules

1. **ID Validation**:
   - Must be a positive integer
   - Must be unique within the task collection

2. **Description Validation**:
   - Must not be empty or contain only whitespace
   - Maximum length: 1000 characters

3. **Priority Validation**:
   - Must be one of: "high", "medium", "low" (case-sensitive)
   - If not provided, defaults to "medium"

4. **Tags Validation**:
   - Each tag must be non-empty and not contain commas
   - Tags are stored as a list of strings
   - If not provided, defaults to empty list

5. **Due Date Validation**:
   - If provided, must be a valid datetime object
   - Format should be ISO format (YYYY-MM-DD or ISO 8601)

## TaskManager API Contracts

### Method Signatures

```python
class TaskManager:
    def add_task(self, description: str, priority: str = "medium",
                 tags: List[str] = None, due_date: Optional[datetime] = None) -> Task:
        """Add a new task with optional priority, tags, and due date.

        Args:
            description: Task description (required)
            priority: Priority level (optional, defaults to "medium")
            tags: List of tags (optional, defaults to empty list)
            due_date: Due date (optional, defaults to None)

        Returns:
            Task: The created Task object with assigned ID

        Raises:
            ValueError: If priority is not valid
        """

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in description (case-insensitive).

        Args:
            keyword: Search term to find in task descriptions

        Returns:
            List[Task]: List of tasks containing the keyword
        """

    def filter_tasks(self, **criteria) -> List[Task]:
        """Filter tasks by various criteria.

        Args:
            **criteria: Filter criteria (status, priority, due_date)

        Returns:
            List[Task]: List of tasks matching all criteria

        Supported criteria:
            status: "complete", "incomplete", "completed", "pending"
            priority: "high", "medium", "low"
            due_date: datetime object to match
        """

    def sort_tasks(self, by: str, reverse: bool = False) -> List[Task]:
        """Sort tasks by specified criteria.

        Args:
            by: Sort criteria ("priority", "due_date", "title")
            reverse: Whether to reverse the sort order (optional, defaults to False)

        Returns:
            List[Task]: Sorted list of tasks (does not modify original order)

        Raises:
            ValueError: If 'by' is not a valid sort criteria
        """
```

## CLI Command Contracts

### Command-Line Interface Specification

#### Add Command
```
add "task description" [--priority PRIORITY] [--tags TAGS] [--due-date DATE]

Parameters:
  "task description"  Required task description in quotes
  --priority          Optional priority: high, medium, low (default: medium)
  --tags              Optional comma-separated tags (e.g., work,urgent)
  --due-date          Optional due date in YYYY-MM-DD format

Example:
  add "Complete project" --priority high --tags work,important --due-date 2025-01-15
```

#### Search Command
```
search "keyword"

Parameters:
  "keyword"  Search term to find in task descriptions

Example:
  search "project"
```

#### Filter Command
```
filter [--status STATUS] [--priority PRIORITY] [--due-date DATE]

Parameters:
  --status      Filter by completion status: complete, incomplete
  --priority    Filter by priority: high, medium, low
  --due-date    Filter by due date in YYYY-MM-DD format

Example:
  filter --status incomplete --priority high
```

#### Sort Command
```
sort --by CRITERIA [--reverse]

Parameters:
  --by      Sort criteria: priority, due_date, title
  --reverse Reverse sort order (optional flag)

Example:
  sort --by priority
  sort --by due_date --reverse
```

## Backward Compatibility Contract

### Existing Functionality Preservation

All Phase I functionality must continue to work without changes:

1. **Add Command**: Existing usage without new parameters must continue to work
   - `add "task description"` should work as before

2. **View Command**: Should display new fields appropriately
   - Existing tasks should show default values for new fields

3. **Complete/Incomplete Commands**: Should work unchanged
   - No impact on priority, tags, or due_date

4. **Update/Delete Commands**: Should work unchanged
   - Only affects description and completion status

### Default Values for Existing Tasks

When existing tasks (without Phase II attributes) are displayed or processed:
- Priority: "medium" (default)
- Tags: [] (empty list)
- Due Date: None

## Error Contract

### Error Response Format

All errors should follow this format:
```
Error: [descriptive error message]
```

### Valid Error Scenarios

1. **Invalid Priority**: "Error: Priority must be one of high, medium, low"
2. **Invalid Date Format**: "Error: Invalid date format: [input]. Use YYYY-MM-DD format."
3. **Empty Description**: "Error: Task description cannot be empty"
4. **Unknown Command**: "Error: Unknown command [command]. Use 'help' for available commands."

## Performance Contract

### Performance Expectations

- Search operations: Complete in < 100ms for up to 1000 tasks
- Filter operations: Complete in < 100ms for up to 1000 tasks
- Sort operations: Complete in < 200ms for up to 1000 tasks
- All operations should be memory efficient (no unnecessary copies)

## Testing Contract

### Required Test Cases

1. **Unit Tests**:
   - Task creation with all field combinations
   - Validation error cases
   - Search, filter, sort functionality

2. **Integration Tests**:
   - CLI command integration
   - Backward compatibility verification
   - Error handling verification

3. **Performance Tests**:
   - Operations with 1000+ tasks
   - Memory usage verification