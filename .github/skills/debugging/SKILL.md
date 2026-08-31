---
name: debugging
description: Diagnose and fix bugs or failing tests in the todo-app. Use this skill when tests fail, unexpected behavior occurs, or an implementation does not work as expected.
---

# Debugging

Use this skill when debugging the todo-app.

## Goals

- Find the root cause rather than treating symptoms.
- Make the smallest safe fix.
- Preserve existing behavior.
- Verify the fix with tests.
- Avoid unrelated refactoring.

## Debugging process

When a test fails or unexpected behavior occurs:

1. Read the complete error message.
2. Identify the failing test, function, or operation.
3. Inspect the relevant source code.
4. Inspect related tests.
5. Reproduce the problem when possible.
6. Determine the root cause.
7. Explain the cause before making a significant change.
8. Make the smallest reasonable fix.
9. Run the failing test again.
10. Run the full relevant test suite.

## When debugging tests

Do not automatically change a test because it fails.

First determine:

- Is the implementation incorrect?
- Is the test incorrect?
- Has the expected behavior intentionally changed?
- Is the failure caused by test setup or environment configuration?

If the implementation is wrong, fix the implementation.

If the test expectation is genuinely outdated or incorrect, explain why before changing the test.

## Data handling

The todo-app uses task data stored in JSON.

When debugging task data:

- Preserve existing fields.
- Avoid deleting user data.
- Handle missing or unexpected fields safely.
- Do not silently discard task information.
- Maintain compatibility with existing `tasks.json` data unless the task explicitly requires a format change.

## Scope control

Do not:

- Rewrite unrelated code.
- Introduce unnecessary dependencies.
- Perform large refactors to fix a small bug.
- Change project architecture without a clear reason.
- Modify unrelated tests.

## Verification

After fixing a bug:

1. Re-run the test that exposed the problem.
2. Run related tests.
3. Run the full test suite.
4. Review the final diff.
5. Confirm that the fix addresses the root cause.

## Completion criteria

A debugging task is complete only when:

- The root cause has been identified.
- The bug has been fixed.
- The relevant tests pass.
- Existing functionality continues to work.
- No unrelated changes were introduced.