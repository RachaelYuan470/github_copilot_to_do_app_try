---
name: python-testing
description: Test Python changes in the todo-app. Use this skill whenever implementing, modifying, or reviewing Python functionality, especially when adding or changing task behavior.
---

# Python Testing

Use this skill when working on Python functionality in the todo-app.

## Goals

- Preserve existing behavior unless the task explicitly requires a change.
- Follow the existing project structure and coding style.
- Keep implementations simple and easy to understand.
- Add tests for new functionality.
- Avoid unnecessary dependencies.

## Before changing code

1. Inspect the relevant Python source files.
2. Inspect the existing tests.
3. Understand how the current functionality works.
4. Identify the smallest reasonable set of files that need to change.
5. Do not modify unrelated files.

## When implementing a feature

1. Make the smallest implementation that satisfies the requirement.
2. Reuse existing functions and patterns where appropriate.
3. Avoid unnecessary abstractions, classes, or dependencies.
4. Preserve compatibility with existing task data.
5. Add or update tests that verify the new behavior.

## Testing requirements

After implementing a change:

1. Run the relevant tests.
2. If relevant tests pass, run the full test suite.
3. If tests fail, determine whether the failure is caused by the implementation.
4. Fix implementation problems rather than weakening or deleting tests.
5. Run the tests again after making fixes.

## Test quality

Tests should:

- Verify the expected behavior.
- Cover important edge cases.
- Be independent and repeatable.
- Follow the testing style already used by the project.
- Avoid testing implementation details when behavior can be tested instead.

## Completion criteria

Do not declare the task complete until:

- The requested behavior is implemented.
- Existing functionality still works.
- Relevant tests pass.
- The full test suite passes when practical.
- No unrelated files were modified.