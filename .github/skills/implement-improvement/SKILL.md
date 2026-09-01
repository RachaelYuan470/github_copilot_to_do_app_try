---
name: implement-improvement
description: Implement a small improvement to the todo-app, test it, debug failures, review the changes, create a focused local commit, and wait for user approval before pushing.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Implement Improvement

Use this skill whenever implementing a small improvement to the todo-app.

The specific improvement must come from the user's current prompt.

Example:

```
Improvement:
Add a command that lists only incomplete tasks.
```

Do not store task-specific requirements permanently in this skill.

## Project requirements

* Follow `.github/copilot-instructions.md`.
* Use the `python-testing` skill when implementing or testing the change.
* Use the `debugging` skill if any test fails.
* Use the `test-and-commit` skill when verifying and committing the completed change.
* Preserve backward compatibility.
* Keep the implementation minimal.
* Follow the existing architecture and coding style.
* Avoid unnecessary dependencies.
* Add or update tests for new behavior.
* Do not modify unrelated functionality.

## Before implementation

1. Read `.github/copilot-instructions.md`.
2. Read the user's requested improvement carefully.
3. Inspect the relevant implementation.
4. Inspect the existing tests.
5. Run `git status`.
6. Record any pre-existing unrelated working-tree changes.
7. Identify the smallest reasonable set of files that need to change.

Do not modify unrelated files.

## Implementation

Use the `python-testing` skill.

Implement the smallest change that satisfies the requested improvement.

While implementing:

* Preserve existing behavior unless explicitly changed by the requirement.
* Reuse existing functions and patterns where appropriate.
* Avoid unnecessary abstractions.
* Maintain compatibility with existing `tasks.json` data.
* Add or update tests covering the requested behavior and important edge cases.

## Testing

After implementation:

1. Run tests directly related to the improvement.
2. If they pass, run the full test suite.
3. If any test fails, use the `debugging` skill.
4. Determine whether the failure was caused by the current implementation.
5. Fix implementation problems instead of weakening valid tests.
6. Re-run the failing tests.
7. Run the full test suite again.

Do not proceed to commit while relevant tests are failing.

## Review before commit

After all tests pass:

1. Run `git status`.
2. Review `git diff`.
3. Confirm the requested improvement is fully implemented.
4. Confirm only intended files were changed.
5. Check for accidental debugging code.
6. Check for secrets, tokens, credentials, or sensitive information.
7. Confirm backward compatibility.
8. Confirm no unrelated working-tree changes will be included.

If unrelated changes exist, leave them unstaged.

## Commit

Use the `test-and-commit` skill.

Stage only files related to the current improvement.

Do not use:

```
git add .
```

when unrelated working-tree changes exist.

Prefer explicitly staging files, for example:

```
git add todo.py test_todo.py
```

Create one focused local commit.

Use a concise descriptive commit message.

Prefer conventional commit style when appropriate:

```
feat: add incomplete task filter

feat: add task search command

fix: handle invalid task identifiers
```

Do not push yet.

## Mandatory user review before push

After creating the local commit, stop before pushing.

Report:

1. What improvement was implemented.
2. Files changed.
3. Tests added or updated.
4. Relevant test results.
5. Full test-suite result.
6. Commit message.
7. Commit hash.
8. Current branch.
9. Any unrelated changes still present in the working tree.

Also show or summarize the committed diff so the user can review the change.

Then explicitly ask the user whether to push.

Do not run `git push` until the user explicitly approves the push after this review.

## Push after approval

Only after the user explicitly approves:

1. Verify the current branch.
2. Verify the intended Git remote.
3. Confirm the local commit still exists.
4. Confirm there are no new problems that would make the push unsafe.
5. Push the current branch.

Prefer:

```
git push
```

If the branch has no upstream and `origin` is clearly the intended remote:

```
git push -u origin <current-branch>
```

Never:

* force-push
* rewrite remote history
* push a different branch without instruction
* push unrelated changes
* push secrets or credentials
* bypass required authentication or approval

## Final report after push

After pushing, report:

1. Commit hash.
2. Branch pushed.
3. Remote used.
4. Whether the push succeeded.
5. Whether anything remains uncommitted.

If the push fails, report the exact reason and do not attempt destructive recovery actions.
