# onboarding

- Status: Approved (owner, 2026-10-17)
- Surfaces: app | api (no web)
- Related ADRs: ADR-001 (guest-first, guest merge)
- Requirements: Product Overview § How the app works / First run, § Accounts · Screens: `design/canvas/Splash`,
  `Onb1Welcome`, `Onb2Language`, `Onb3Experience`, `Onb4Interests`, `Onb5Companion`; notes `n_onb1`, `n_onb2`,
  `n_onb5` in `canvas.json`

## Goal
On first launch a new user meets Irbis, picks a language, their hiking experience and interests, and meets their
starting companion (Bao the panda cub, Level 1 Wanderer) — without an account. The choices stay on the phone and move
into the account on sign-up; on log-in the account's saved choices win.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| POST | /v1/me/guest-merge (existing) | user | `onboarding` becomes typed: `{ experience?: Experience, interests?: Interest[] }` | `{ merged, skipped }` | VALIDATION_FAILED (unknown enum value, duplicate or >5 interests) |
| GET | /v1/me (existing) | user | — | + `experience: Experience \| null`, `interests: Interest[]` | — |

`Experience` = `beginner | weekend | experienced`; `Interest` = `peaks | caves | lakes | camping | trails`.

## Data model changes
`User.experience Experience?` (new enum), `User.interests Interest[] @default([])` (new enum array).
New migration `onboarding_profile`. Merge rule (Q8): guest-merge never overwrites a value the account already has —
`experience` only if null, `interests` only if empty, `locale` is no longer overwritten on merge (set at sign-up).

## Acceptance criteria
- **AC1** — First run: Splash (teal, Irbis, "irbis", "Explore. Learn. Come back safe.") shows for 1.5 s, then Meet
  Irbis. Once onboarding ends (Let's go!, ✕, or log-in from Onb1) the flag `onboarding.done` is saved and every later
  cold start goes straight to the tabs with no in-app splash. A user who is already signed in at launch skips
  onboarding and the flag is set. (A reinstall shows it again.)
- **AC2** — Meet Irbis (Onb1): bubble, title, body per canvas. "Get started" → Language. "I already have an account"
  → Log in; a successful log-in ends onboarding on the tabs; closing Log in returns to Onb1. The top-right chip shows
  the current language code (UZ/RU/EN) and opens the language sheet; a pick switches the app language at once.
- **AC3** — Steps 2–4 header: back chevron (and Android back) → previous step; ✕ → ends onboarding on the tabs,
  keeping the current language and saving no experience/interests; progress "Step N of 4" (Language 1, Experience 2,
  Interests 3). Language (Onb2): UZ/RU/EN list, the current app language preselected (first run: device locale
  uz/ru/en, else en); tapping one switches and saves the language immediately (Irbis nods) and it stays after ✕.
  Continue is always enabled.
- **AC4** — Experience (Onb3): Beginner / Weekend hiker / Experienced tiles (trail / lake / peak art, 1 / 2 / 4
  boots), none preselected; Continue disabled until one is picked. The orange card shows the canvas text only (not
  tappable; the quiz is feature `onboarding-quiz`).
- **AC5** — Interests (Onb4): Peaks, Caves, Lakes, Camping, Trails toggle tiles, none preselected; counter
  "N selected · Your weekly path mixes these with safe options for the season." (plural-aware in ru/uz); Continue
  disabled at 0 selected.
- **AC6** — Companion reveal (Onb5): no header; "Meet Bao, your panda cub!", level pill "1 Wanderer · clumsy & cozy",
  six locked companion silhouettes; on entry a reveal animation runs (placeholder until Lottie: backpack pop, panda
  scale-in, 0.8 s confetti) with a success haptic. "Let's go!" → tabs. Android back on Onb5 → Interests.
- **AC7** — Choices (experience, interests) are stored on the phone as guest data. On sign-up they are sent in
  guest-merge `onboarding` and saved on the new account; `GET /v1/me` returns them. Unknown values are rejected (400).
- **AC8** — Log-in (Q8, account wins): guest-merge fills only empty account fields and never overwrites `locale`,
  `experience` or non-empty `interests`; after log-in the app switches to the account's `locale`.

### QA events (app, dev/staging builds)
- `onboarding_step { step: splash|welcome|language|experience|interests|companion }`
- `onboarding_language { locale }` · `onboarding_end { via: finish|close|login, experience?, interestsCount }`
- existing `guest_merged { keys }` (from auth) proves AC7/AC8 merge.

### testIDs (app)
`onboarding.splash`, `onboarding.welcome`, `onboarding.get-started`, `onboarding.have-account`,
`onboarding.lang-chip`, `onboarding.back`, `onboarding.close`, `onboarding.progress`,
`onboarding.lang-{uz|ru|en}`, `onboarding.exp-{beginner|weekend|experienced}`,
`onboarding.interest-{peaks|caves|lakes|camping|trails}`, `onboarding.interests-count`, `onboarding.continue`,
`onboarding.companion`, `onboarding.lets-go`.

### Required UI states (every touched client)
- [x] Loading — none (all local); Splash covers startup
- [x] Empty — n/a; Continue-disabled states in AC4/AC5
- [x] Error / Offline — onboarding is fully offline; merge errors are handled by auth's existing merge path
- [ ] App: safe areas; haptics (selection on tap, success on Onb5); press states; long ru/uz text wraps, never truncates
- [ ] Light + dark via design tokens (canvas has light only); `src/shared/components` primitives only

## Media
From `design/media/onboarding/MEDIA.md`: canvas SVGs final (exported into the app); backpack and native launch splash
placeholders; Lottie files `irbis-wave`, `irbis-nod`, `irbis-clap`, `onb5-reveal` placeholders (static SVG / simple
Reanimated) until the owner provides them — all tracked in STATUS.md Known issues.

## Waivers
- none

## Out of scope
- Experienced-user safety quiz → feature `onboarding-quiz` after `lessons`, with a new ADR on what passing grants.
- Editing experience/interests later (Profile/Settings); `PUT /v1/me/onboarding`, `PATCH /v1/me`.
- Using the choices (weekly path, level) — later features. Web admin display of the choices.
- Final Lottie animations and final backpack / native splash art.

## Assumptions
- Q1 (owner, 2026-10-17): Finish auth QA + merge first; onboarding starts from `main` afterwards. (Auth merged with QA
  gaps by owner decision, 2026-10-17.)
- Q2 (owner, 2026-10-17): Quiz wanted. Q5 (owner, 2026-10-17): split it into its own feature `onboarding-quiz`, after
  `lessons`, with a new ADR; onboarding shows the Onb3 card text only.
- Q3 (owner, 2026-10-17): "I already have an account" → Log in; on success onboarding ends. ✕ on steps 2–4 ends
  onboarding with no experience/interests, lands on tabs. Neither re-shows onboarding.
- Q4 (owner, 2026-10-17): Experience and ≥1 interest required; nothing preselected; language preselected from the
  device locale (uz/ru/en, else en). Canvas selections are demo state.
- Q6 (owner, 2026-10-17): Header has both: back chevron → previous step, ✕ → end.
- Q7 (owner, 2026-10-17): A tapped language is saved immediately and stays after ✕.
- Q8 (owner, 2026-10-17): Account wins on log-in; device choices fill only empty account fields; sign-up takes the
  device choices; fix auth's locale merge accordingly.
- Q9 (owner, 2026-10-17): Motion via Lottie (`lottie-react-native`, approved).
- Q10 (owner, 2026-10-17): Canvas SVGs final; backpack + native splash placeholders.
- Q11 (owner, 2026-10-17): Splash on first run only.
- Q12 (owner, 2026-10-17): Onb1 chip opens the language sheet.
- Q13 (owner, 2026-10-17): Lottie files: ship placeholders now, swap later.
- Copy: canvas is English only; ru/uz copy is written in the briefs for owner review.

## Open questions
- none
