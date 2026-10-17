# onboarding

- Status: Draft — paused before spec (owner: finish auth QA first, 2026-10-17)
- Surfaces: app | api
- Related ADRs: ADR-001 (guest-first, guest merge)
- Requirements: Product Overview § First run · Screens: `design/canvas/Splash`, `Onb1Welcome`, `Onb2Language`,
  `Onb3Experience`, `Onb4Interests`, `Onb5Companion`; notes `n_onb1`, `n_onb2`, `n_onb5` in `canvas.json`

## Builds on (from auth, feat/auth)
- App: `src/shared/guest/guestStore.ts` `registerGuestItem` (onboarding keys merge); tab shell; Log in screen.
- API: `POST /v1/me/guest-merge` already accepts `onboarding` (Record); `GuestMergeRegistry` waits for an
  onboarding handler (`src/features/auth/guest-merge/`).
- App packages already present: reanimated, react-native-svg, haptic-feedback, localize, mmkv.

## Assumptions (answers so far)
- Q1 (owner, 2026-10-17): Finish auth QA + merge first; onboarding starts from `main` afterwards.
- Q2 (owner, 2026-10-17): Build the experienced-user safety quiz now. Not defined anywhere (doc/canvas) —
  needs its rules (questions source, pass mark, retries, what it unlocks vs. ADR/level gates) and likely a
  split into `onboarding` + `onboarding-quiz` to stay within ~8 ACs. Ask next session.
- Q3 (owner, 2026-10-17): "I already have an account" → Log in; on success onboarding ends (account's saved
  choices kept, else defaults). ✕ on steps 2–4 ends onboarding with the device language and no
  experience/interests, lands on tabs. Neither re-shows onboarding.
- Q4 (owner, 2026-10-17): Experience and ≥1 interest required (Continue disabled); nothing preselected;
  language preselected from device locale (uz/ru/en, else en).

## Still to ask (next session)
- Quiz rules (Q2 follow-up) and the split.
- Media: which canvas SVGs are final; mascot motion via Reanimated on static SVGs vs Lottie (new package);
  backpack + native splash placeholders. List: `design/media/onboarding/MEDIA.md`.
