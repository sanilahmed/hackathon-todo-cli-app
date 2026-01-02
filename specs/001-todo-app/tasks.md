# Tasks: In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/todo_app/
- [X] T002 [P] Create __init__.py files for package structure in src/todo_app/, src/todo_app/core/, src/todo_app/cli/
- [X] T003 [P] Set up basic project configuration (pyproject.toml or setup.py)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create Task data model in src/todo_app/core/task.py
- [X] T005 Create TaskManager class for in-memory storage in src/todo_app/core/task_manager.py
- [X] T006 [P] Create CLI argument parsing in src/todo_app/cli/interface.py
- [X] T007 [P] Create output formatting in src/todo_app/cli/formatter.py
- [X] T008 Create main application entry point in src/todo_app/main.py
- [X] T009 [P] Implement basic error handling infrastructure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks to their todo list with unique IDs

**Independent Test**: User can run the application, enter a new task via command line, and verify the task appears in the list of tasks.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for add command in tests/contract/test_add_command.py
- [ ] T011 [P] [US1] Integration test for adding task user journey in tests/integration/test_add_task.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Implement Task class with properties and methods in src/todo_app/core/task.py
- [X] T013 [US1] Implement TaskManager.add_task() method in src/todo_app/core/task_manager.py
- [X] T014 [US1] Implement add command in src/todo_app/cli/interface.py
- [X] T015 [US1] Add validation for empty task descriptions
- [X] T016 [US1] Implement sequential ID generation starting from 1

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to see all tasks currently in their todo list with their completion status

**Independent Test**: User can run the application and view all tasks with their completion status and IDs.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T017 [P] [US2] Contract test for view command in tests/contract/test_view_command.py
- [ ] T018 [P] [US2] Integration test for viewing tasks user journey in tests/integration/test_view_tasks.py

### Implementation for User Story 2

- [X] T019 [P] [US2] Implement TaskManager.get_all_tasks() method in src/todo_app/core/task_manager.py
- [X] T020 [US2] Implement view command in src/todo_app/cli/interface.py
- [X] T021 [US2] Implement formatted output display in src/todo_app/cli/formatter.py
- [X] T022 [US2] Handle empty task list case with appropriate message

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Enable users to mark tasks as complete or incomplete to track their progress

**Independent Test**: User can mark a task as complete and verify the status change is reflected when viewing tasks.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Contract test for complete command in tests/contract/test_complete_command.py
- [ ] T024 [P] [US3] Contract test for incomplete command in tests/contract/test_incomplete_command.py

### Implementation for User Story 3

- [X] T025 [P] [US3] Implement TaskManager.mark_complete() method in src/todo_app/core/task_manager.py
- [X] T026 [P] [US3] Implement TaskManager.mark_incomplete() method in src/todo_app/core/task_manager.py
- [X] T027 [US3] Implement complete command in src/todo_app/cli/interface.py
- [X] T028 [US3] Implement incomplete command in src/todo_app/cli/interface.py
- [X] T029 [US3] Add validation to check if task ID exists before marking complete/incomplete

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task Description (Priority: P3)

**Goal**: Enable users to modify the description of an existing task

**Independent Test**: User can update a task description and verify the change is reflected when viewing tasks.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US4] Contract test for update command in tests/contract/test_update_command.py
- [ ] T031 [P] [US4] Integration test for updating task user journey in tests/integration/test_update_task.py

### Implementation for User Story 4

- [X] T032 [P] [US4] Implement Task.update_description() method in src/todo_app/core/task.py
- [X] T033 [US4] Implement TaskManager.update_task() method in src/todo_app/core/task_manager.py
- [X] T034 [US4] Implement update command in src/todo_app/cli/interface.py
- [X] T035 [US4] Add validation for empty new task descriptions

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Enable users to remove completed or unwanted tasks from their todo list

**Independent Test**: User can delete a task and verify it no longer appears in the task list.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T036 [P] [US5] Contract test for delete command in tests/contract/test_delete_command.py
- [ ] T037 [P] [US5] Integration test for deleting task user journey in tests/integration/test_delete_task.py

### Implementation for User Story 5

- [X] T038 [P] [US5] Implement TaskManager.delete_task() method in src/todo_app/core/task_manager.py
- [X] T039 [US5] Implement delete command in src/todo_app/cli/interface.py
- [X] T040 [US5] Add validation to check if task ID exists before deletion

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T041 [P] Documentation updates in README.md
- [X] T042 [P] Unit tests for core functionality in tests/unit/
- [X] T043 Error handling for edge cases (invalid IDs, empty descriptions, etc.)
- [X] T044 [P] Input validation across all commands
- [X] T045 Run quickstart.md validation to ensure all commands work as specified

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories