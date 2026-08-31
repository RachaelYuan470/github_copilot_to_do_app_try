# Todo App — Copilot Instructions

## Project Overview

This repository contains a small Python command-line todo application.

The application allows users to create, list, complete, and delete tasks and persists task data in JSON.

Keep the project simple, readable, and appropriate for a small Python application.

## Current Project Structure

The main project files are:

- `todo.py` — application logic and command-line interface
- `test_todo.py` — automated tests
- `tasks.json` — persisted task data

Copilot skills are stored under:

- `.github/skills/`

Do not introduce additional architectural layers unless a task clearly requires them.

## Task Model

A task currently contains:

- `id`
- `title`
- `done`
- `priority`

Example:

    {
      "id": 1,
      "title": "Review plan",
      "done": false,
      "priority": "High"
    }

Valid priority values are:

- `Low`
- `Medium`
- `High`

## Task Title Rules

Task titles must:

- Be strings.
- Have leading and trailing whitespace removed.
- Not be empty.
- Not consist only of whitespace.

Invalid task titles must not create a task.

## Priority Rules

New tasks may have one of these priorities:

- `Low`
- `Medium`
- `High`

Do not introduce additional priority values unless explicitly requested.

When loading persisted tasks:

- Missing priority values must default to `Medium`.
- Invalid priority values must default to `Medium`.
- Null priority values must default to `Medium`.
- Valid priority values must remain unchanged.

When saving tasks, only valid priority values should be persisted.

Maintain backward compatibility with older task data that does not contain a priority field.

## Persistence

Tasks are persisted in `tasks.json`.

When modifying persistence behavior:

- Preserve existing task data whenever possible.
- Maintain backward compatibility.
- Do not silently discard task information.
- Keep the JSON structure simple.
- Avoid changing the file format unless explicitly required.

Do not manually modify `tasks.json` merely to make automated tests pass.

## Implementation Guidelines

When implementing a feature:

1. Understand the existing implementation first.
2. Inspect related tests.
3. Identify the smallest reasonable change.
4. Follow existing coding patterns.
5. Keep functions focused and understandable.
6. Avoid unnecessary abstractions.
7. Avoid unnecessary dependencies.
8. Preserve existing behavior unless the requirement explicitly changes it.
9. Add or update tests for new behavior.
10. Run the relevant tests after implementation.

Prefer modifying existing functions over introducing new architectural layers when the existing design can support the requirement cleanly.

## Testing

The project uses Python tests.

For every behavioral change:

- Inspect existing tests first.
- Add tests for new behavior.
- Include important edge cases.
- Run relevant tests.
- Run the full test suite before declaring the task complete when practical.

Do not:

- Delete a valid test simply because it fails.
- Weaken assertions to make an incorrect implementation pass.
- Modify unrelated tests.
- hard-code behavior solely to satisfy a specific test case.

When a test fails, determine the root cause before changing code.

## Debugging

When debugging:

1. Read the complete error.
2. Identify the failing behavior.
3. Reproduce the problem when possible.
4. Inspect relevant code and tests.
5. Determine the root cause.
6. Make the smallest safe fix.
7. Re-run the failing test.
8. Run related tests.
9. Run the full test suite when practical.

Avoid unrelated refactoring while fixing a bug.

## Scope Control

Keep each task focused.

Do not:

- Modify unrelated functionality.
- Perform large refactors unless requested.
- Add third-party dependencies without a clear need.
- Rename files unnecessarily.
- Change public behavior unrelated to the task.
- Reformat the entire project for a small change.

If a requested task appears to require a significant architectural change, explain why before making the change.

## Code Review

Before considering implementation complete, review the changes for:

- Correctness
- Edge cases
- Backward compatibility
- Unnecessary complexity
- Missing tests
- Accidental unrelated changes
- Debugging code left behind
- Sensitive information or secrets

Prefer simple solutions over clever solutions.

## Git

Before creating a commit:

1. Run the relevant tests.
2. Review `git status`.
3. Review the Git diff.
4. Ensure only files related to the current task are staged.
5. Ensure no secrets or credentials are included.

Do not automatically stage unrelated files.

Avoid `git add .` when unrelated working-tree changes exist.

Prefer explicitly staging files related to the task.

Use concise, descriptive commit messages.

Examples:

    feat: add task priority support

    feat: add task completion support

    fix: normalize invalid task priorities

    fix: reject empty task titles

Do not push commits to GitHub unless the user explicitly requests a push.

A local Git commit and a GitHub push are separate operations.

## Copilot Skills

Reusable workflows are stored under `.github/skills/`.

Use the appropriate skill when relevant:

- `python-testing` — implementing or modifying Python behavior and tests
- `debugging` — diagnosing bugs and failing tests
- `test-and-commit` — verifying completed work and creating a local commit

Skills supplement these repository instructions.

These repository instructions apply throughout the project.

## General Principle

Make the smallest correct change that satisfies the requirement.

Prioritize:

1. Correctness
2. Data integrity
3. Backward compatibility
4. Tests
5. Readability
6. Simplicity

Do not over-engineer this application.