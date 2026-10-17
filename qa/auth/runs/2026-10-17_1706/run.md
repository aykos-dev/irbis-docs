# Run 2026-10-17_1706 — auth
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — installed on device (app HEAD 1a4978d)
**Backend:** local api :3000
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** full
**Blocked reasons:** TC-035 (guest.merged already set on device; needs fresh install); STD-TEXT@* (harness switches system locale, app uses in-app language)
**Plan:** ../../cases/Test_auth.md

## Results
49 pass / 1 fail / 7 blocked / 0 not run (57 ids: 39 TC + 18 STD).
Fail: TC-040 (D1). Blocked: TC-035, STD-TEXT@login/signup/forgot/guest-profile/gate/account-profile.
Toolkit fixes during run: drv.py now html-unescapes UI-dump text (&amp; broke 'Safety & SOS' match, TC-003); TC-010 hides the keyboard before reading the error.

## Defects
| D1 | irbis:// deep links not resolved (no intent-filter) | 2 - High | TC-040 | [D1](../../bugs/D1_deeplink-intent-filter/D1_deeplink-intent-filter.md) |

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| TC-001 | Cold start lands on the five-tab bar with no log-in wall | Pass | script all green | — | [proof/TC-001/](proof/TC-001/) |
| TC-002 | Path, Explore, Lessons, Community show the coming-soon empty state | Pass | script all green | — | [proof/TC-002/](proof/TC-002/) |
| TC-003 | Guest Profile matches the A6 canvas content | Pass | script all green | — | [proof/TC-003/](proof/TC-003/) |
| TC-004 | Safety opens its empty state; Language opens the language sheet | Pass | script all green | — | [proof/TC-004/](proof/TC-004/) |
| TC-005 | Username length boundaries: 2 refused, 3 and 20 accepted, 21 refused | Pass | script all green | — | [proof/TC-005/](proof/TC-005/) |
| TC-006 | Username characters and dot rules | Pass | script all green | — | [proof/TC-006/](proof/TC-006/) |
| TC-007 | Reserved and taken usernames refused; live availability moves pristine → validating → success | Pass | script all green | — | [proof/TC-007/](proof/TC-007/) |
| TC-008 | Password rules in the form: 5 chars, 65 chars, equal to username, common password | Pass | script all green | — | [proof/TC-008/](proof/TC-008/) |
| TC-009 | Password bounds through the API: 6 and 64 accepted, 5 and 65 refused | Pass | script all green | — | [proof/TC-009/](proof/TC-009/) |
| TC-010 | Recovery phone validation: 8 digits refused, 9 accepted, letters not typable | Pass | script all green | — | [proof/TC-010/](proof/TC-010/) |
| TC-011 | Terms must be accepted to create an account | Pass | script all green | — | [proof/TC-011/](proof/TC-011/) |
| TC-012 | Sign-up with a 6-char password and no phone logs in and returns to Profile | Pass | script all green | — | [proof/TC-012/](proof/TC-012/) |
| TC-013 | Sign-up with a recovery phone reports has_phone and sends a verification code | Pass | script all green | — | [proof/TC-013/](proof/TC-013/) |
| TC-014 | Wrong password and unknown username give the same generic message | Pass | script all green | — | [proof/TC-014/](proof/TC-014/) |
| TC-015 | Four wrong passwords do not lock: the fifth attempt with the right password logs in | Pass | script all green | — | [proof/TC-015/](proof/TC-015/) |
| TC-016 | Fifth wrong password locks the username for 15 minutes and says how long | Pass | script all green | — | [proof/TC-016/](proof/TC-016/) |
| TC-018 | Continue as guest closes the log-in screen | Pass | script all green | — | [proof/TC-018/](proof/TC-018/) |
| TC-019 | Forgot password shows the same code screen for unknown, phoneless and verified accounts | Pass | script all green | — | [proof/TC-019/](proof/TC-019/) |
| TC-020 | Forgot password screen shows the support path for accounts without a phone | Pass | script all green | — | [proof/TC-020/](proof/TC-020/) |
| TC-021 | Correct code and a new password log the user in and end the other sessions | Pass | script all green | — | [proof/TC-021/](proof/TC-021/) |
| TC-022 | Three wrong codes void the code; the right code is then refused | Pass | script all green | — | [proof/TC-022/](proof/TC-022/) |
| TC-023 | Send again is locked with a countdown when the code screen opens | Pass | script all green | — | [proof/TC-023/](proof/TC-023/) |
| TC-024 | An expired code is refused with a clear message | Pass | script all green | — | [proof/TC-024/](proof/TC-024/) |
| TC-025 | At most 5 reset codes per account per day | Pass | script all green | — | [proof/TC-025/](proof/TC-025/) |
| TC-026 | Reset refuses a 5-char new password and leaves the old one valid | Pass | script all green | — | [proof/TC-026/](proof/TC-026/) |
| TC-027 | Signed-in Profile shows username, Recovery phone row and Sign out | Pass | script all green | — | [proof/TC-027/](proof/TC-027/) |
| TC-028 | Add a recovery phone and verify it with the SMS code | Pass | script all green | — | [proof/TC-028/](proof/TC-028/) |
| TC-029 | A wrong verification code is refused and the phone stays unverified | Pass | script all green | — | [proof/TC-029/](proof/TC-029/) |
| TC-030 | Sign out returns to the guest Profile and stays signed out after restart | Pass | script all green | — | [proof/TC-030/](proof/TC-030/) |
| TC-031 | Log-in prompt for a guest: shown with the reason, Not now closes with nothing lost | Pass | script all green | — | [proof/TC-031/](proof/TC-031/) |
| TC-032 | Log in from the prompt: the gated action continues exactly once | Pass | script all green | — | [proof/TC-032/](proof/TC-032/) |
| TC-033 | Create account from the prompt: sign-up returns to where it started and the action runs once | Pass | script all green | — | [proof/TC-033/](proof/TC-033/) |
| TC-034 | Signed-in user: the gated action runs immediately with no prompt | Pass | script all green | — | [proof/TC-034/](proof/TC-034/) |
| [TC-035](#tc-035) | Guest language moves into the account once, after the first sign-up on the device | Blocked | script bullet 1 red: no guest_merged event | — | [proof/TC-035/](proof/TC-035/) |
| TC-036 | Tokens: ~15-min access, refresh rotates, reuse revokes the family, refresh stored hashed | Pass | script all green | — | [proof/TC-036/](proof/TC-036/) |
| TC-037 | Refresh failure after a 401 returns the app to guest with a toast | Pass | script all green | — | [proof/TC-037/](proof/TC-037/) |
| [TC-040](#tc-040) | Status is not the first screen; reachable from Debug and by deep link | Fail | bullet 3 red; crop = Path tab | ❌ 3 | [proof/TC-040/](proof/TC-040/) |
| TC-041 | A blocked user cannot log in and sees the block reason | Pass | script all green | — | [proof/TC-041/](proof/TC-041/) |
| TC-042 | A signed-in user who gets blocked is signed out on the next request with the same message | Pass | script all green | — | [proof/TC-042/](proof/TC-042/) |
| STD-DARK@login | Dark mode uses the night tokens — login | Pass | script all green | — | [proof/STD-DARK@login/](proof/STD-DARK@login/) |
| STD-OFFLINE@login | Offline shows a persistent banner and keeps the screen — login | Pass | script all green | — | [proof/STD-OFFLINE@login/](proof/STD-OFFLINE@login/) |
| [STD-TEXT@login](#std-text@login) | Copy is translated and layout survives long text — login | Blocked | harness check: untranslated under system locale | — | [proof/STD-TEXT@login/](proof/STD-TEXT@login/) |
| STD-DARK@signup | Dark mode uses the night tokens — signup | Pass | script all green | — | [proof/STD-DARK@signup/](proof/STD-DARK@signup/) |
| STD-OFFLINE@signup | Offline shows a persistent banner and keeps the screen — signup | Pass | script all green | — | [proof/STD-OFFLINE@signup/](proof/STD-OFFLINE@signup/) |
| [STD-TEXT@signup](#std-text@signup) | Copy is translated and layout survives long text — signup | Blocked | harness check: untranslated under system locale | — | [proof/STD-TEXT@signup/](proof/STD-TEXT@signup/) |
| STD-DARK@forgot | Dark mode uses the night tokens — forgot | Pass | script all green | — | [proof/STD-DARK@forgot/](proof/STD-DARK@forgot/) |
| STD-OFFLINE@forgot | Offline shows a persistent banner and keeps the screen — forgot | Pass | script all green | — | [proof/STD-OFFLINE@forgot/](proof/STD-OFFLINE@forgot/) |
| [STD-TEXT@forgot](#std-text@forgot) | Copy is translated and layout survives long text — forgot | Blocked | harness check: untranslated under system locale | — | [proof/STD-TEXT@forgot/](proof/STD-TEXT@forgot/) |
| STD-DARK@guest-profile | Dark mode uses the night tokens — guest-profile | Pass | script all green | — | [proof/STD-DARK@guest-profile/](proof/STD-DARK@guest-profile/) |
| STD-OFFLINE@guest-profile | Offline shows a persistent banner and keeps the screen — guest-profile | Pass | script all green | — | [proof/STD-OFFLINE@guest-profile/](proof/STD-OFFLINE@guest-profile/) |
| [STD-TEXT@guest-profile](#std-text@guest-profile) | Copy is translated and layout survives long text — guest-profile | Blocked | harness check: untranslated under system locale | — | [proof/STD-TEXT@guest-profile/](proof/STD-TEXT@guest-profile/) |
| STD-DARK@gate | Dark mode uses the night tokens — gate | Pass | script bullet red; crop OK | — | [proof/STD-DARK@gate/](proof/STD-DARK@gate/) |
| STD-OFFLINE@gate | Offline shows a persistent banner and keeps the screen — gate | Pass | script all green | — | [proof/STD-OFFLINE@gate/](proof/STD-OFFLINE@gate/) |
| [STD-TEXT@gate](#std-text@gate) | Copy is translated and layout survives long text — gate | Blocked | harness check: untranslated under system locale | — | [proof/STD-TEXT@gate/](proof/STD-TEXT@gate/) |
| STD-DARK@account-profile | Dark mode uses the night tokens — account-profile | Pass | script all green | — | [proof/STD-DARK@account-profile/](proof/STD-DARK@account-profile/) |
| STD-OFFLINE@account-profile | Offline shows a persistent banner and keeps the screen — account-profile | Pass | script all green | — | [proof/STD-OFFLINE@account-profile/](proof/STD-OFFLINE@account-profile/) |
| [STD-TEXT@account-profile](#std-text@account-profile) | Copy is translated and layout survives long text — account-profile | Blocked | RuntimeError profile.sign-out not found | RuntimeError: not found: profile.sign-out @ line 153 | [proof/STD-TEXT@account-profile/](proof/STD-TEXT@account-profile/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

<a id="tc-035"></a>
### TC-035 · Blocked · Guest language moves into the account once, after the first sign-up on the device
**Group:** Core · **Priority:** P1 · **Env:** Android · auto (adb)
**Case:** Guest language moves into the account once, after the first sign-up on the device · [→ Test_auth.md](../../cases/Test_auth.md#tc-035--p1--guest-language-moves-into-the-account-once-after-the-first-sign-up-on-the-device)
**Reason:** —
**Proof:** proof/TC-035/__pycache__, proof/TC-035/case.py, proof/TC-035/events.txt, proof/TC-035/video_steps.tsv

<a id="tc-040"></a>
### TC-040 · Fail · Status is not the first screen; reachable from Debug and by deep link
**Group:** Core · **Priority:** P1 · **Env:** Android · auto (adb)
**Case:** Status is not the first screen; reachable from Debug and by deep link · [→ Test_auth.md](../../cases/Test_auth.md#tc-040--p1--status-is-not-the-first-screen-reachable-from-debug-and-by-deep-link)
**Done:** dev build → 2. Profile → Debug tools → API status → 3. Deep link
**Expected** (source: —):
1. First screen is the tab bar, health.status-card absent — UI tree
2. Profile → Debug tools (profile.debug) → debug.screen → API status (debug.api-status) opens health.status-card — UI tree
3. irbis://debug/status opens health.status-card — UI tree + screenshot
**Actual:**
1. ✅ no status card on start — proof/TC-040/1_start.png
2. ✅ debug=True, status=True — proof/TC-040/2_status.png
3. ❌ deep link not delivered to app; app stays on Path tab (crop) — proof/TC-040/3_link.png
**Conclusion:** irbis://debug/status does not open the Status card. adb reports the intent cannot be resolved: AndroidManifest has no irbis:// intent-filter (only MAIN/LAUNCHER). Same for irbis://profile and irbis://debug.

<a id="std-text@login"></a>
### STD-TEXT@login · Blocked · Copy is translated and layout survives long text — login
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — login · [→ Test_auth.md](../../cases/Test_auth.md#std-textlogin--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** —
**Proof:** proof/STD-TEXT@login/__pycache__, proof/STD-TEXT@login/case.py, proof/STD-TEXT@login/en_font2.0.png, proof/STD-TEXT@login/events.txt, proof/STD-TEXT@login/ru_font1.15.png, proof/STD-TEXT@login/uz_font1.15.png, proof/STD-TEXT@login/video_steps.tsv

<a id="std-text@signup"></a>
### STD-TEXT@signup · Blocked · Copy is translated and layout survives long text — signup
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — signup · [→ Test_auth.md](../../cases/Test_auth.md#std-textsignup--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** —
**Proof:** proof/STD-TEXT@signup/__pycache__, proof/STD-TEXT@signup/case.py, proof/STD-TEXT@signup/en_font2.0.png, proof/STD-TEXT@signup/events.txt, proof/STD-TEXT@signup/ru_font1.15.png, proof/STD-TEXT@signup/uz_font1.15.png, proof/STD-TEXT@signup/video_steps.tsv

<a id="std-text@forgot"></a>
### STD-TEXT@forgot · Blocked · Copy is translated and layout survives long text — forgot
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — forgot · [→ Test_auth.md](../../cases/Test_auth.md#std-textforgot--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** —
**Proof:** proof/STD-TEXT@forgot/__pycache__, proof/STD-TEXT@forgot/case.py, proof/STD-TEXT@forgot/en_font2.0.png, proof/STD-TEXT@forgot/events.txt, proof/STD-TEXT@forgot/ru_font1.15.png, proof/STD-TEXT@forgot/uz_font1.15.png, proof/STD-TEXT@forgot/video_steps.tsv

<a id="std-text@guest-profile"></a>
### STD-TEXT@guest-profile · Blocked · Copy is translated and layout survives long text — guest-profile
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — guest-profile · [→ Test_auth.md](../../cases/Test_auth.md#std-textguest-profile--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** —
**Proof:** proof/STD-TEXT@guest-profile/__pycache__, proof/STD-TEXT@guest-profile/case.py, proof/STD-TEXT@guest-profile/en_font2.0.png, proof/STD-TEXT@guest-profile/events.txt, proof/STD-TEXT@guest-profile/ru_font1.15.png, proof/STD-TEXT@guest-profile/uz_font1.15.png, proof/STD-TEXT@guest-profile/video_steps.tsv

<a id="std-text@gate"></a>
### STD-TEXT@gate · Blocked · Copy is translated and layout survives long text — gate
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — gate · [→ Test_auth.md](../../cases/Test_auth.md#std-textgate--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** —
**Proof:** proof/STD-TEXT@gate/__pycache__, proof/STD-TEXT@gate/case.py, proof/STD-TEXT@gate/en_font2.0.png, proof/STD-TEXT@gate/events.txt, proof/STD-TEXT@gate/ru_font1.15.png, proof/STD-TEXT@gate/uz_font1.15.png, proof/STD-TEXT@gate/video_steps.tsv

<a id="std-text@account-profile"></a>
### STD-TEXT@account-profile · Blocked · Copy is translated and layout survives long text — account-profile
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — account-profile · [→ Test_auth.md](../../cases/Test_auth.md#std-textaccount-profile--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** RuntimeError: not found: profile.sign-out @ line 153
**Proof:** proof/STD-TEXT@account-profile/__pycache__, proof/STD-TEXT@account-profile/case.py, proof/STD-TEXT@account-profile/events.txt, proof/STD-TEXT@account-profile/ru_font1.15.png, proof/STD-TEXT@account-profile/uz_font1.15.png, proof/STD-TEXT@account-profile/video_steps.tsv


## Additional observations

## Follow-ups
