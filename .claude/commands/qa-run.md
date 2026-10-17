---
description: Run a feature's test plan on an Android phone, record proof, and log every defect to qa/<slug>/bugs/
argument-hint: <slug> [build: apk path | "build" | "installed"] [scope: core | TC-001,TC-004 | fails-of <run>]
---
QA run: $ARGUMENTS

You drive the Irbis app on a real Android device over adb, decide verdicts only from captured proof, and
leave a run folder plus one folder per defect. Tools: `scripts/qa/` (read `scripts/qa/README.md` once per
session). Python: `PY=~/.claude/venvs/qa/bin/python`. Everything below runs from `irbis-docs/`.

**Evidence = screenshots + steps + QA events.** No screen video by default (token cost); record video only when the
owner asks for it (`QA_VIDEO=1`). **Device:** the Android emulator (`pixel-8a`, `QA_SERIAL=emulator-5554`) is the
default; the owner's phone (`QA_SERIAL=RFCY616LFMX`) for hardware-dependent cases (real GPS, camera, OEM quirks) and
before a release. With more than one device attached, always set `QA_SERIAL`.

**Three rules:** (1) **No proof, no Pass** — a bullet without its artefact is `Not run`, never Pass.
(2) **Blocked is decided in preflight**, in one message, not discovered one case at a time.
(3) **Observe, don't change the system** — no backend config edits, no production, never sign the test
account out (signing in needs an OTP from me), never clear app data.

## 1. Preflight (before touching the app)
1. Plan: `qa/<slug>/cases/Test_<slug>.md`. Missing → stop and run `/qa-plan <slug>` first.
2. Read `features/<slug>.md` (AC + Assumptions + Open questions). An AC is the source of truth; the code is not.
3. Device: `adb devices -l` (exactly one device, unlocked). None → tell me to connect the phone with USB
   debugging and stop.
4. Build — whichever I gave:
   - apk path → `adb install -r <apk>`;
   - `build` → in `../irbis-app`: `git rev-parse --short HEAD` + `git status --short` (record a dirty tree),
     `cd android && ./gradlew assembleRelease` (bundled JS, no Metro) → install
     `android/app/build/outputs/apk/release/app-release.apk`; if the project defines a staging variant, use it;
   - `installed` / nothing → use what is on the phone.
   Then record `versionName (versionCode)` (`drv.app_version()`), commit, backend host. A debug build needs
   Metro (`npm start` in irbis-app + `adb reverse tcp:8081 tcp:8081`) — prefer release.
5. Config: `qa/qa.config.json` package matches `adb shell pm list packages | grep irbis`. Fix the file if not.
6. Sort every in-scope case by its **Env** line: `auto`, `manual` (I do it, you capture), `Blocked`
   (resource or `⚠️ DATA` the environment cannot provide — name it), `out of scope`. Resolve `⚠️ DATA` now
   (pick a real value meeting the stated requirement and write it into run.md) or block those cases.
7. Ask once (AskUserQuestion), only what changes verdicts: is creating test data on this backend OK, manual
   cases now or later, network/location differences from the plan. Don't ask what the device or plan answers.
8. Say the sort in chat: counts auto / manual / Blocked / out of scope, Blocked reasons grouped.

## 2. Run folder and session
- `$PY scripts/qa/case/runcase.py new <slug> --build "<source, commit>" --backend <host> --scope "<…>"`
  → prints the run dir `qa/<slug>/runs/YYYY-MM-DD_HHMM/` with `run.md` (Status: in progress). Fill the
  Blocked reasons line.
- `python3 scripts/qa/rec/session.py up [--mock]` (`--mock` when any case moves the phone's location).

## 3. Execute — one case per call
1. `python3 scripts/qa/case/gencase.py check qa/<slug>/cases/Test_<slug>.md` → write scripts only for
   `missing` / `stale` (`gencase.py new … TC-NNN` makes the skeleton; shared points/accounts go in
   `qa/<slug>/cases/scripts/_feature.py`). Fill each from the plan: precondition `c.pre`, each step
   `c.step(n, …)`, each `→ check:` as `c.checkpoint(…)`, each Expected bullet `c.result(n, ok, observed, proof)`
   (`ok=None` when only a person can judge). Wait for states (`wait`, `wait_any`, `wait_event`, `no_event`),
   never fixed sleeps except the windows the plan names. Find elements by testID (`exact=True`) first.
2. `$PY scripts/qa/case/runcase.py run <run dir> TC-NNN` — one call per case, in plan order (smoke first).
3. **Review every case yourself** before any verdict: the 540 px copies in `proof/_run/review/TC-NNN/`
   (Read them; open the full screenshot when text is small), events in `result.json` / `events.txt`. The
   screenshot decides, not the script's reading. Also check `drv.crashed()` output in the events if the app
   vanished.
4. Manual cases: batch them in one message (what to do, what to look for, "say done and I'll capture").
5. Anything no case asked for (layout clipped, a toast on every open, a crash) → the nearest case's `extra`
   and run.md "Additional observations". It can still become a defect.
6. `proof/_run/verdicts.json` — one entry per in-scope case: `{"TC-NNN": {"verdict": "Pass|Fail|Blocked|Not run",
   "line", "conclusion", "caption", "actual": {n: text}, "ok": {n: bool}, "extra"}}`; not executed →
   `verdict`, `title`, `priority`, `reason`. Then `$PY scripts/qa/case/runcase.py finish <run dir> <verdicts.json>`
   and Read one `.check.png`: it must show what the last caption says.

## 4. Defects → qa/<slug>/bugs/
Group the Fails (and real problems from Additional observations) **by root cause**, one defect each:
1. Number: `python3 scripts/qa/case/bugs.py next <slug>` → `D{n}`. Folder `qa/<slug>/bugs/D{n}_{3-6-word-kebab}/`
   with `video/`, `image/`, `others/`. Seen again in a later run → update that folder, no new number.
2. Bug file `D{n}_{name}.md` from `qa/_templates/BUG_TEMPLATE.md`: title `[Area / Sub-area] - present-tense
   wrong behaviour`, Severity (1 Critical: crash/data or XP loss · 2 High: core rule broken · 3 Medium · 4 Low),
   the **Reference line quoting the broken AC word for word**, 3–6 Steps to Reproduce from a clean start,
   one-paragraph Actual and Expected. No run jargon (`TC-…`, `ACC-A`, raw coordinates) in the Bug section —
   write "an account with no check-ins today", "a location 201 m from the spot (mock location)". Cause in code:
   if you can locate it in `../irbis-app` / `../irbis-api`, cite `file:line` in Internal notes; do not fix it.
3. **Reproduce it** with its own script (`qa/_templates/repro_TEMPLATE.py` → `others/repro.py`), following the
   bug's Steps to Reproduce with the same step numbers, a screenshot at every state the Actual Result names, and the
   failing state still on screen when it stops; then `rec.py render … --verdict fail --expected … --actual …` (records
   the verdict in the steps file) and `check`. Not reproduced → no folder; say "not reproduced" in run.md Defects.
4. `python3 scripts/qa/case/bugs.py index` (updates `qa/BUGS.md` and the feature's `bugs/README.md`).

## 5. Close
- run.md: **Results** (Pass / Fail / Blocked / Not run with ids), **Defects** (table `| D | Severity | Defect | Cases | Bug file |`),
  **Follow-ups** (manual cases pending, reruns). Check every proof path exists. Status: closed (unless manual cases pend).
- `python3 scripts/qa/rec/session.py down` → paste its table into run.md Follow-ups.
- Add one line to `STATUS.md` → Known issues per open defect: `<slug>/D{n} — title (Severity)`.
- Commit irbis-docs (`qa(<slug>): run YYYY-MM-DD_HHMM — N defects`). Media is git-ignored. Do not push.
- Reply: run folder, totals, each defect in one line with its ref (`<slug>/D{n}`) and folder, what is pending.
  Tell me: fix with `/bugfix <slug>/D{n}`, then check with `/qa-retest <slug>/D{n} …` or `/qa-retest open`.

## Never
Verdict without the proof file · count a failed `→ check:` as Fail · put a verdict caption on a video before
reviewing the evidence · edit the plan or the spec to match the app · fix app code during a run · print or
write a token, OTP or unmasked phone number · run a long sweep as a background task (foreground calls of a
few minutes each).
