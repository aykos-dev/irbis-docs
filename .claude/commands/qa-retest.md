---
description: Re-check logged defects on a new build by re-running only their cases — in the qa-tester subagent
argument-hint: <slug>/D{n} [<slug>/D{n} …] | open [build] [full] [phone]
---
Delegate to the **qa-tester** subagent: "retest $ARGUMENTS". It re-runs only each defect's `Cases` (full suite only
with `full`, e.g. before a release). Relay its ≤12-line summary. Not fixed → suggest `/bugfix <slug>/D{n}` again.
