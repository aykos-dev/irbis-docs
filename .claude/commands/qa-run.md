---
description: Run a feature's cases + the standards suite on the Android emulator (or phone), log defects — in the qa-tester subagent
argument-hint: <slug> [build: apk path | "build" | "installed"] [scope: core | TC-001,TC-004 | full] [phone] [video]
---
Delegate to the **qa-tester** subagent: "run $ARGUMENTS". Defaults: emulator, no video, all cases + standards suite.
Relay its ≤12-line summary as is. Do not open run folders, screenshots or logs in this conversation unless the owner
asks about a specific case. Next step for each defect: `/bugfix <slug>/D{n}`, then `/qa-retest <slug>/D{n}`.
