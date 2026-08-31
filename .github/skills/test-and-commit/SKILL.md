---
name: test-and-commit
description: Verify completed changes and create a Git commit for the todo-app. Use this skill when a coding task has been implemented and the user asks to commit the changes or asks to finish the task with a commit.
---

# Test and Commit

Use this skill when implementation work is complete and the changes are ready to be committed.

## Important Git rule

Do not push to GitHub automatically.

This skill may create a local Git commit when explicitly requested by the user.

Pushing to a remote repository requires a separate explicit user request.

## Before committing

1. Check the current Git status.
2. Review the changes made for the current task.
3. Review the Git diff.
4. Identify unrelated changes.
5. Run the relevant tests.
6. Run the full test suite when practical.

## Test requirements

Do not commit if:

- Relevant tests are failing.
- The implementation is clearly incomplete.
- There is an unresolved error caused by the current changes.

If tests fail:

1. Determine the cause.
2. Fix the implementation when appropriate.
3. Run the tests again.
4. Only proceed when the relevant tests pass.

Do not modify tests merely to make a failing implementation pass.

## Review requirements

Before committing, verify:

- The requested feature or bug fix is implemented.
- Existing functionality still works.
- No unrelated files are included.
- No debugging code was accidentally left behind.
- No passwords, API keys, tokens, or other secrets are being committed.
- No unnecessary dependencies or generated files were added.

## Commit scope

Only stage files that belong to the current task.

Do not use a blanket command such as:

    git add .

when unrelated changes may exist in the working tree.

Prefer explicitly staging the relevant files.

## Commit message

Create a concise, descriptive commit message.

Prefer conventional commit style when appropriate:

- `feat:` for a new feature
- `fix:` for a bug fix
- `test:` for test-only changes
- `refactor:` for refactoring
- `docs:` for documentation changes
- `chore:` for maintenance

Examples:

    feat: add task completion support

    feat: add task priority support

    fix: handle missing task fields

## Commit

Only create the commit if:

- The user explicitly requested a commit, or
- The user's instruction clearly asks for the completed work to be committed.

Before committing, ensure the staged changes contain only the intended task.

Create one focused commit for the task unless the user explicitly requests otherwise.

## After committing

Run:

    git status

Confirm that the commit was created successfully.

Do not push unless the user explicitly asks for a push.

## Completion report

After committing, report:

1. What was changed.
2. Which tests were run.
3. Whether the tests passed.
4. The commit message.
5. Whether anything remains uncommitted.
6. Whether the changes were pushed.

Make clear that a local commit is not the same as a GitHub push.