# Irbis QA toolkit (Android)

Drives the Irbis app on a real Android phone (or emulator) over adb, records every case with captions,
and keeps the proof. Used by `/qa-plan`, `/qa-run`, `/qa-retest`. Adapted from the Bellissimo QA `runner`:
only the generic Android parts were kept; Expo, ADO and Bellissimo-specific helpers were dropped.

## One-time setup (done on this Mac 2026-10-16)
```bash
brew install scrcpy ffmpeg                       # adb is already in /opt/homebrew/bin
python3 -m venv ~/.claude/venvs/qa
~/.claude/venvs/qa/bin/pip install -r scripts/qa/requirements.txt
```
Phone: Developer options → USB debugging on, connect, accept the RSA prompt, `adb devices` shows `device`.
Device UI in **English** (session.py reads the Location Accuracy switch by its English label).
Test account signed in on the phone. Phone/OTP for scripts that must type them: export `IRBIS_QA_PHONE`,
`IRBIS_QA_OTP` in your shell profile yourself — never in a file or the chat.

## Layout
```
irbis-docs/
  scripts/qa/
    rec/   config.py   qa/qa.config.json + env overrides (package, activity, event tag)
           drv.py      device helpers: nodes/find/tap/wait (text or testID), QA events, mock location,
                       app launch/deep link, device conditions (network, font, dark, rotation, permissions)
           rec.py      scrcpy recorder: start/step/shot/stop → render (captions + verdict) → check → prune
           caption.py  caption strip under the video (Pillow; Homebrew ffmpeg has no drawtext)
           events.py   parses IRBIS_QA lines from logcat
           session.py  up [--mock] / down: show taps, Do Not Disturb, mock location; restores everything
           mockloop.sh re-sends the mock point every second (started by session.py up --mock)
           blur.py     blur a real person's data in a video before it leaves the machine
    case/  gencase.py  one script per test case; `check` finds missing/stale scripts via plan_hash
           runcase.py  new (run folder) · run (one case per call) · finish (render + run.md)
           casekit.py  the `c` object a case script uses
           runmd.py    run.md rows and sections
           bugs.py     next D number · index (qa/BUGS.md) · open · find <slug>/D{n}
  qa/
    qa.config.json     Android package / activity / event tag of the build under test
    BUGS.md            every defect of every feature (generated)
    _templates/        Test_TEMPLATE.md · BUG_TEMPLATE.md · repro_TEMPLATE.py
    <slug>/
      cases/Test_<slug>.md          the plan (/qa-plan)
      cases/scripts/TC-NNN.py       case library, reused by every run; _feature.py shared helpers
      runs/YYYY-MM-DD_HHMM/run.md   one run: manifest, table, every case's expected vs actual, defects
      runs/…/proof/TC-NNN/          screenshots, video.mp4, video_steps.tsv, events.txt, result.json
      bugs/README.md                this feature's defects (generated) + common setup
      bugs/D{n}_{name}/             D{n}_{name}.md · video/ · image/ · others/ (repro.py, steps, events)
```
Media (`*.mp4`, `*.png`) is git-ignored; Markdown, scripts, step times and events are committed.

## The app's side of the contract (irbis-app engineering standards §16)
- **testID** on every interactive element and every element a test asserts on: `<feature>.<element>`
  (`spot.checkin-button`). On Android it is the node's resource-id → `tap("spot.checkin-button", exact=True)`.
- **QA event log** in dev/staging builds: `src/shared/utils/qaLog.ts` logs `IRBIS_QA {"event": "...", ...}`.
  Names and non-personal props only. The app must emit `location_received { is_mocked, accuracy_m }` when it
  reads a fix — mock-location cases wait for it.

## Verdicts
| Verdict | When |
|---|---|
| Pass | every Expected bullet observed **and** its proof captured |
| Fail | at least one bullet not observed, proof captured |
| Blocked | precondition / resource / `→ check:` checkpoint did not hold (the setup failed, not the app) |
| Not run | proof could not be captured, or the case was not reached |
Retests: **Fixed** (expected holds and the bug's code path was exercised) · **Not fixed** · **Not reached**.

## Quick reference
```bash
PY=~/.claude/venvs/qa/bin/python
python3 scripts/qa/rec/session.py up --mock            # before the first recording
$PY scripts/qa/case/runcase.py new check-in --build "release apk, irbis-app a1b2c3d" --backend dev
python3 scripts/qa/case/gencase.py check qa/check-in/cases/Test_check-in.md
python3 scripts/qa/case/gencase.py new   qa/check-in/cases/Test_check-in.md TC-001
$PY scripts/qa/case/runcase.py run    qa/check-in/runs/2026-10-20_1400 TC-001
$PY scripts/qa/case/runcase.py finish qa/check-in/runs/2026-10-20_1400 qa/check-in/runs/2026-10-20_1400/proof/_run/verdicts.json
python3 scripts/qa/case/bugs.py next check-in      # → D4
$PY qa/check-in/bugs/D4_…/others/repro.py
python3 scripts/qa/rec/rec.py render qa/check-in/bugs/D4_… --verdict fail --expected "…" --actual "…"
python3 scripts/qa/rec/rec.py check  qa/check-in/bugs/D4_…
python3 scripts/qa/case/bugs.py index
python3 scripts/qa/rec/session.py down                 # restores the phone; prints the cleanup table
```

## Gotchas (from the original runner's measured runs)
- **Mock location on a real phone:** `session.py up --mock` turns Google *Location Accuracy* off, otherwise
  Play Services mixes the real Wi-Fi fix in and it wins. `open_app_at` opens Google Maps for ~4 s first so the
  cache holds the mock point, and declines Google's "No thanks" accuracy prompt. The emulator needs none of it.
  If the app reads location through Android's LocationManager (not Play Services), the test providers apply directly.
- **Wait for states, not time.** `wait`, `wait_any`, `wait_event`, `no_event(window)` — fixed sleeps only for a
  window the plan names, ≤0.5 s for an animation.
- **One case per call**, in the foreground. Long background sweeps get killed under memory pressure.
- **A script's reading can be wrong** (it once read a field behind a dialog as the dialog). The screenshot decides.
- **Two-finger gestures** can't be sent over adb on a non-rooted phone → those cases are manual.
- **A notification banner** can steal a tap mid-recording → `session.py up` sets Do Not Disturb.
- **An OTA/JS-only update keeps versionName/versionCode** → record the irbis-app commit; it's the only way to
  know what changed between a defect's build and the retest build.
