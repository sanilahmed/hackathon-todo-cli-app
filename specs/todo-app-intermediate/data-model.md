# Data Model: The Evolution of Todo – Phase II (Intermediate Level)

**Created**: 2025-12-31
**Feature**: /specs/todo-app-intermediate/spec.md

## Overview

This document defines the enhanced data model for Phase II of the Todo application, extending the existing Task model to include priority, tags, and due date functionality while maintaining backward compatibility.

## Enhanced Task Model

### Class Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                           Task                              │
├─────────────────────────────────────────────────────────────┤
│ - id: int                                                   │
│ - description: str                                          │
│ - completed: bool                                           │
│ - priority: str (high/medium/low)                          │
│ - tags: List[str]                                           │
│ - due_date: Optional[datetime]                              │
├─────────────────────────────────────────────────────────────┤
│ + __init__(id: int, description: str, completed: bool,      │
│            priority: str, tags: List[str],                  │
│            due_date: Optional[datetime])                    │
│ + __post_init__()                                           │
└─────────────────────────────────────────────────────────────┘
```

### Entity Definition

**Task Entity**
- **Purpose**: Represents a single todo item with enhanced organizational features
- **Lifespan**: Exists in memory during application runtime
- **Identity**: Unique integer ID assigned at creation

### Attributes

| Attribute | Type | Default | Constraints | Description |
|-----------|------|---------|-------------|-------------|
| id | int | - | Positive integer, unique | Unique identifier for the task |
| description | str | - | Non-empty string | Human-readable task description |
| completed | bool | False | Boolean value | Completion status of the task |
| priority | str | "medium" | One of ["high", "medium", "low"] | Priority level for organization |
| tags | List[str] | [] | List of non-empty strings | Category tags for classification |
| due_date | Optional[datetime] | None | Valid datetime or None | Optional deadline for the task |

### Attribute Details

#### Priority Attribute
- **Values**: "high", "medium", "low"
- **Default**: "medium"
- **Purpose**: Provides a way to prioritize tasks
- **Sorting Order**: High → Medium → Low
- **Validation**: Must be one of the three allowed values

#### Tags Attribute
- **Type**: List of strings
- **Default**: Empty list []
- **Purpose**: Provides categorical organization for tasks
- **Format**: Each tag is a non-empty string without commas
- **Usage**: Multiple tags per task, comma-separated in CLI input
- **Example**: ["work", "urgent", "meeting"]

#### Due Date Attribute
- **Type**: Optional datetime
- **Default**: None
- **Purpose**: Provides deadline information for tasks
- **Format**: ISO datetime format (YYYY-MM-DD or full ISO 8601)
- **Usage**: Optional deadline for task completion
- **Example**: 2025-01-15T09:00:00

## Relationship Model

### Task Relationships

Since this is an in-memory, single-user application, the Task entity exists in isolation with no foreign key relationships. However, there are logical groupings:

```
Task (1) ───► Priority (1)     // Each task has one priority value
Task (1) ───► Tags (0..n)      // Each task can have zero or more tags
Task (1) ───► Due Date (0..1)  // Each task can have zero or one due date
```

## Data Flow

### Creation Flow
```
CLI Input → Validation → Task Creation → Storage in TaskManager
```

### Retrieval Flow
```
CLI Command → TaskManager → Filter/Sort/Search → Task Objects → CLI Output
```

## Backward Compatibility

### Existing Task Handling

For tasks created in Phase I (without Phase II attributes), the data model handles them as follows:

1. **Priority**: Default to "medium" when accessed
2. **Tags**: Default to empty list [] when accessed
3. **Due Date**: Default to None when accessed

### Migration Strategy

No migration required since the application uses in-memory storage. When existing tasks are loaded or accessed, they will automatically have the default values for new attributes.

## Validation Rules

### Business Rules

1. **Priority Validation**:
   - Value must be one of: "high", "medium", "low"
   - Case-sensitive comparison
   - Invalid values raise ValueError

2. **Tags Validation**:
   - Each tag must be a non-empty string
   - Tags cannot contain commas (used as delimiter)
   - Empty tags are removed from the list

3. **Due Date Validation**:
   - If provided, must be a valid datetime object
   - Invalid date formats raise ValueError
   - ISO format preferred (YYYY-MM-DD)

4. **Description Validation**:
   - Cannot be empty or contain only whitespace
   - Maximum length: 1000 characters

### Validation Implementation

```python
# Example validation implementation
def validate_priority(priority: str) -> str:
    if priority not in ["high", "medium", "low"]:
        raise ValueError(f"Priority must be one of: high, medium, low, got: {priority}")
    return priority

def validate_tags(tags: List[str]) -> List[str]:
    validated_tags = []
    for tag in tags:
        if tag.strip():  # Non-empty after stripping whitespace
            if ',' in tag:
                raise ValueError(f"Tag cannot contain commas: {tag}")
            validated_tags.append(tag.strip())
    return validated_tags
```

## Serialization Format

### Internal Representation
```python
# Task object in memory
Task(
    id=1,
    description="Complete project proposal",
    completed=False,
    priority="high",
    tags=["work", "important"],
    due_date=datetime(2025, 1, 15, 9, 0, 0)
)
```

### CLI Display Format
```
ID: 1 | [HIGH] Complete project proposal | Tags: work,important | Due: 2025-01-15 | Status: Incomplete
```

### Storage Format (Conceptual - In-memory only)
```
tasks = [
    {
        "id": 1,
        "description": "Complete project proposal",
        "completed": False,
        "priority": "high",
        "tags": ["work", "important"],
        "due_date": "2025-01-15T09:00:00"
    },
    # ... more tasks
]
```

## Performance Considerations

### Memory Usage
- Adding priority (string), tags (list), and due_date (datetime) to each task
- Additional memory per task: ~50-100 bytes
- For 1000 tasks: Additional ~50-100KB memory usage

### Access Patterns
- Primary access: By ID (O(1) with proper indexing)
- Search access: By keyword in description (O(n))
- Filter access: By attributes (O(n))
- Sort access: By attributes (O(n log n))

## Extension Points

### Future Enhancements
The data model is designed to support future extensions:

1. **Additional Attributes**: Easy to add new optional attributes
2. **Nested Objects**: Priority could become an object with additional properties
3. **Complex Tags**: Tags could evolve to include color, category, etc.
4. **Recurring Tasks**: Due date could expand to support recurrence patterns

## Data Integrity

### Consistency Rules
1. Task ID must remain constant throughout the task's lifetime
2. Priority values must remain consistent with the allowed values
3. Tags list should not contain duplicate values
4. Due date should remain unchanged unless explicitly modified

### Error Handling
- Invalid data during creation raises appropriate exceptions
- Invalid data during modification raises appropriate exceptions
- All errors provide meaningful messages to the user