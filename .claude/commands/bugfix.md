---
description: Fix a bug — reproduce with a failing test first, then fix
argument-hint: <slug>/D{n} (a defect logged by /qa-run) | <repo?> <error/log line> — <failing behaviour, expected behaviour>
---
Bug: $ARGUMENTS

Read STATUS.md. If the bug report contains a secret or personal data, say so first and continue
with placeholders.

If the argument is a defect ref (`check-in/D3`): resolve it with
`python3 scripts/qa/case/bugs.py find <ref>` and read that `D{n}_{name}.md` — its Steps, Actual, Expected,
the quoted AC and "Cause in code" are the bug report. Do not edit the bug file; verification happens on the device
with `/qa-retest <ref>`, which re-runs the defect's `Cases`.

1. Locate: identify the owning repo(s). Delegate to that repo's dev subagent with the bug file (or a ≤20-line fix
   brief) as its brief — it reads RULES.md, the brief and the files the bug's "Cause in code" names.
2. Reproduce: branch fix/<short-slug>. Write a failing test that reproduces the bug. Show it failing.
3. Fix: smallest change that makes it pass. Do not modify other existing tests.
4. Verify: `npm run check` green. If the fix changes the API contract, run `openapi:export`
   and `gen:api` + check in affected clients.
5. Review: reviewer subagent on the diff (short pass).
6. Wrap up: add a line to STATUS.md (Known issues → "fix committed, awaiting retest" for a defect ref,
   else resolved / Done). Commit, do not push.
   Reply with root cause (1–2 lines), the test name, and final check output. For a defect ref, end with:
   "Build the app and run `/qa-retest <ref>` to verify on the device." 
