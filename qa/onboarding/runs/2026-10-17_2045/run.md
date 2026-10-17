# Run 2026-10-17_2045 — onboarding
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — irbis-app feat/onboarding 5299146
**Backend:** irbis-api feat/onboarding
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** rerun TC-003 TC-005 TC-010 TC-011 (script fixes)
**Blocked reasons:** —
**Plan:** ../../cases/Test_onboarding.md

## Results
2 Pass (TC-003, TC-005), 2 Fail (TC-010, TC-011), 0 blocked, 0 not run.

## Defects
- onboarding/D1 · Medium · merge skipped, no guest_merge_result (TC-010, TC-011)

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| TC-003 | Meet Irbis: Get started opens Language; the chip shows EN and switches the language | Pass | 4/4 green | — | [proof/TC-003/](proof/TC-003/) |
| TC-005 | Steps 2–4 header: progress, back chevron, Android back | Pass | 3/3 green | — | [proof/TC-005/](proof/TC-005/) |
| [TC-010](#tc-010) | Sign-up after onboarding: the choices land on the new account | Fail | 2 fail | ❌ 1, 2 | [proof/TC-010/](proof/TC-010/) |
| [TC-011](#tc-011) | Log-in: the account's values win, the account language is applied | Fail | bullet 1 fail | ❌ 1 | [proof/TC-011/](proof/TC-011/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

<a id="tc-010"></a>
### TC-010 · Fail · Sign-up after onboarding: the choices land on the new account
**Group:** Core · **Priority:** P0 · **Env:** Android · auto (adb)
**Case:** Sign-up after onboarding: the choices land on the new account · [→ Test_onboarding.md](../../cases/Test_onboarding.md#tc-010--p0--sign-up-after-onboarding-the-choices-land-on-the-new-account)
**Done:** First run (reset link), app language English, guest → 3. Sign up
**Expected** (source: —):
1. Event guest_merge_result after sign-up whose merged includes onboarding — QA events
2. DB: users.experience = weekend and interests = {peaks,lakes} for the new user — SQL on the LOCAL dev DB
**Actual:**
1. ❌ event None — proof/TC-010/1_account.png
2. ❌ db experience=null, interests={} — no proof
**Conclusion:** No guest_merge_result after sign-up; DB experience null, interests empty. See D1.

<a id="tc-011"></a>
### TC-011 · Fail · Log-in: the account's values win, the account language is applied
**Group:** Core · **Priority:** P0 · **Env:** Android · auto (adb)
**Case:** Log-in: the account's values win, the account language is applied · [→ Test_onboarding.md](../../cases/Test_onboarding.md#tc-011--p0--log-in-the-accounts-values-win-the-account-language-is-applied)
**Done:** First run (reset link), app language English, guest → 3. Log in
**Expected** (source: —):
1. Event guest_merge_result whose skipped names onboarding / locale (nothing overwritten) — QA events
2. Event locale_applied {locale: ru} and the tab labels turn Russian (nav.tab-profile content-desc "Профиль") — QA events + UI tree
3. DB: experience still beginner, interests still {caves}, locale still ru — SQL on the LOCAL dev DB
**Actual:**
1. ❌ event None — no proof
2. ✅ locale_applied {'locale': 'ru'}, tab 'Профиль' — proof/TC-011/1_tabs_ru.png
3. ✅ db beginner, {caves}, ru — no proof
**Conclusion:** No guest_merge_result on log-in (locale_applied ru and DB unchanged OK). See D1.


## Additional observations

## Follow-ups
- Owner: confirm whether guest.merged should reset on sign-out (D1).
