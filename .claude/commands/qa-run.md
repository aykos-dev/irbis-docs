---
description: Run a feature's P0 cases (core) or all cases + the standards suite (full) on the Android emulator (or phone), log defects — in the qa-tester subagent
argument-hint: <slug> [build: apk path | "build" | "installed"] [scope: core | TC-001,TC-004 | full] [phone] [video]
---
Delegate to the **qa-tester** subagent: "run $ARGUMENTS". Defaults: emulator, no video, scope `core` (P0 cases only,
no standards suite). Use `full` (all cases + standards suite) once per feature, right before merging its branch.
Relay its ≤12-line summary as is. Do not open run folders, screenshots or logs in this conversation unless the owner
asks about a specific case. Next step for each defect: `/bugfix <slug>/D{n}`, then `/qa-retest <slug>/D{n}`.
