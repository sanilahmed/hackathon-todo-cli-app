# Data Model: The Evolution of Todo – Phase I Advanced Level: Intelligent Features

**Feature**: The Evolution of Todo – Phase I Advanced Level: Intelligent Features
**Date**: 2025-12-31
**Branch**: `001-todo-intelligent-scheduling`

## Entity Definitions

### Task Entity (Enhanced)

The Task entity is enhanced to support intelligent scheduling features while maintaining backward compatibility.

#### Attributes
- **id** (int): Unique identifier for the task
  - Primary key, auto-incremented
  - Example: 1, 2, 3

- **description** (str): Text content of the task
  - Required field
  - Example: "Submit quarterly report"

- **completed** (bool): Completion status of the task
  - Default: False
  - Example: True, False

- **priority** (str): Priority level of the task
  - Values: "high", "medium", "low"
  - Default: "medium"
  - Example: "high"

- **tags** (List[str]): List of tags associated with the task
  - Optional, default: empty list
  - Example: ["work", "urgent"]

- **due_date** (Optional[datetime]): Due date and time for the task
  - Optional, default: None
  - Format: datetime object in ISO format
  - Example: datetime(2024, 12, 31, 0, 0)

- **recurrence** (Optional[str]): Recurrence pattern for the task
  - Optional, default: None
  - Values: "daily", "weekly", "monthly"
  - Example: "daily"

#### Methods
- `is_overdue()` → bool: Returns True if task is overdue (due_date < current date)
- `is_upcoming()` → bool: Returns True if task is due soon (within 24 hours)
- `calculate_next_occurrence()` → datetime: Calculates next occurrence based on recurrence pattern
- `to_dict()` → dict: Returns dictionary representation of the task

#### Relationships
- No direct relationships with other entities
- Each recurring task creates a new instance when completed

#### Backward Compatibility
- Existing tasks without due_date or recurrence will continue to function
- New attributes have appropriate default values
- All existing functionality remains unchanged

### Recurring Task Entity (Virtual)

A recurring task is a special case of the Task entity with a recurrence pattern. It's not a separate entity but rather a Task with recurrence information.

#### Special Behavior
- When marked complete, automatically creates a new Task instance with the next occurrence date
- Only one instance of a recurring task exists at a time (until completed)
- Next occurrence calculated based on recurrence pattern and current date

#### Recurrence Patterns
- **daily**: Creates a new instance with due date = current date + 1 day
- **weekly**: Creates a new instance with due date = current date + 7 days
- **monthly**: Creates a new instance with due date = current date + 1 month (with month-end handling)

### Due Date Entity (Virtual)

Due date functionality is implemented as a property of the Task entity rather than a separate entity.

#### Properties
- **overdue**: due_date < current date
- **upcoming**: current date <= due_date <= current date + 24 hours
- **future**: due_date > current date + 24 hours

## Data Flow

### Task Creation
1. User creates a task via CLI
2. TaskManager.add_task() creates a new Task instance
3. If due_date or recurrence provided, they are validated and stored
4. Task is added to in-memory storage

### Task Completion (for recurring tasks)
1. User marks a recurring task complete
2. TaskManager.mark_complete() processes the completion
3. If task has recurrence, calculate_next_occurrence() is called
4. A new Task instance is created with the next occurrence date
5. The new task is added to in-memory storage

### Due Date Processing
1. When viewing tasks, TaskManager.get_all_tasks() returns all tasks
2. Formatter checks each task for due date status (overdue, upcoming)
3. Appropriate indicators are added to the display format

## Validation Rules

### Due Date Validation
- Must be in valid ISO format (YYYY-MM-DD)
- Date values must be valid (e.g., no February 30th)
- Optional field - tasks without due dates are valid

### Recurrence Validation
- Must be one of: "daily", "weekly", "monthly"
- Optional field - tasks without recurrence are valid
- Invalid values are rejected with error message

### Month-End Handling
- For monthly recurrence, if the day doesn't exist in the target month, use the last day of that month
- Example: January 31st recurring monthly becomes February 28th/29th

## Storage Format

### In-Memory Representation
Tasks are stored as Task objects in a Python list within TaskManager:
```python
_tasks: List[Task]
```

### Data Persistence (None)
- No persistence layer - all data stored in-memory only
- Data is lost when application terminates
- Recurring tasks only exist in the current session

## Migration Considerations

### Existing Tasks
- Tasks created before this feature will have due_date=None and recurrence=None
- All existing functionality continues to work unchanged
- New attributes are optional with appropriate defaults

### Future Extensions
- Data model supports additional scheduling features (e.g., time of day, multiple due dates)
- Recurrence patterns could be extended with more complex rules
- Calendar integration could be added as a future enhancement