# Research Notes: The Evolution of Todo – Phase II (Intermediate Level)

**Created**: 2025-12-31
**Feature**: /specs/todo-app-intermediate/spec.md

## Research Summary

This document captures the research and technical investigation for implementing Phase II features (priorities, tags, search, filter, sort) in the Todo CLI application. The research focuses on extending the existing architecture while maintaining backward compatibility.

## Technical Investigation

### Task Model Extension Research

**Priority Implementation Options**:
- **Option 1**: Simple string enum (high/medium/low)
  - Pros: Simple implementation, easy to understand
  - Cons: No type safety, potential for typos
  - Selected: Yes - aligns with Python simplicity

- **Option 2**: Python Enum class
  - Pros: Type safety, prevents invalid values
  - Cons: Slightly more complex, may be overkill for this use case
  - Selected: No - string validation is sufficient

**Tags Implementation Options**:
- **Option 1**: List of strings
  - Pros: Flexible, allows multiple tags per task
  - Cons: Need validation for tag format
  - Selected: Yes - most flexible approach

- **Option 2**: Single string with delimiter
  - Pros: Simple storage
  - Cons: Less flexible for complex tag operations
  - Selected: No - list approach is better

**Due Date Implementation Options**:
- **Option 1**: datetime object
  - Pros: Proper date operations, timezone support if needed
  - Cons: More complex parsing from CLI
  - Selected: Yes - proper date handling is important

- **Option 2**: String with format validation
  - Pros: Simple storage and parsing
  - Cons: No date operations, potential for invalid dates
  - Selected: No - datetime is better for functionality

### Core Logic Research

**Search Algorithm Options**:
- **Simple substring matching**: Fast, case-insensitive search in task descriptions
- **Regex matching**: More complex patterns but potentially overkill
- **Selected approach**: Simple substring matching with case-insensitive comparison

**Filter Implementation Research**:
- **Method chaining**: task_manager.filter_by_status().filter_by_priority()
  - Pros: Readable, extensible
  - Cons: Multiple iterations over data
- **Single filter method with criteria**: task_manager.filter(criteria)
  - Pros: Single iteration, efficient
  - Cons: Less readable for complex chains
- **Selected approach**: Single filter method with criteria dictionary

**Sort Implementation Research**:
- **Built-in sorted() function**: Leverages Python's optimized sorting
- **Custom comparison functions**: More control but potentially slower
- **Selected approach**: Built-in sorted() with key functions for efficiency

### Performance Considerations

**Memory Usage**:
- Adding priority, tags, and due_date to existing tasks will increase memory per task by ~50-100 bytes
- For 1000 tasks: Additional ~50-100KB memory usage (acceptable)

**Time Complexity**:
- Search: O(n) where n is number of tasks
- Filter: O(n) where n is number of tasks
- Sort: O(n log n) where n is number of tasks
- These are acceptable for CLI application with up to 1000 tasks

## Architecture Patterns

### Separation of Concerns Validation

**Current Architecture Review**:
- Core logic in src/todo_app/core/ (task.py, task_manager.py)
- CLI interface in src/todo_app/cli/ (interface.py, formatter.py)
- This separation is maintained in Phase II implementation

**New Component Integration**:
- Validators in new src/todo_app/cli/validators.py
- Enhanced task model in src/todo_app/core/task.py
- Extended task manager in src/todo_app/core/task_manager.py

## Implementation Risks

### Risk 1: Backward Compatibility
- **Issue**: Existing tasks without priority/tags/due_date need to work
- **Mitigation**: Default values and null-safe operations
- **Status**: Resolved - default priority is medium, tags is empty list, due_date is None

### Risk 2: CLI Command Complexity
- **Issue**: Adding many new commands and flags might make CLI confusing
- **Mitigation**: Clear help system and intuitive command structure
- **Status**: Addressed - commands follow consistent patterns

### Risk 3: Performance Degradation
- **Issue**: New operations might slow down the application
- **Mitigation**: Efficient algorithms and testing with large task sets
- **Status**: Addressed - algorithms are optimized for expected usage

## Technology Decisions

### Python Standard Library Components
- **datetime**: For date parsing and validation
- **re**: For input validation patterns if needed
- **typing**: For type hints in enhanced models
- **dataclasses**: For clean Task model definition

### Validation Approach
- **Input validation**: Performed in CLI layer before passing to core
- **Data validation**: Performed in core layer to ensure consistency
- **User feedback**: Clear error messages without stack traces

## Research Conclusions

The research confirms that Phase II features can be implemented while maintaining:
1. Backward compatibility with existing tasks
2. Performance requirements (sub-second operations)
3. Clean separation of concerns
4. Code readability and extensibility
5. CLI-first user experience

The selected approaches balance functionality with simplicity, aligning with the project's core principles.