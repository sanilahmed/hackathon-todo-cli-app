# CLI Interface Contract: In-Memory Python Console Todo App

**Date**: 2025-12-28
**Feature**: 001-todo-app
**Version**: 1.0

## Overview

This document defines the contract for the command-line interface of the In-Memory Python Console Todo App. It specifies the expected commands, arguments, input/output formats, and error handling behavior.

## Command Format

The application follows the format:
```
python -m src.todo_app [command] [arguments]
```

## Command Specifications

### 1. Add Command
**Command**: `add`
**Arguments**: `"task description"`
**Synopsis**: Add a new task to the todo list

**Request**:
- **Input**: Task description as a string argument (in quotes if containing spaces)
- **Format**: `python -m src.todo_app add "task description"`
- **Validation**: Description must not be empty or contain only whitespace

**Response**:
- **Success**: `Added task #[ID]: [description]`
- **Example**: `Added task #1: Buy groceries`
- **Error**: `Error: Task description cannot be empty`

### 2. View Command
**Command**: `view`
**Arguments**: None
**Synopsis**: Display all tasks with their status and IDs

**Request**:
- **Input**: No arguments required
- **Format**: `python -m src.todo_app view`

**Response**:
- **Success**: Formatted table showing ID, status, and description
- **Format**:
```
ID | Status    | Description
---|-----------|------------------
1  | Incomplete| Buy groceries
2  | Complete  | Finish report
```
- **Empty List**: `No tasks in the list`

### 3. Complete Command
**Command**: `complete`
**Arguments**: `task_id`
**Synopsis**: Mark a task as complete

**Request**:
- **Input**: Task ID as integer argument
- **Format**: `python -m src.todo_app complete [task_id]`
- **Validation**: Task ID must exist in the current task list

**Response**:
- **Success**: `Task #[ID] marked as complete`
- **Example**: `Task #1 marked as complete`
- **Error**: `Error: Task with ID [ID] does not exist`

### 4. Incomplete Command
**Command**: `incomplete`
**Arguments**: `task_id`
**Synopsis**: Mark a task as incomplete

**Request**:
- **Input**: Task ID as integer argument
- **Format**: `python -m src.todo_app incomplete [task_id]`
- **Validation**: Task ID must exist in the current task list

**Response**:
- **Success**: `Task #[ID] marked as incomplete`
- **Example**: `Task #2 marked as incomplete`
- **Error**: `Error: Task with ID [ID] does not exist`

### 5. Update Command
**Command**: `update`
**Arguments**: `task_id "new description"`
**Synopsis**: Update the description of an existing task

**Request**:
- **Input**: Task ID as integer, new description as string (in quotes if containing spaces)
- **Format**: `python -m src.todo_app update [task_id] "new description"`
- **Validation**: Task ID must exist, new description must not be empty

**Response**:
- **Success**: `Task #[ID] updated to: [new description]`
- **Example**: `Task #1 updated to: Buy groceries and cook dinner`
- **Error**: `Error: Task with ID [ID] does not exist` or `Error: Task description cannot be empty`

### 6. Delete Command
**Command**: `delete`
**Arguments**: `task_id`
**Synopsis**: Remove a task from the todo list

**Request**:
- **Input**: Task ID as integer argument
- **Format**: `python -m src.todo_app delete [task_id]`
- **Validation**: Task ID must exist in the current task list

**Response**:
- **Success**: `Task #[ID] deleted`
- **Example**: `Task #1 deleted`
- **Error**: `Error: Task with ID [ID] does not exist`

## Error Handling Contract

### Standard Error Format
```
Error: [descriptive message]
```

### Error Types
1. **Invalid Task ID**: Task ID does not exist in current session
2. **Empty Description**: Provided description is empty or only whitespace
3. **Invalid Arguments**: Missing required arguments or incorrect format
4. **Unknown Command**: Command not recognized by the application

## Exit Codes

- **0**: Success - Command executed successfully
- **1**: Error - Command failed due to validation or runtime error
- **2**: Usage Error - Incorrect command usage

## Examples

### Valid Usage Examples
```bash
python -m src.todo_app add "Buy groceries"
python -m src.todo_app view
python -m src.todo_app complete 1
python -m src.todo_app update 2 "Updated task description"
python -m src.todo_app delete 1
```

### Invalid Usage Examples
```bash
python -m src.todo_app add ""                    # Error: Empty description
python -m src.todo_app complete 999             # Error: Task doesn't exist
python -m src.todo_app invalid-command          # Error: Unknown command
```

## Versioning

This contract follows semantic versioning:
- **Major**: Breaking changes to command interface or behavior
- **Minor**: Non-breaking additions to functionality
- **Patch**: Corrections or clarifications to existing behavior

## Compliance Testing

Any implementation of this todo app must pass the following contract validation:
1. All commands return the specified success or error formats
2. All validation rules are enforced as specified
3. Exit codes match the defined contract
4. Output formats match the specified formats exactly