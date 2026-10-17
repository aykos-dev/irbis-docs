# Run 2026-10-17_1850 — onboarding
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — irbis-app feat/onboarding 5299146
**Backend:** irbis-api feat/onboarding 4471316, migrations applied
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** core
**Blocked reasons:** TC-010/011 need a guest; device was signed in as a QA user left by TC-004
**Plan:** ../../cases/Test_onboarding.md

## Results
9 Pass (TC-001..009), 0 Fail, 2 Blocked (TC-010, TC-011), 0 not run.

## Defects
None.

## Follow-ups
- TC-010/011: add ensure_guest() (in-app sign-out of the QA user) before first_run_to; TC-003 chip: read visible text not label 'Change language'; TC-005 progress: read text not progressbar value.

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| TC-001 | First run: Splash for 1.5 s, then Meet Irbis | Pass | script all green | — | [proof/TC-001/](proof/TC-001/) |
| TC-002 | Let's go ends onboarding; the next cold start goes straight to the tabs | Pass | script all green | — | [proof/TC-002/](proof/TC-002/) |
| TC-004 | I already have an account: log-in from Meet Irbis ends onboarding on the tabs | Pass | script all green | — | [proof/TC-004/](proof/TC-004/) |
| TC-006 | Language step: English preselected, a tap switches the app at once and Continue stays enabled | Pass | script all green | — | [proof/TC-006/](proof/TC-006/) |
| TC-007 | Experience: nothing preselected, Continue disabled until a pick, quiz card is static | Pass | script all green | — | [proof/TC-007/](proof/TC-007/) |
| TC-008 | Interests: nothing preselected, counter and Continue follow the selection | Pass | script all green | — | [proof/TC-008/](proof/TC-008/) |
| TC-009 | Companion: Bao reveal, Let's go goes to the tabs, Android back returns to Interests | Pass | script all green | — | [proof/TC-009/](proof/TC-009/) |
| TC-003 | Meet Irbis: Get started opens Language; the chip shows EN and switches the language | Pass | script bullets 1-3 red; crops OK | — | [proof/TC-003/](proof/TC-003/) |
| TC-005 | Steps 2–4 header: progress, back chevron, Android back | Pass | script bullet 1 red; crops OK | — | [proof/TC-005/](proof/TC-005/) |
| [TC-010](#tc-010) | Sign-up after onboarding: the choices land on the new account | Blocked | checkpoint failed | Checkpoint failed: device still signed in as an earlier QA user (left by TC-004), so Profile showed the account, not guest. Script setup gap (no in-app sign-out first); not executed on a guest. | [proof/TC-010/](proof/TC-010/) |
| [TC-011](#tc-011) | Log-in: the account's values win, the account language is applied | Blocked | checkpoint failed | Checkpoint failed: device still signed in as an earlier QA user (left by TC-004), so Profile showed the account, not guest. Script setup gap (no in-app sign-out first); not executed on a guest. | [proof/TC-011/](proof/TC-011/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

<a id="tc-010"></a>
### TC-010 · Blocked · Sign-up after onboarding: the choices land on the new account
**Group:** Core · **Priority:** P0 · **Env:** Android · auto (adb)
**Case:** Sign-up after onboarding: the choices land on the new account · [→ Test_onboarding.md](../../cases/Test_onboarding.md#tc-010--p0--sign-up-after-onboarding-the-choices-land-on-the-new-account)
**Reason:** Checkpoint failed: device still signed in as an earlier QA user (left by TC-004), so Profile showed the account, not guest. Script setup gap (no in-app sign-out first); not executed on a guest.
**Proof:** proof/TC-010/__pycache__, proof/TC-010/case.py, proof/TC-010/events.txt, proof/TC-010/video_steps.tsv

<a id="tc-011"></a>
### TC-011 · Blocked · Log-in: the account's values win, the account language is applied
**Group:** Core · **Priority:** P0 · **Env:** Android · auto (adb)
**Case:** Log-in: the account's values win, the account language is applied · [→ Test_onboarding.md](../../cases/Test_onboarding.md#tc-011--p0--log-in-the-accounts-values-win-the-account-language-is-applied)
**Reason:** Checkpoint failed: device still signed in as an earlier QA user (left by TC-004), so Profile showed the account, not guest. Script setup gap (no in-app sign-out first); not executed on a guest.
**Proof:** proof/TC-011/__pycache__, proof/TC-011/case.py, proof/TC-011/events.txt, proof/TC-011/video_steps.tsv


## Additional observations

## Follow-ups
