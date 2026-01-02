# Data Model: In-Memory Python Console Todo App

**Date**: 2025-12-28
**Feature**: 001-todo-app
**Input**: Feature specification and implementation plan

## Overview

This document defines the data structures and relationships for the In-Memory Python Console Todo App. The data model is designed to support all 5 core features (Add, View, Update, Delete, Mark Complete) while maintaining simplicity appropriate for a console-based MVP.

## Core Data Entities

### Task Entity

#### Properties
- **id** (Integer)
  - Type: int
  - Constraints: Unique, Sequential, Positive
  - Generation: Auto-increment starting from 1
  - Purpose: Primary identifier for task operations

- **description** (String)
  - Type: str
  - Constraints: Non-empty, Max length TBD (to be determined by implementation)
  - Purpose: Human-readable description of the task

- **completed** (Boolean)
  - Type: bool
  - Default: False
  - Purpose: Track completion status of the task

#### Example Representation
```python
{
    "id": 1,
    "description": "Buy groceries",
    "completed": False
}
```

### Task Collection

#### In-Memory Storage
- **Structure**: List of Task objects
- **Access Pattern**: Sequential lookup by ID
- **Operations**: Add, Remove, Update, Find by ID
- **Size Limitations**: Limited by available system memory

## State Transitions

### Task Lifecycle
```
[Created] --(add)--> [Active] --(complete)--> [Completed]
                      |                    |
                      |(update)            |(update)
                      v                    v
                 [Updated]            [Updated Completed]
                      |                    |
                      |(delete)            |(delete)
                      v                    v
                 [Removed] <-------------- [Removed]
```

### State Transition Rules
1. **New Task**: Created with `completed = False`
2. **Complete Task**: `completed` changes from `False` to `True`
3. **Incomplete Task**: `completed` changes from `True` to `False`
4. **Update Task**: Description can be modified regardless of completion status
5. **Delete Task**: Task is removed from collection, ID becomes invalid

## Data Validation Rules

### Input Validation
- Task descriptions must not be empty or contain only whitespace
- Task IDs must exist in the current collection for update/delete operations
- Task IDs must be positive integers

### Business Rules
- Task IDs are unique within a session
- Task IDs are never reused within a session (even after deletion)
- Task descriptions should be meaningful (not just special characters)

## Data Access Patterns

### Query Operations
- **Get All Tasks**: Return entire collection
- **Get Task by ID**: Return single task matching ID
- **Get Completed Tasks**: Filter collection by completion status
- **Get Active Tasks**: Filter collection by completion status

### Modification Operations
- **Add Task**: Append to collection, assign next available ID
- **Update Task**: Find by ID, modify description
- **Mark Complete**: Find by ID, set completion status to True
- **Mark Incomplete**: Find by ID, set completion status to False
- **Delete Task**: Find by ID, remove from collection

## Performance Characteristics

### Time Complexity
- **Add Task**: O(1) - append to list
- **Get All Tasks**: O(1) - return reference to list
- **Get Task by ID**: O(n) - linear search through list
- **Update Task**: O(n) - find by ID then update
- **Delete Task**: O(n) - find by ID then remove
- **Mark Complete/Incomplete**: O(n) - find by ID then update

### Space Complexity
- O(n) where n is the number of tasks in memory
- Memory usage approximately: n * (id_size + description_size + completed_size)

## Data Integrity Considerations

### In-Memory Constraints
- No persistence between sessions
- Data loss on application exit
- No concurrent access issues (single-user application)
- No transaction requirements

### Error Handling
- Invalid ID operations return appropriate error messages
- Empty collection operations handled gracefully
- Duplicate ID prevention through sequential generation