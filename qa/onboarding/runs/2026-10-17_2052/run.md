# Run 2026-10-17_2052 — onboarding
**Status:** closed
**Build:** uz.irbis.app.dev 1.0-dev (1) — irbis-app feat/onboarding 421295e (installed)
**Backend:** irbis-api feat/onboarding local
**Device:** sdk_gphone64_arm64 (Android 15), emulating the phone (density 450, font 1.15)
**Accounts:** see Test data; phone numbers masked
**Tester:** Claude (auto) + owner (manual)
**Scope:** full
**Blocked reasons:** —
**Plan:** ../../cases/Test_onboarding.md

## Results
35 cases: 29 pass (19 TC without TC-019; STD-DARK x5, STD-OFFLINE x5) / 1 fail (STD-TEXT@welcome) / 4 blocked (STD-TEXT@language, experience, interests, companion) / 1 not run (TC-019 haptic, manual).
Script fixes in this run: `before_case()` now ends every case as a guest (TC-004, TC-012, TC-013, TC-018 were red from a leftover QA sign-in); TC-013 relaunches after the language reset; standards openers keep the language and reach later steps at 2.0 via a 1.15 walk.

## Defects
- [D2](../../bugs/D2_welcome_font2/D2_welcome_font2.md) · High · Meet Irbis CTAs unreachable at font 2.0
- [D3](../../bugs/D3_font_change_restarts/D3_font_change_restarts.md) · Low · font change mid-flow restarts at Meet Irbis

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|
| TC-016 | Experience tiles show their art and 1 / 2 / 4 boots | Pass | crop reviewed | — | [proof/TC-016/](proof/TC-016/) |
| [TC-019](#tc-019) | Reveal animation and haptic on entering Companion | Not run | — | Animation progresses t0/0.6/1.2 s (backpack to Bao, confetti, settles) per crops; haptic is manual on the phone, no proof possible on the emulator. | [proof/TC-019/](proof/TC-019/) |
| [STD-TEXT@welcome](#std-text@welcome) | Copy is translated and layout survives long text — welcome | Fail | en@2.0 fail | — | [proof/STD-TEXT@welcome/](proof/STD-TEXT@welcome/) |
| [STD-TEXT@language](#std-text@language) | Copy is translated and layout survives long text — language | Blocked | — | en@2.0 cannot be reached: Meet Irbis buttons are off-screen at 2.0 (D2) and a font change mid-flow restarts onboarding at Meet Irbis (D3). ru/uz crops fit; the only 'untranslated' text is the English endonym. | [proof/STD-TEXT@language/](proof/STD-TEXT@language/) |
| [STD-TEXT@experience](#std-text@experience) | Copy is translated and layout survives long text — experience | Blocked | — | en@2.0 cannot be reached (D2, D3). | [proof/STD-TEXT@experience/](proof/STD-TEXT@experience/) |
| [STD-TEXT@interests](#std-text@interests) | Copy is translated and layout survives long text — interests | Blocked | — | en@2.0 cannot be reached (D2, D3). | [proof/STD-TEXT@interests/](proof/STD-TEXT@interests/) |
| [STD-TEXT@companion](#std-text@companion) | Copy is translated and layout survives long text — companion | Blocked | — | en@2.0 cannot be reached (D2, D3). | [proof/STD-TEXT@companion/](proof/STD-TEXT@companion/) |

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

<a id="tc-019"></a>
### TC-019 · Not run · Reveal animation and haptic on entering Companion
**Group:** Supplementary · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Reveal animation and haptic on entering Companion · [→ Test_onboarding.md](../../cases/Test_onboarding.md#tc-019--p2--reveal-animation-and-haptic-on-entering-companion)
**Reason:** Animation progresses t0/0.6/1.2 s (backpack to Bao, confetti, settles) per crops; haptic is manual on the phone, no proof possible on the emulator.
**Proof:** proof/TC-019/1_t0.png, proof/TC-019/2_t06.png, proof/TC-019/3_t12.png, proof/TC-019/__pycache__, proof/TC-019/case.py, proof/TC-019/events.txt, proof/TC-019/video_steps.tsv

<a id="std-text@welcome"></a>
### STD-TEXT@welcome · Fail · Copy is translated and layout survives long text — welcome
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — welcome · [→ Test_onboarding.md](../../cases/Test_onboarding.md#std-textwelcome--p2--copy-is-translated-and-layout-survives-long-text)
**Done:** 1. ru, font 1.15 — open the screen → 2. uz, font 1.15 — open the screen → 3. en, font 2.0 — open the screen
**Expected** (source: —):
1. No English catalog string left on screen in Russian or Uzbek — UI tree
2. Nothing clipped or overflowing its container in any of the three — one composite crop (human)
**Actual:**
1. ✅ untranslated: {'ru': [], 'uz': []} — no proof
2. — judge _composite.png: ru · uz · en@2.0 side by side — proof/STD-TEXT@welcome/ru_font1.15.png, proof/STD-TEXT@welcome/uz_font1.15.png, proof/STD-TEXT@welcome/en_font2.0.png
**Conclusion:** ru and uz fit; at font 2.0 Get started and I already have an account are pushed off-screen, not in the UI tree and the screen does not scroll. See D2.

<a id="std-text@language"></a>
### STD-TEXT@language · Blocked · Copy is translated and layout survives long text — language
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — language · [→ Test_onboarding.md](../../cases/Test_onboarding.md#std-textlanguage--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** en@2.0 cannot be reached: Meet Irbis buttons are off-screen at 2.0 (D2) and a font change mid-flow restarts onboarding at Meet Irbis (D3). ru/uz crops fit; the only 'untranslated' text is the English endonym.
**Proof:** proof/STD-TEXT@language/__pycache__, proof/STD-TEXT@language/case.py, proof/STD-TEXT@language/en_font2.0.png, proof/STD-TEXT@language/events.txt, proof/STD-TEXT@language/ru_font1.15.png, proof/STD-TEXT@language/uz_font1.15.png, proof/STD-TEXT@language/video_steps.tsv

<a id="std-text@experience"></a>
### STD-TEXT@experience · Blocked · Copy is translated and layout survives long text — experience
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — experience · [→ Test_onboarding.md](../../cases/Test_onboarding.md#std-textexperience--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** en@2.0 cannot be reached (D2, D3).
**Proof:** proof/STD-TEXT@experience/__pycache__, proof/STD-TEXT@experience/case.py, proof/STD-TEXT@experience/events.txt, proof/STD-TEXT@experience/ru_font1.15.png, proof/STD-TEXT@experience/uz_font1.15.png, proof/STD-TEXT@experience/video_steps.tsv

<a id="std-text@interests"></a>
### STD-TEXT@interests · Blocked · Copy is translated and layout survives long text — interests
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — interests · [→ Test_onboarding.md](../../cases/Test_onboarding.md#std-textinterests--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** en@2.0 cannot be reached (D2, D3).
**Proof:** proof/STD-TEXT@interests/__pycache__, proof/STD-TEXT@interests/case.py, proof/STD-TEXT@interests/events.txt, proof/STD-TEXT@interests/ru_font1.15.png, proof/STD-TEXT@interests/uz_font1.15.png, proof/STD-TEXT@interests/video_steps.tsv

<a id="std-text@companion"></a>
### STD-TEXT@companion · Blocked · Copy is translated and layout survives long text — companion
**Group:** Standards · **Priority:** P2 · **Env:** Android · auto (adb)
**Case:** Copy is translated and layout survives long text — companion · [→ Test_onboarding.md](../../cases/Test_onboarding.md#std-textcompanion--p2--copy-is-translated-and-layout-survives-long-text)
**Reason:** en@2.0 cannot be reached (D2, D3).
**Proof:** proof/STD-TEXT@companion/__pycache__, proof/STD-TEXT@companion/case.py, proof/STD-TEXT@companion/events.txt, proof/STD-TEXT@companion/ru_font1.15.png, proof/STD-TEXT@companion/uz_font1.15.png, proof/STD-TEXT@companion/video_steps.tsv


## Additional observations

## Follow-ups
- Owner: haptics on Companion (TC-019 bullet 2); first-run language preselect for uz/ru device locales.
