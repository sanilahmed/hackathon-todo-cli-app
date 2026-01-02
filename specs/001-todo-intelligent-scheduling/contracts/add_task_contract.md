# Contract: Add Task with Intelligent Scheduling

**Feature**: The Evolution of Todo – Phase I Advanced Level: Intelligent Features
**Contract**: Add Task with Due Date and Recurrence
**Date**: 2025-12-31
**Branch**: `001-todo-intelligent-scheduling`

## Overview

This contract defines the behavior for adding tasks with due dates and recurrence patterns to the todo application.

## Input Contract

### Command Structure
```
python -m src.todo_app.main add [description] [--due-date YYYY-MM-DD] [--recurrence daily|weekly|monthly]
```

### Parameters
- **description** (required): String containing the task description
  - Type: string
  - Constraints: Non-empty, trimmed of leading/trailing whitespace
  - Example: "Submit quarterly report"

- **--due-date** (optional): Date when the task should be completed
  - Type: string in ISO format (YYYY-MM-DD)
  - Constraints: Valid date format, valid calendar date
  - Example: "2024-12-31"

- **--recurrence** (optional): Recurrence pattern for the task
  - Type: string
  - Values: "daily", "weekly", "monthly"
  - Constraints: Must be one of the allowed values
  - Example: "daily"

### Validations
1. Description must not be empty after trimming
2. Due date must be in valid ISO format (YYYY-MM-DD)
3. Due date must be a valid calendar date (e.g., not February 30th)
4. Recurrence must be one of: "daily", "weekly", "monthly"
5. If both due date and recurrence are provided, both must be valid

## Output Contract

### Success Response
- **Return Code**: 0 (success)
- **Console Output**: "Added task #[id]: [description]"
- **State Change**: New Task object added to TaskManager storage
- **Task Properties**:
  - id: Next available integer ID
  - description: Provided description string
  - completed: False
  - priority: "medium" (default)
  - tags: [] (empty list default)
  - due_date: Parsed datetime object or None
  - recurrence: Provided recurrence string or None

### Error Response
- **Return Code**: Non-zero (error)
- **Console Output**: Error message describing the issue
- **State Change**: No new task is added to storage

#### Error Cases
1. **Invalid Date Format**:
   - Condition: --due-date not in YYYY-MM-DD format
   - Output: "Error: Invalid date format: [input]. Use YYYY-MM-DD format."
   - Return Code: 1

2. **Invalid Recurrence Value**:
   - Condition: --recurrence not in ["daily", "weekly", "monthly"]
   - Output: "Error: Recurrence must be one of: daily, weekly, monthly"
   - Return Code: 1

3. **Invalid Date**:
   - Condition: Date is not a valid calendar date (e.g., "2024-02-30")
   - Output: "Error: Invalid date: [input]"
   - Return Code: 1

4. **Empty Description**:
   - Condition: Description is empty or only whitespace
   - Output: "Error: Task description cannot be empty"
   - Return Code: 1

## Behavioral Contract

### Task Creation
1. When valid parameters are provided:
   - A new Task object is created with the provided properties
   - The task is added to the TaskManager's storage
   - The next available ID is assigned sequentially
   - Success message is displayed

2. When due date is provided:
   - Date string is parsed to datetime object
   - Invalid dates result in error (see Error Response)

3. When recurrence is provided:
   - Value is validated against allowed options
   - Invalid values result in error (see Error Response)

4. When both due date and recurrence are provided:
   - Both values are validated independently
   - If either is invalid, an error is returned

### State Management
- The task is added to the in-memory storage
- The next ID counter is incremented
- No persistence beyond application lifetime

## Testing Scenarios

### Happy Path
1. `add "Simple task"` → Success: Task added with no due date or recurrence
2. `add "Task with due date" --due-date "2024-12-31"` → Success: Task added with due date
3. `add "Recurring task" --recurrence daily` → Success: Task added with recurrence
4. `add "Complex task" --due-date "2024-12-31" --recurrence weekly` → Success: Task added with both

### Error Path
1. `add "Task" --due-date "invalid"` → Error: Invalid date format
2. `add "Task" --recurrence yearly` → Error: Invalid recurrence value
3. `add ""` → Error: Empty description
4. `add "Task" --due-date "2024-02-30"` → Error: Invalid date

## Backward Compatibility
- Existing add command functionality remains unchanged
- New optional parameters do not affect existing usage
- Tasks without due dates or recurrence work as before