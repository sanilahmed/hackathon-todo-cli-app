# Todo CLI Application Constitution

## Core Principles

### I. Incremental Development
- Extend existing code, do not rewrite
- Build features in structured phases while preserving stability
- Maintain backward compatibility: existing commands must continue to work

### II. CLI-First UX
- Features must be usable via interactive CLI
- Interactive prompt-based CLI (`todo>`)
- Commands must be intuitive and discoverable
- Helpful error messages for invalid input
- `help` command should list all available actions

### III. Clear Separation of Concerns
- Clear separation between CLI parsing and business logic
- Task model must remain extensible
- Ensure future features can be added without refactoring core logic
- Avoid tight coupling between components

### IV. Code Quality
- No unnecessary dependencies; Python 3.13+ only
- Code readability over cleverness
- Defensive input validation
- Consistent output formatting
- Store task metadata (priority, tags, due dates) in structured form

### V. Spec-Driven Development
- No code may be written without an approved specification
- All features must have their own clear specification before implementation
- All tasks must be uniquely identifiable via an ID
- Task state (complete/incomplete) must be explicitly visible in the task list

## Feature Phases

### Phase I – Basic Level (Core Essentials):
- Add Task: create new todo items
- Delete Task: remove tasks by ID
- Update Task: modify task description
- View Task List: display all tasks clearly
- Mark as Complete: toggle completion status

### Phase II – Intermediate Level (Organization & Usability):
- Priorities: support high / medium / low priority levels
- Tags / Categories: assign labels such as work, personal, home
- Search: find tasks by keyword
- Filter: filter tasks by status, priority, or category
- Sort: order tasks by priority, due date, or alphabetically

### Phase III – Advanced Level (Intelligent Features):
- Recurring Tasks: auto-reschedule repeating tasks (daily / weekly / custom)
- Due Dates: support deadlines with date & time
- Time Reminders: notify user via CLI output at runtime (no external services)

## Technology Standards

### Python Requirements
- Python version: 3.13+
- Environment management: UV only
- Architecture: Proper `/src` folder with modular Python files
- Interface: Command-line only (no GUI, no web)

### Data & Architecture Rules
- Task model must remain extensible
- Avoid tight coupling between CLI parsing and business logic
- Store task metadata (priority, tags, due dates) in structured form
- Ensure future features can be added without refactoring core logic

## Quality Standards

### CLI Design Rules
- Interactive prompt-based CLI (`todo>`)
- Commands must be intuitive and discoverable
- Helpful error messages for invalid input
- `help` command should list all available actions

### Code Quality Requirements
- Clear command naming and predictable behavior
- Defensive input validation
- Consistent output formatting
- Code readability over cleverness

### Documentation Requirements
- Update CLAUDE.md after each phase
- Document new commands, flags, and examples
- Include upgrade notes for developers

## Non-Goals
- No GUI or web interface
- No database or cloud sync
- No external notification services

## Success Criteria
A stable, extensible Todo CLI app that evolves from basic task management into an intelligent, user-friendly command-line productivity tool.

## Governance
This constitution governs all development decisions for the Todo CLI Application. It is the highest authority that governs the behavior of all agents, specs, plans, and implementations. All features, commands, and functionality MUST comply strictly with this constitution to pass evaluation.

**Version**: 3.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31