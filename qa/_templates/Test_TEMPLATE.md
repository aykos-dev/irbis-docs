# Test_<slug> — <feature title>

**Spec:** [features/<slug>.md](../../../features/<slug>.md) (status: Approved) · **Written:** YYYY-MM-DD
**Source of truth:** the spec's acceptance criteria. Code is never the source of truth: when the app and an AC
disagree, the case keeps the AC's expected result and the case fails.

## 1. How to read
- `### ★ TC-NNN · P{0-3} · title` — one case. **Requirement** names the AC it checks; **Env** says platform and
  how it runs (`auto (adb)`, `auto (adb + mock location)`, `manual (reason)`); `resources:` are ids from §2–3.
- **Steps** are one action each. `→ check:` is a checkpoint: if it does not hold, the *setup* failed and the
  case is **Blocked**, never Fail.
- **Expected result** is one final state. Every bullet names its evidence after ` — `. A Pass needs proof for
  every bullet ("no proof, no Pass").
- An absence or a timing ("no dialog", "instantly") always has a window and a trigger ("within 5 s after tapping
  Check in").
- Group 1 Core = must pass before release. Group 2 Supplementary = run when time allows.
- P0 = feature unusable / data or XP loss · P1 = the core rule at its main boundary · P2 = secondary rule,
  recoverable failure, most negatives · P3 = cosmetic, rare edge.
- `⚠️ DATA` = a test data value still to find (resolved in run preflight, else its cases are Blocked).
- `⚠️ Q{n}` = rests on an open question in the spec; the expected result follows the reading the spec most supports.

## 2. Resources
| Env | What it needs |
|---|---|
| Android | device/emulator (model, Android version), build (variant, how installed), backend host |
| Tools | adb, scrcpy, mock location (`session.py up --mock`) |
| Access | test accounts (§3), admin role on web for setup, … |

## 3. Test data
| ID | What | Value |
|---|---|---|
| ACC-A | User with no check-ins today | dev, phone ***XXXX (OTP via `IRBIS_QA_OTP` env var — never written here) |
| SPOT-1 | Verified spot | 41.3111, 69.2797 · radius 200 m |
| P-199 | 199 m from SPOT-1 | `offset(SPOT-1, metres_north=199)` |

Setup recipes (plain steps, for a tester who joins tomorrow):
- **ACC-A:** …

## 4. Coverage matrix
**Requirements:** N AC → M cases (X Core + Y Supplementary)

| AC | Requirement (short) | Technique | Core | Supplementary |
|---|---|---|---|---|
| AC1 | Check-in only within radius | BVA (199 / 200 / 201 m) | TC-001–TC-003 | TC-020 |

Techniques: **BVA** boundary (inside / on / outside, real numbers) · **EP** one value per input class ·
**DT** one case per condition combination with a distinct outcome · **ST** one case per allowed transition and
per forbidden one (one invalid transition per case) · **EG** error guessing.
Every AC has at least one Core case. Every case appears in exactly one row.

## 5. Group 1 — Core

## ▌ 5.1 <feature area, in risk order: smoke → main rule boundary → combinations → states>

### ★ TC-001 · P1 · <what is checked, as behaviour>
---
**Requirement:** AC1 — <the rule, one line> · [→ AC1 "<the AC's own words>"](../../../features/<slug>.md#acceptance-criteria)
**Env:** Android · auto (adb + mock location) · resources: ACC-A, SPOT-1, P-199

**Precondition:**
- ACC-A signed in; no check-in at SPOT-1 today; location permission granted

**Steps:**
1. Phone location = P-199 (41.3128, 69.2797), accuracy 10 m → check: event `location_received` { is_mocked: true }
2. Open SPOT-1 (`irbis://spots/spot_1`)
3. Tap "Check in"

**Expected result** (within 5 s after step 3):
- Success sheet "+50 XP" — screenshot
- Event `checkin_succeeded` { xp_awarded: 50 } — event log

**Postcondition:** ACC-A has a check-in at SPOT-1 today (next case builds on it)

## 6. Group 2 — Supplementary

## ▌ 6.1 Engineering standards on this feature's screens
Cases derived from `irbis-app/docs/engineering-standards.md` Quick gate where this feature has a screen:
offline (`set_network(False, False)`), largest font (`font_scale(2.0)`), dark mode, landscape, keyboard over
inputs, Android back with a dirty form, process death (`process_death()`), permission denied / blocked.
