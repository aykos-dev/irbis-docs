# check-in

- Status: Approved (owner Q&A 2026-10-29)
- Surfaces: api | app
- Related ADRs: ADR-001 (guest-first), ADR-006 (demo accounts)
- Requirements: Product Overview § XP sources ("Real check-in at a place 40–120"), § Levels (verified check-ins),
  § Weekly chest · Screens: `design/canvas/Summit.dc.html`; `canvas-rules.md` :12 ("GPS check-in on site counts")

## Goal
On site, the explorer taps **Check in**. The phone's GPS proves they are at the place; the server grants XP by
difficulty once per place per month, counts it for level requirements and marks the place done on the monthly
path. A Summit celebration follows. Works offline (queued) and for guests (demo account on first sync).

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| POST | `/v1/check-ins` | user | `{ clientId (uuid), placeId, lat, lng, accuracyM, recordedAt }` | 201 `CheckInResultDto` (200 on a repeated `clientId`) | 404 `PLACE_NOT_FOUND`, 422 `CHECK_IN_TOO_FAR {distanceM, radiusM}`, 422 `LOCATION_INACCURATE`, 422 `CHECK_IN_TOO_OLD`, 400 `VALIDATION_FAILED` (future `recordedAt` > 2 min skew) |
| POST | `/v1/auth/demo` | public, throttled | `{ locale }` | 201 same as sign-up (tokens + me) | 429 `RATE_LIMITED`, 429 `DEMO_LIMIT` |
| POST | `/v1/me/secure` | user (demo only) | `{ username, password, acceptTerms }` | 200 `MeResponseDto` | 409 `NOT_DEMO`, 409 `USERNAME_TAKEN`, 400 `VALIDATION_FAILED` |

`CheckInResultDto = { id, placeId, recordedAt, counted, xp, levelUps, pathVisited }` · `PlaceDetailDto` gains
`checkInRadiusM` · `MeResponseDto` gains `isDemo`.

## Data model changes
Migration `check_in`:
- `CheckIn` (`check_ins`): id, userId → User (cascade), placeId → Place, `clientId` uuid, lat, lng, accuracyM,
  `recordedAt`, `month` char(7) (Tashkent month of recordedAt), `counted` bool, `xpAwarded` int, createdAt.
  Unique (userId, clientId). Partial unique (userId, placeId, month) WHERE counted (raw SQL in the migration).
- GameConfig `checkIn.config` = `{ xpByDifficulty: [40, 60, 80, 100, 120], radiusMByType: { peak: 300,
  waterfall: 300, cave: 200, lake: 1000, canyon: 1000, camping: 1000, trail: 1000 }, maxAccuracyM: 50,
  maxAgeHours: 72, demoPerIpPerDay: 5 }` (zod).
Migration `demo_accounts`: `User.passwordHash` nullable, `User.isDemo` bool default false.

## Acceptance criteria
- **AC1 — Verified on site.** A check-in is accepted only when the fix's `accuracyM` ≤ 50 and its haversine
  distance to the place ≤ the place type's radius (peak 300 m, waterfall 300 m, cave 200 m, lake / canyon /
  camping / trail 1 km; server config). Too far → 422 `CHECK_IN_TOO_FAR` with `distanceM` and `radiusM`; the app
  shows "You're {distance} away — get within {radius} to check in."
- **AC2 — XP by difficulty, once per place per month.** The first accepted check-in at a place in a Tashkent
  calendar month is `counted`: XP 40 / 60 / 80 / 100 / 120 for difficulty 1–5 (config, source `check_in`, refId =
  check-in id), a `check_in` level fact with the place difficulty, and `WeeklyPathService.recordVisit`. Later
  accepted check-ins at that place that month are stored with `counted: false`, `xp: 0`. No daily XP cap.
- **AC3 — Idempotent + time rules.** The same `clientId` returns the first result (200). `recordedAt` older than
  72 h → 422 `CHECK_IN_TOO_OLD`; more than 2 min in the future → 400. The month and the path month come from
  `recordedAt`, not the upload time.
- **AC4 — Where the button is.** Place screen and the active trip show **Check in** (testID `checkin.button`).
  Tapping takes one fix (accuracy ≤ 50 m, 10 s timeout, location permission flow as trip-plan). If the phone is
  outside `checkInRadiusM` it says so and stores nothing. "Not now" places still allow check-in (being there is a
  fact), but the button never says "Go there".
- **AC5 — Offline queue.** Offline, a passing fix is stored on the phone (max 20, oldest dropped) and the Summit
  screen opens with "Checked in · XP arrives when you're online". The queue sends in order when online (app
  start / foreground / reconnect); a 422 drops that item with one toast; 5xx/network keeps it.
- **AC6 — Guests (ADR-006).** A guest's check-in is queued the same way. On the first send, the app calls
  `POST /v1/auth/demo`, stores the tokens like a log-in, runs the guest merge, then sends the queue. The guest
  sees a toast "Your progress is saved as {username}". Max 5 demo accounts per IP per day (429 `DEMO_LIMIT`, the
  queue waits).
- **AC7 — Summit celebration.** After a sent check-in: confetti 1.2 s, mascot of the user's companion (fox art
  for now, placeholder for others), title by type — peak "Summit reached!", others "You made it!" — place name ·
  elevation, tile "+{xp} XP earned" (counted) or "Already counted this month" (not counted), Share (OS share
  sheet: "I checked in at {place} on Irbis!") and Continue (back). Level-up after a check-in goes to LevelUp first.
  League elevation and Badge tiles are not shown until those features exist.
- **AC8 — Demo account.** `/v1/me` returns `isDemo`. The account Profile shows the demo username and a **Secure
  your account** card → form (username, password, confirm, terms checkbox; sign-up rules) → `POST /v1/me/secure`. Log-in with a
  demo username fails like a wrong password. Sign out of a demo account asks first: "You'll lose {username}'s
  progress unless you secure it."

### QA events (app)
`check_in_sent { placeId, counted, xp, queued }` · `check_in_queued { placeId }` · `check_in_rejected { code }` ·
`demo_account_created {}` · `account_secured {}`

### testIDs (app)
`checkin.button`, `checkin.too-far`, `summit.screen`, `summit.title`, `summit.xp`, `summit.share`,
`summit.continue`, `summit.queued`, `profile.secure-card`, `secure.username`, `secure.password`,
`secure.confirm`, `secure.submit`

### Required UI states
- [ ] Loading (locating…), error + retry, offline (queued), permission denied (explain + Settings)
- [ ] Keyboard (secure form), safe areas, haptics (success on check-in), tokens only

## Media
- Summit mascot per companion: fox exists (`95f8b158…`); panda, marmot, ibex, bear, eagle, snow leopard summit
  poses placeholder (neutral pose) → prompts in `design/media/IMAGE-PROMPTS.md` § Check-in & streaks.
- Confetti: Reanimated (no Lottie).

## Out of scope
Guessed-place 2× XP (Bu qayer?), league elevation, badges, feed post from Summit, photo check-ins,
demo-account cleanup job, web admin view of check-ins.

## Assumptions
- Q1 (owner, 2026-10-29): radius per place type, server config.
- Q2: any time on site, no trip plan needed.
- Q3: XP + level count once per place per Tashkent month.
- Q4: offline queue, ≤ 72 h old.
- Q5: XP 40/60/80/100/120.
- Q6: Summit shows XP + week streak only (week tile added by `streaks`).
- Q7: title per type.
- Q8: guests: stored, demo account on first sync with a visible username + Secure your account (ADR-006).
- Q9 (owner, 2026-10-29): demo accounts accept the terms on Secure your account (termsAcceptedAt null until then).
- Q10 (owner, 2026-10-29): `isDemo` added to the /v1/me exact-keys test in auth-recovery e2e.
