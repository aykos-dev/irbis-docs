---
description: Write a feature's Android test cases (scripts are the plan) — runs in the qa-tester subagent
argument-hint: <slug>
---
Delegate to the **qa-tester** subagent: "plan $ARGUMENTS". Relay its ≤12-line summary.
If it returns an ambiguity question, ask the owner (AskUserQuestion), record the answer in the spec's Assumptions,
then send the answer back to the same subagent to finish. Do not read the case scripts yourself.
