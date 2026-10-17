# D{n} · {what goes wrong, one line}

| | |
|---|---|
| Status | Open · reproduced YYYY-MM-DD |
| Severity | 3 - Medium |
| Feature | [features/{slug}.md](../../../../features/{slug}.md) |
| Found | run [YYYY-MM-DD_HHMM](../../runs/YYYY-MM-DD_HHMM/run.md), TC-NNN |
| Build | com.irbis {versionName} ({versionCode}), irbis-app commit {sha} |
| Evidence | screenshots in `image/`, steps + events in `others/` (video only if recorded with `QA_VIDEO=1`) |
| Device | emulator pixel-8a (Android 15) / Galaxy S25 Ultra (Android 16) |

<!-- one row per retest, newest first, inserted above this comment:
| Retest YYYY-MM-DD | ✅ Fixed / ❌ Not fixed / ⏸ Not reached on {build} ([video](video/D{n}_{name}__retest-YYYY-MM-DD.mp4)) |
-->

## Bug

**Title:** [Area / Sub-area] - {wrong behaviour, present tense, ~60–95 chars, no trailing period}

**Description**

{2–4 sentences: where in the app, what happens, the consequence for the user.}

*Reference: features/{slug}.md acceptance criteria AC{n}: "{the broken AC text, word for word}"* {(QA reading, owner to confirm) — only when it rests on an open question}

- **Environment / Build Version:** {device (Android version)}, Irbis app {versionName} ({versionCode}), backend {host}

**Steps to Reproduce**

1. {state setup: signed-in account, permission, location}
2. …
3. {the observation step} <!-- 3–6 steps; more means the repro is not minimal -->

**Actual Result**

{one paragraph: what is seen — exact strings in quotes, QA event names and values}

**Expected Result**

{one paragraph: one assertable statement}

---

## Internal notes

### Recording
- Re-record: `~/.claude/venvs/qa/bin/python others/repro.py`
- Video: [video/D{n}_{name}.mp4](video/D{n}_{name}.mp4)

| Video time | Caption |
|---|---|

Events (`others/events.txt`): …
Screenshots: [image/01_….png](image/01_….png)

### Test data
{accounts (masked), mock points, data created}

### Which AC is broken
- AC{n}: "{quote}" — cause in code (for the developer): `{repo}/{file}:{line}` … | "not located"

### Why {severity}

### Notes
