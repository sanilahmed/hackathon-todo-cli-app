# Contract: View Tasks with Intelligent Scheduling

**Feature**: The Evolution of Todo – Phase I Advanced Level: Intelligent Features
**Contract**: View Tasks with Due Date and Recurrence Information
**Date**: 2025-12-31
**Branch**: `001-todo-intelligent-scheduling`

## Overview

This contract defines the behavior for viewing tasks with due dates, recurrence patterns, overdue status, and upcoming indicators in the todo application.

## Input Contract

### Command Structure
```
python -m src.todo_app.main view
```

### Parameters
- **No parameters required**
- **No optional parameters**

## Output Contract

### Success Response
- **Return Code**: 0 (success)
- **Console Output**: Formatted table displaying all tasks with additional scheduling information
- **State Change**: None (read-only operation)

### Output Format
The output displays a table with the following columns:
```
ID | Status | Priority | Tags | Due Date | Recurrence | Description
```

#### Column Details
- **ID**: Task identifier (integer)
- **Status**: "Complete" or "Incomplete"
- **Priority**: "HIGH", "MEDI", "LOW" (truncated to 4 characters)
- **Tags**: Comma-separated list of tags (empty if no tags)
- **Due Date**: Date in YYYY-MM-DD format, or empty if no due date
- **Recurrence**: Recurrence pattern ("DAILY", "WEEKLY", "MONTHLY"), or empty if no recurrence
- **Description**: Task description text

#### Additional Indicators
- **Overdue Indicator**: Tasks with due date < current date show "[OVERDUE]" in the description column
- **Upcoming Indicator**: Tasks with due date within 24 hours show "[DUE SOON]" in the description column

### Example Output
```
ID | Status    | Priority | Tags       | Due Date   | Recurrence | Description
---|-----------|----------|------------|------------|------------|-------------
1  | Incomplete | HIGH     | work,urgent | 2024-12-15 | DAILY      | [OVERDUE] Daily exercise
2  | Incomplete | MEDI     | personal   | 2024-12-02 |            | [DUE SOON] Doctor appointment
3  | Complete  | LOW      |            |            |            | Completed task
```

### Error Response
- **Return Code**: 0 (success, even when no tasks exist)
- **Console Output**: "No tasks in the list" when no tasks exist
- **State Change**: None

## Behavioral Contract

### Task Filtering and Display
1. When no tasks exist:
   - Output "No tasks in the list"
   - Return success code

2. When tasks exist:
   - All tasks are displayed in a formatted table
   - Each task is displayed on a separate row
   - Columns are properly aligned

### Due Date Indicators
1. When a task has a due date:
   - The due date is displayed in YYYY-MM-DD format in the Due Date column
   - If the due date is in the past, "[OVERDUE]" is prepended to the description
   - If the due date is within 24 hours of current time, "[DUE SOON]" is prepended to the description

2. When a task has no due date:
   - The Due Date column is empty
   - No overdue or upcoming indicators are shown

### Recurrence Indicators
1. When a task has a recurrence pattern:
   - The pattern is displayed in the Recurrence column (DAILY, WEEKLY, MONTHLY)
   - The pattern is displayed in uppercase

2. When a task has no recurrence:
   - The Recurrence column is empty

### Priority Display
- Priority values are truncated to 4 characters: "HIGH", "MEDI", "LOW"
- Original priority values are preserved in the Task object

## Testing Scenarios

### Happy Path
1. **No tasks**: `view` → Output: "No tasks in the list"
2. **Tasks without scheduling**: `view` → Output: Table with basic task info
3. **Tasks with due dates**: `view` → Output: Table with due dates and indicators
4. **Tasks with recurrence**: `view` → Output: Table with recurrence patterns
5. **Overdue tasks**: `view` → Output: Table with [OVERDUE] indicators
6. **Upcoming tasks**: `view` → Output: Table with [DUE SOON] indicators

### Edge Cases
1. **Current date matches due date**: Task is not marked as overdue until after the date passes
2. **Empty tags**: Tags column shows empty space instead of comma-separated list
3. **Multiple indicators**: A task can have both due date and recurrence information

## Backward Compatibility
- Existing task display functionality remains unchanged
- New columns (Due Date, Recurrence) are added to the display
- Tasks without new attributes display empty values in those columns
- All existing task information continues to be displayed as before