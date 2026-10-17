# Irbis QA toolkit (Android)

Drives the Irbis app on an Android emulator or phone over adb and keeps the proof: screenshots, step times and QA
events per case. Screen video is opt-in (`QA_VIDEO=1`) — off by default to keep runs cheap. Used by `/qa-plan`, `/qa-run`, `/qa-retest`. Adapted from the Bellissimo QA `runner`:
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

## How it fits together (token-lean by design)
- **Runs happen in the `qa-tester` subagent (Sonnet)**; the main conversation sees only a ≤12-line summary.
- **The case script is the plan:** `qa/<slug>/cases/scripts/TC-NNN.py` = META (title, requirement, precondition,
  steps, expected + evidence) + `run(c)`. `gencase.py doc <slug>` renders the readable `Test_<slug>.md`.
- **Standards suite** (`scripts/qa/standards/STD-*.py`) — dark mode, offline, translated copy + long-text layout —
  runs on every screen in the feature's `_feature.SCREENS`, so feature cases cover only their ACs.
- **Evidence:** full screenshot (proof) + a small crop of the case's `focus` testID (what a reviewer reads). Only ids
  with ❌ or — are looked at; STD-TEXT gives one composite image. No video unless `QA_VIDEO=1`.
- **Defects** point at their failing case ids (`Cases`); a retest re-runs exactly those. Bug files are short.
- **run.md**: a table row per case; a full section only for cases that did not pass.

## Layout
```
irbis-docs/
  .claude/agents/qa-tester.md   the procedure (plan / run / retest) — loaded only by the subagent
  scripts/qa/
    rec/       config.py (qa.config.json + env) · drv.py (device helpers) · rec.py (steps/events; video opt-in)
               session.py (up/down; emulator emulates the phone) · events.py · mockloop.sh · caption.py · blur.py
    case/      gencase.py (new/doc/list) · runcase.py (new/run/finish) · casekit.py (`c`) · runmd.py · bugs.py
    standards/ _std.py · STD-DARK.py · STD-OFFLINE.py · STD-TEXT.py   (STD-KEYBOARD arrives with the first input screen)
  qa/
    qa.config.json   package, activity, event tag, video, serial, emulate_phone
    BUGS.md          every defect (generated)
    _templates/BUG_TEMPLATE.md
    <slug>/cases/scripts/{_feature.py, TC-NNN.py} · cases/Test_<slug>.md (generated)
    <slug>/runs/<YYYY-MM-DD_HHMM>/{run.md, proof/<id>/…, proof/_run/review/<id>/*.png}
    <slug>/bugs/D{n}_{name}/D{n}_{name}.md
```

## The app's side of the contract (irbis-app engineering standards §16)
- **testID** on every interactive element and every element a test asserts on: `<feature>.<element>`
  (`spot.checkin-button`). On Android it is the node's resource-id → `tap("spot.checkin-button", exact=True)`.
- **QA event log** in dev/staging builds: `src/shared/utils/qaLog.ts` logs `IRBIS_QA {"event": "...", ...}`.
  Names and non-personal props only. The app must emit `location_received { is_mocked, accuracy_m }` when it
  reads a fix — mock-location cases wait for it.

## Devices
| Device | `QA_SERIAL` | Use for |
|---|---|---|
| Emulator `pixel-8a` (Android 15, arm64, Google Play image) | `emulator-5554` | default for every run and retest |
| Owner's Galaxy S25 Ultra (Android 16) | `RFCY616LFMX` | real GPS / camera / hotspot, Samsung font scale & edge UI, before a release |
Start the emulator: `~/Library/Android/sdk/emulator/emulator -avd pixel-8a -no-boot-anim &`. Install the same APK on
either (`adb -s <serial> install -r …`); the app reaches the local API through `adb reverse tcp:3000 tcp:3000` on both.

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
PY=~/.claude/venvs/qa/bin/python; export QA_SERIAL=emulator-5554
python3 scripts/qa/rec/session.py up                          # emulator: density 450 + font 1.15 like the phone
$PY scripts/qa/case/gencase.py new  health TC-006 "title" --priority P1 --ac AC3
$PY scripts/qa/case/gencase.py doc  health                    # regenerate Test_health.md
R=$($PY scripts/qa/case/runcase.py new health --build "…" --backend "…" --scope "…")
$PY scripts/qa/case/runcase.py run $R TC-001
$PY scripts/qa/case/runcase.py run $R STD-TEXT@status
$PY scripts/qa/case/runcase.py finish $R $R/proof/_run/verdicts.json
python3 scripts/qa/case/bugs.py next health | index | open | find health/D2
python3 scripts/qa/rec/session.py down
```

## Gotchas (from the original runner's measured runs)
- **Mock location on a real phone:** `session.py up --mock` turns Google *Location Accuracy* off, otherwise
  Play Services mixes the real Wi-Fi fix in and it wins. `open_app_at` opens Google Maps for ~4 s first so the
  cache holds the mock point, and declines Google's "No thanks" accuracy prompt. The emulator needs none of it.
  If the app reads location through Android's LocationManager (not Play Services), the test providers apply directly.
- **Wait for states, not time.** `wait`, `wait_any`, `wait_event`, `no_event(window)` — fixed sleeps only for a
  window the plan names, ≤0.5 s for an animation.
- **One case per call**, in the foreground. Long background sweeps get killed under memory pressure.
- **A script's reading can be wrong** (it once read a field behind a dialog as the dialog). The crop decides.
- **uiautomator bounds can differ from what is drawn** (health/D2: a chip overflowed visually while its node stayed inside) — layout checks are judged on the crop.
- **Two-finger gestures** can't be sent over adb on a non-rooted phone → those cases are manual.
- **A notification banner** can steal a tap mid-recording → `session.py up` sets Do Not Disturb.
- **An OTA/JS-only update keeps versionName/versionCode** → record the irbis-app commit; it's the only way to
  know what changed between a defect's build and the retest build.
