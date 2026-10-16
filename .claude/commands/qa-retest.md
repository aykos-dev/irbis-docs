---
description: Re-check logged defects on a new Android build — Fixed / Not fixed / Not reached, with video proof
argument-hint: <slug>/D{n} [<slug>/D{n} …] | open | <slug> [build: apk path | "build" | "installed"]
---
Retest: $ARGUMENTS

Re-check defects that `/qa-run` logged in `qa/<slug>/bugs/`. Tools: `scripts/qa/` (see `scripts/qa/README.md`).
`PY=~/.claude/venvs/qa/bin/python`. Run from `irbis-docs/`.

## 1. Scope
- Resolve the refs: `python3 scripts/qa/case/bugs.py find <ref>` for each; `open` →
  `python3 scripts/qa/case/bugs.py open`; a bare `<slug>` → that feature's open defects.
  Show the list (ref, severity, title, current status) before starting.
- Read each bug file fully — the **Bug** section's Steps to Reproduce and Expected Result are what is checked,
  and `Build` says which build it was found on.

## 2. What changed (before touching the device)
- For each bug: in `../irbis-app` (and `../irbis-api` if the cause is there) list the commits since the commit
  in the bug's `Build` row: `git log --oneline <old>..HEAD` and `git diff --stat <old>..HEAD`. Read the diff of
  the files the bug's "Cause in code" points at. Note whether the old steps still reach the changed code path —
  a fix behind a new condition can make the old steps skip it.
- No new commit touching the cause → say so; the retest still runs (the fix may be elsewhere).

## 3. Build and session
- Build/install exactly as `/qa-run` §1.4 (apk path / `build` / `installed`); record `versionName (versionCode)`
  and commit. Same build as the bug's `Build` row → tell me and ask whether to continue.
- `python3 scripts/qa/rec/session.py up [--mock]`.

## 4. Per defect — one call each
1. Copy `others/repro.py` → `others/repro__retest-YYYY-MM-DD.py`, set `VARIANT = "retest-YYYY-MM-DD"`.
   Update it if the bug's steps or the app's testIDs changed; pick fresh test data where an earlier
   recording could leak state (a spot already checked in today, a dismissed prompt).
2. `$PY others/repro__retest-YYYY-MM-DD.py` — captions `Observed:` stay neutral.
3. Look at `image/*__retest-…png` and `others/events__retest-….txt` yourself, then decide:
   - **Fixed** — the Expected Result holds **and** the steps really went through the bug's code path;
   - **Not fixed** — the Actual Result (or another wrong result) still shows;
   - **Not reached** — a precondition or setup failed, so the path wasn't exercised (say what blocked it).
     A missing precondition is never "Fixed".
4. `python3 scripts/qa/rec/rec.py render <bug folder> --variant retest-YYYY-MM-DD --verdict fixed|not-fixed|blocked
   --expected "…" --actual "…"`, then `rec.py check …` and Read the frame it names.
5. If the original case script exists, also run the case in a new run folder
   (`runcase.py new <slug> --scope "retest of D3, D5"` then `runcase.py run … TC-NNN`) so the case library
   stays green — optional when only the bug matters.

## 5. Write it down
- Bug file: add `| Retest YYYY-MM-DD | ✅ Fixed / ❌ Not fixed / ⏸ Not reached on {build} ([video](…)) |` to the
  header table (newest first), and a `### Retest YYYY-MM-DD` block at the top of Internal notes (result, build +
  commit, what changed in code, caption table, events, screenshots, anything that differed from the steps).
- Status row: Fixed → `Fixed · retest YYYY-MM-DD`; Not fixed → `Not fixed · retest YYYY-MM-DD`;
  Not reached → leave the status, note it.
- `python3 scripts/qa/case/bugs.py index`. `STATUS.md`: remove fixed ones from Known issues (add to Done:
  `<slug>/D{n} fixed — verified YYYY-MM-DD on <build>`), keep not-fixed ones.
- A new problem seen during the retest → log it as a new defect exactly as `/qa-run` §4.
- `python3 scripts/qa/rec/session.py down`; commit irbis-docs (`qa(<slug>): retest D3, D5 — 1 fixed, 1 not fixed`).
  Do not push.

## 6. Reply
One table — `| Ref | Severity | Result | Build | Video |` — then what was not reached and why, any new
defects, and the cleanup. Not fixed → suggest `/bugfix <slug>/D{n}` again.
