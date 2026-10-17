# Run 2026-10-17_1648 — auth
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — installed devRelease (uz.irbis.app.dev), app HEAD 1a4978d
**Backend:** irbis-api start:dev local
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** core (P0)
**Blocked reasons:** —
**Plan:** ../../cases/Test_auth.md

## Results
19 pass / 0 fail / 0 blocked / 0 not run (core P0: TC-001, 003, 005, 007, 012, 014, 016, 019, 021, 022, 027, 028, 030, 031, 032, 036, 037, 041, 042). TC-003 and TC-019 had script readings wrong; crops decided Pass.

## Defects
None.

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| TC-001 | Cold start lands on the five-tab bar with no log-in wall | Pass | script all green | — | [proof/TC-001/](proof/TC-001/) |
| TC-003 | Guest Profile matches the A6 canvas content | Pass | script bullet 3 red; crop OK | — | [proof/TC-003/](proof/TC-003/) |
| TC-005 | Username length boundaries: 2 refused, 3 and 20 accepted, 21 refused | Pass | script all green | — | [proof/TC-005/](proof/TC-005/) |
| TC-007 | Reserved and taken usernames refused; live availability moves pristine → validating → success | Pass | script all green | — | [proof/TC-007/](proof/TC-007/) |
| TC-012 | Sign-up with a 6-char password and no phone logs in and returns to Profile | Pass | script all green | — | [proof/TC-012/](proof/TC-012/) |
| TC-014 | Wrong password and unknown username give the same generic message | Pass | script all green | — | [proof/TC-014/](proof/TC-014/) |
| TC-016 | Fifth wrong password locks the username for 15 minutes and says how long | Pass | script all green | — | [proof/TC-016/](proof/TC-016/) |
| TC-019 | Forgot password shows the same code screen for unknown, phoneless and verified accounts | Pass | script 'same texts' red; crops identical | — | [proof/TC-019/](proof/TC-019/) |
| TC-021 | Correct code and a new password log the user in and end the other sessions | Pass | script all green | — | [proof/TC-021/](proof/TC-021/) |
| TC-022 | Three wrong codes void the code; the right code is then refused | Pass | script all green | — | [proof/TC-022/](proof/TC-022/) |
| TC-027 | Signed-in Profile shows username, Recovery phone row and Sign out | Pass | script all green | — | [proof/TC-027/](proof/TC-027/) |
| TC-028 | Add a recovery phone and verify it with the SMS code | Pass | script all green | — | [proof/TC-028/](proof/TC-028/) |
| TC-030 | Sign out returns to the guest Profile and stays signed out after restart | Pass | script all green | — | [proof/TC-030/](proof/TC-030/) |
| TC-031 | Log-in prompt for a guest: shown with the reason, Not now closes with nothing lost | Pass | script all green | — | [proof/TC-031/](proof/TC-031/) |
| TC-032 | Log in from the prompt: the gated action continues exactly once | Pass | script all green | — | [proof/TC-032/](proof/TC-032/) |
| TC-036 | Tokens: ~15-min access, refresh rotates, reuse revokes the family, refresh stored hashed | Pass | script all green | — | [proof/TC-036/](proof/TC-036/) |
| TC-037 | Refresh failure after a 401 returns the app to guest with a toast | Pass | script all green | — | [proof/TC-037/](proof/TC-037/) |
| TC-041 | A blocked user cannot log in and sees the block reason | Pass | script all green | — | [proof/TC-041/](proof/TC-041/) |
| TC-042 | A signed-in user who gets blocked is signed out on the next request with the same message | Pass | script all green | — | [proof/TC-042/](proof/TC-042/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

## Additional observations

## Follow-ups
- Script fixes: TC-003 bullet 3 text match for 'Safety & SOS' failed though the node exists; TC-019 same-texts compare must mask the countdown digits.
- Installed build is 4c563f2-era; later app commits are chore/test only. Stale run folder ../2026-10-17_1528 (in progress, empty) can be deleted.
