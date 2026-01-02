# Research Notes: The Evolution of Todo – Phase I Advanced Level: Intelligent Features

**Feature**: The Evolution of Todo – Phase I Advanced Level: Intelligent Features
**Date**: 2025-12-31
**Branch**: `001-todo-intelligent-scheduling`

## Technical Research

### Date Handling in Python
- Using `datetime` module for all date operations
- `datetime.fromisoformat()` for parsing ISO date strings (YYYY-MM-DD)
- `date.replace()` for handling month-end dates when rescheduling (e.g., Jan 31 → Feb 28/29)
- Timezone handling: Using system local time only, no timezone conversion

### Recurrence Calculation Strategies
- **Daily**: Add 1 day to current date
- **Weekly**: Add 7 days to current date (maintains same day of week)
- **Monthly**: Add 1 month to current date with special handling for month-end dates
  - For month-end dates (28th, 29th, 30th, 31st), use the last day of the target month if the day doesn't exist
  - Example: January 31st → February 28th/29th → March 31st → April 30th, etc.

### Overdue Detection
- Compare task's due date with current date
- Tasks with due date < current date are overdue
- Use `datetime.date()` comparison for day-level precision

### Upcoming Task Detection
- Tasks with due date within 24 hours of current time are "upcoming"
- Use `datetime.timedelta(hours=24)` for time window calculation

## Implementation Considerations

### Memory Management
- Recurring tasks create new task instances when completed
- No automatic cleanup of old recurring tasks to maintain user history
- Memory usage grows with task completion but should remain manageable for typical usage

### Validation Strategies
- Due dates: Validate ISO format and ensure date is not in the past (optional)
- Recurrence: Validate against allowed values (daily, weekly, monthly)
- Error messages: Provide clear, user-friendly feedback for invalid inputs

## Architecture Decisions

### Data Model Changes
- Extend Task model with optional `due_date` and `recurrence` fields
- Maintain backward compatibility with existing tasks that lack these fields
- Use `Optional[datetime]` for due_date to allow non-dated tasks

### CLI Command Design
- Add `--due-date` and `--recurrence` flags to `add` command
- Maintain existing command structure while adding new functionality
- Provide clear help text for new options

## Risk Assessment

### Month-End Date Handling
- Critical: Need to handle month-end dates properly when rescheduling
- Solution: Use calendar-aware date arithmetic to handle February 29th, 30th, 31st scenarios
- Testing: Include test cases for all month-end scenarios

### Performance Considerations
- Large numbers of recurring tasks could impact performance
- Solution: Keep in-memory storage efficient with simple data structures
- Monitoring: No background processes needed for this implementation