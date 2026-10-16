---
description: Fix a bug — reproduce with a failing test first, then fix
argument-hint: <repo?> <error/log line> — <failing behaviour, expected behaviour>
---
Bug: $ARGUMENTS

Read STATUS.md. If the bug report contains a secret or personal data, say so first and continue
with placeholders.

1. Locate: identify the owning repo(s). Delegate to that repo's dev subagent.
2. Reproduce: branch fix/<short-slug>. Write a failing test that reproduces the bug. Show it failing.
3. Fix: smallest change that makes it pass. Do not modify other existing tests.
4. Verify: `npm run check` green. If the fix changes the API contract, run `openapi:export`
   and `gen:api` + check in affected clients.
5. Review: reviewer subagent on the diff (short pass).
6. Wrap up: add a line to STATUS.md (Known issues → resolved, or Done). Commit, do not push.
   Reply with root cause (1–2 lines), the test name, and final check output.
