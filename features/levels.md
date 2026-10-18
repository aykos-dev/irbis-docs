# levels

- Status: Approved (2026-10-18)
- Surfaces: api | app (web: no code change; admin user detail shows the real level from the api)
- Related ADRs: ADR-001 (guest-first: guests see Level 1, earning needs an account), ADR-002, ADR-003
- Requirements: Product Overview § Levels & companions (levels table), § XP, streaks, leagues & gems (XP sources),
  § Decisions ("XP numbers and level thresholds — decided later, after testing") ·
  Screens: `design/canvas/Level`, `LevelUp`, `Companions` · notes `n_lvlup` · `design/canvas-rules.md` (a) Progression,
  (b) 4–5
- Builds on: `auth` (User, `/v1/me`, guest-merge, admin users `level: null`), `places` (`difficulty`, `requiredLevel`,
  detail `viewer`), `onboarding` (companion art, `Motion`). Branch `feat/levels` stacks on `feat/conditions` (Q8).

## Goal
Every account has an XP total and a level L1–L7 with its companion. A level needs XP **and** safety lessons **and**
verified check-ins at the right difficulty (L7 also 3 verified spots); all numbers live in server config. The app
shows the Level screen (three requirement bars, next-companion silhouette), the Companions list, a level-up evolution
screen, and places above your level carry a lock. Lessons and check-ins don't exist yet: this feature builds the
ledger and counters they will feed, plus a QA-only grant to test every bar now (Q1).

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | /v1/levels | `@Public()` | — | `{ items: LevelDef[] }` (7, ascending) | — |
| GET | /v1/me/level | user | — | `MyLevel` | — |
| POST | /v1/me/level-ups/{id}/seen | user | — | 204 | LEVEL_UP_NOT_FOUND (404, also another user's) |
| POST | /v1/qa/levels/grant | user, only when `QA_TOOLS_ENABLED=true` | `{ xp?: 1–20000, lessons?: {tier: string}[] (≤50), checkIns?: {difficulty: 1–5}[] (≤50), verifiedSpots?: 0–10 }` | `MyLevel` | 404 NOT_FOUND when disabled; VALIDATION_FAILED |
| GET | /v1/me (existing) | user | — | + `level: 1–7`, `xpTotal: int` | — |
| GET | /v1/places/{id} (existing) | `@Public()` + optional token | — | `viewer.level` = account level (guest 1), `viewer.qualifies` | unchanged |
| GET | /v1/admin/users, /{id} (existing) | admin | — | `level` = real level (no longer null) | unchanged |

`LevelDef` = `{ level, xp, lessons: { kind: count|tier|all, tier: string|null, required }, checkIns: { required,
minDifficulty }, verifiedSpots: int, maxDifficulty: 1–5, newPlacesCount }` (L1 has all zeros).
`MyLevel` = `{ level, xpTotal, reachedAt, next: { level, xp: Progress, lessons: Progress & {kind, tier},
checkIns: Progress & {minDifficulty}, verifiedSpots: Progress | null } | null (L7), pendingLevelUps: { id, fromLevel,
toLevel, maxDifficulty, newPlacesCount }[] (oldest first) }`; `Progress` = `{ current, required }`.

## Data model changes
New migration `levels_init`.
- `GameConfig { key String @id, value Json, updatedAt }` — seeded keys `levels.table` (the 7 rows below) and
  `xp.dailyCaps` (`{ post: 5, game: 30, campfire: 30 }`). Read through a typed, zod-validated loader; cached ≤ 60 s.
- `enum XpSource { lesson check_in waypoint discoverer top_shots post game campfire qa_grant }`
- `XpEntry { id, userId, source, refId, amount Int, createdAt }` append-only, `@@unique([userId, source, refId])`.
- `enum LevelFactKind { lesson check_in verified_spot }` · `LevelFact { id, userId, kind, refId, tier String?,
  difficulty Int?, createdAt }` `@@unique([userId, kind, refId])` — what lessons / check-in / spots will write.
- `LevelUp { id, userId, fromLevel, toLevel, createdAt, seenAt? }` index `(userId, seenAt)`.
- `User` + `level Int @default(1)`, `xpTotal Int @default(0)`, `levelReachedAt DateTime @default(now())`.
- Removes env `LEVELS_START_LEVEL`. Adds env `QA_TOOLS_ENABLED` (default false; config refuses true when
  `NODE_ENV=production`).

Seed `levels.table` (doc values, Q3): L2 300 XP · lessons count 2 · 2 check-ins ≥ 1 · max diff 2; L3 1,000 · tier "2"
(6) · 5 ≥ 2 · 3; L4 2,500 · tier "3" (6) · 8 ≥ 3 · 3; L5 5,000 · tier "first-aid" (6) · 12 ≥ 3 · 4; L6 9,000 · tier
"5" (6) · 15 ≥ 4 · 4; L7 15,000 · all (36) · 25 ≥ 5 · 3 verified spots · 5. (Tier sizes are config until `lessons`.)

## Acceptance criteria
- **AC1** — Ledger: `LevelsService.award({userId, source, refId, amount})` writes one `XpEntry`; the same
  `(userId, source, refId)` again writes nothing and returns the first entry. Sources with a cap in `xp.dailyCaps` are
  trimmed to what is left of the cap for the current Asia/Tashkent day (0 left → no entry, `capped: true`).
  `xpTotal` always equals the sum of the user's entries. `recordFact({userId, kind, refId, tier?, difficulty?})` is
  idempotent the same way. No XP or threshold number exists in client code.
- **AC2** — Level engine: after every award/fact the user's next level N+1 is reached when `xpTotal ≥ xp`, the lesson
  gate is met (count: ≥ required lesson facts; tier: ≥ required facts with that tier; all: ≥ required total), check-in
  facts with `difficulty ≥ minDifficulty` ≥ required, and verified-spot facts ≥ `verifiedSpots`. It repeats until no
  level is met, writing one `LevelUp` per step and setting `levelReachedAt`. A level never goes down, even when config
  raises a threshold. Check-ins count lifetime, not since the last level (Q4).
- **AC3** — Endpoints: `GET /v1/levels` returns the 7 `LevelDef`s from config (`newPlacesCount` = places with
  `requiredLevel = level`); `GET /v1/me/level` returns `MyLevel` (`next` null at L7; bars use the next level's
  numbers); `seen` sets `seenAt` (idempotent; unknown or another user's id → 404 LEVEL_UP_NOT_FOUND); `/v1/me` and
  admin users carry the real `level`. The QA grant awards `qa_grant` XP and writes facts (random refIds) through AC1/AC2;
  it returns 404 when `QA_TOOLS_ENABLED` is not true.
- **AC4** — Difficulty locks, api: `GET /v1/places/{id}` resolves an optional bearer token: valid → `viewer.level` =
  the account level; no or invalid token → guest, level 1 (never 401). `qualifies = requiredLevel ≤ viewer.level`.
  `LEVELS_START_LEVEL` is gone.
- **AC5** — App Level screen (canvas `Level`, opened from the Profile companion badge and the Place level card,
  Q5): back → previous screen; level frame (shape + colour per level), companion art, "LEVEL N" pill, name,
  "{Animal} · since {Month YYYY}" (`reachedAt`); card "To reach Level N+1 · {Name}" with three rows — "Earn XP" ·
  lessons row (label by kind) · "Verified check-ins at difficulty {d}+" + note "GPS check-in on site counts; photos
  alone don't." — each "{current} / {required}" (thousands separator) and a bar filled `min(current/required, 1)`;
  L7 also "Verified spots". Next-companion card: silhouette, "Next companion", "{Name} · ???", "Unlocks {unlock}.".
  At L7: "You're a Snow Legend — the top level." card, no bars. Button "Continue learning" → Lessons tab. Guest (Q6):
  L1 Bao, bars "0 / {required}" from `/v1/levels`, and a card "Create an account to earn XP and level up" with Create
  account / Log in (AccGate flow) in place of the button. States: skeleton, error + retry, offline shows the last
  level from MMKV (`levels.lastMyLevel`) with the offline banner; nothing cached → offline message + retry.
- **AC6** — App Companions screen ("See all companions" on Level): 7 cards top-down, each with frame + art, "LEVEL N",
  difficulty boots (`maxDifficulty` of 5), name, "{Animal} · {trait}", requirements line from `LevelDef` (L1 "Where
  every explorer starts."), "Unlocks: {unlock}"; your current level is marked "You"; levels above yours show the art
  as a silhouette. Uses `/v1/levels` (cached; offline → cached or offline message).
- **AC7** — App LevelUp (canvas `LevelUp`, Q9–Q10): when `/v1/me/level` (fetched on app start, on foreground, and
  after the QA grant) has `pendingLevelUps`, the app opens LevelUp for the oldest one: placeholder evolution sequence
  3 s, skippable by tap after 1 s (old companion glows, backpack arcs across, white flash, new companion pops in;
  L3→L4 uses the fox-handing / ibex-catching art), success haptic; then "LEVEL UP!", "You're a {Name}", pill
  "{N} {Animal} · {trait}", "NEWLY UNLOCKED" with `maxDifficulty` boots and "{unlock} · {newPlacesCount} new places"
  (count 0 → no "· N new places"). Share → OS share sheet with "I'm now a {Name} on Irbis!" (text only). Continue →
  `seen`, then the next pending one or back to where the user was. A failed `seen` call is retried on the next fetch
  and never shows the same level-up twice in one session.
- **AC8** — App locks + profile + QA link: Profile companion badge shows the account's companion art + level colour
  (guest Bao L1) and opens Level. Place level card uses the real `viewer` (token sent when logged in) and opens Level.
  Explore cards with `requiredLevel` > your level (guest 1) show a lock + "Level N" chip. QA builds only:
  `irbis://debug/levels/grant?xp=&lessons=&tier=&checkins=&difficulty=&spots=` calls the grant, then refetches (LevelUp
  shows if earned); not registered in release builds.

### QA events (app, dev/staging builds)
- `level_viewed { level, guest }` · `companions_viewed { level }` · `levelup_shown { from, to }` ·
  `levelup_skipped { to, atMs }` · `levelup_continue { to }` · `levelup_share { to }` ·
  `level_grant { xp, lessons, checkIns, spots, ok }`

### testIDs (app)
`level.screen`, `level.frame`, `level.pill`, `level.name`, `level.since`, `level.req-xp`, `level.req-lessons`,
`level.req-checkins`, `level.req-spots`, `level.next-companion`, `level.max`, `level.continue`, `level.guest-cta`,
`level.guest-signup`, `level.guest-login`, `level.companions-link`, `level.retry`, `companions.screen`,
`companions.card.<n>`, `companions.you`, `levelup.screen`, `levelup.sequence`, `levelup.title`, `levelup.unlocked`,
`levelup.share`, `levelup.continue`, `profile.companion-badge`, `place.level-card`, `explore.card.<slug>.lock`

### Required UI states (every touched client)
- [x] Loading (skeleton on Level, Companions)
- [x] Empty (guest Level; L7 max)
- [x] Error (message + retry)
- [x] Offline (cached last level / levels, offline banner)
- [ ] Permissions denied — n/a
- [x] App: safe areas; success haptic on level-up; press states
- [x] Design tokens; level colours from `levelColors` (extend with dark/tint per the Companions board)

## Media
`design/media/levels/MEDIA.md`. Final (export from canvas, Q11): L2, L4–L7 neutral companions, fox handing over,
ibex catching. Placeholder (STATUS known issue, Q10): 10 handing/catching poses for the other transitions,
`levelup-evolution.json` Lottie (Reanimated sequence instead), backpack (onboarding placeholder).

## Waivers
- none

## Out of scope
- Lessons, check-ins, spots, waypoints, posts, games writing XP/facts (their features call `award` / `recordFact`).
- Guest-time XP merge (with `lessons`) · weekly path avatar entry (with `weekly-path`) · gear/trail-level locks.
- Admin XP editing or a config editor (Q12) · enforcing overnight / group-lead / verify privileges (later features).
- Share image card; the "Tier X lessons are open" line on LevelUp (until `lessons`).

## Assumptions
- Q1 (owner, 2026-10-18): build the engine (ledger, GameConfig, counters) + a QA-only grant to test bars and level-ups now.
- Q2 (owner, 2026-10-18): overnight trips unlock at L3 (doc + Companions); L4 copy = "scrambles and high passes".
- Q3 (owner, 2026-10-18): lesson gates are tier keys in config per level (L2 any 2; L3 "2"; L4 "3"; L5 "first-aid";
  L6 "5"; L7 all); the lessons feature defines the tiers.
- Q4 (owner, 2026-10-18): never down; several levels at once each get a LevelUp in turn; check-ins counted lifetime.
- Q5 (owner, 2026-10-18): Level opens from Profile badge + Place level card; add a Companions list screen.
- Q6 (owner, 2026-10-18): guest = L1 Bao, bars at 0, log-in CTA; places treat guests as Level 1.
- Q7 (owner, 2026-10-18): real level on Place (optional token) + lock chip on Explore; `LEVELS_START_LEVEL` removed.
- Q8 (owner, 2026-10-18): `feat/levels` stacks on `feat/conditions` in api and app; merge conditions first later.
- Q9 (owner, 2026-10-18): LevelUp from a server pending queue, live "N new places", no lessons line yet, text share.
- Q10 (owner, 2026-10-18): evolution ships as a labelled Reanimated placeholder; poses + Lottie later.
- Q11 (owner, 2026-10-18): canvas companion SVGs are final; export into the app.
- Q12 (owner, 2026-10-18): admin shows the real level only; no XP adjust, no web code change.

## Open questions
- none
