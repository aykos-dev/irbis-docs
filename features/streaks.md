# streaks

- Status: Approved (owner Q&A 2026-10-29)
- Surfaces: api | app
- Related ADRs: ADR-004 (jobs, weather), ADR-006 (demo accounts)
- Requirements: Product Overview § Streaks, § Retention, § Notification rules · Screens: `design/canvas/Home.dc.html`
  (flame / boot / shield in the header), `Summit.dc.html` ("5 Week streak"), `LessonsHub.dc.html` (streak line)

## Goal
Two streaks keep explorers coming back without guilt: the daily **flame** (a lesson or a check-in each day) and
the weekly **boot** (a check-in each week). Bad weather never breaks the boot (weather shield), and 2 free
freezes a month cover a missed day or week.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | `/v1/me/streaks` | user | — | `StreaksDto` | — |

`StreaksDto = { today: "YYYY-MM-DD", flame: { count, doneToday, atRisk }, boot: { count, doneThisWeek,
shieldedLastWeek }, freezes: { left, perMonth, usedThisMonth: [{ kind: "flame"|"boot", date }] } }`

## Data model changes
Migration `streaks`:
- `ActivityDay` (`activity_days`): userId, `day` date (Tashkent), `lessons` int, `checkIns` int. PK (userId, day).
- `StreakState` (`streak_states`): userId PK, flameCount, flameLastDay, bootCount, bootLastWeek (Monday date),
  `evaluatedThrough` date, updatedAt.
- `StreakFreeze` (`streak_freezes`): id, userId, kind, `coversDate` (day or week Monday), month char(7). Unique
  (userId, kind, coversDate).
- `WeekendCondition` (`weekend_conditions`): placeId, `date`, status. PK (placeId, date).
- GameConfig `streaks.config` = `{ freezesPerMonth: 2 }`.

## Acceptance criteria
- **AC1 — Flame.** A Tashkent day counts when the user finished ≥ 1 lesson (first or practice) or made ≥ 1 accepted
  check-in that day (counted or not). The flame count is the run of consecutive counted days ending today or
  yesterday; `doneToday` says if today counts; `atRisk` = not done today and count > 0.
- **AC2 — Boot.** A Monday–Sunday Tashkent week counts with ≥ 1 accepted check-in. The boot count is the run of
  consecutive counted weeks ending this week or last week.
- **AC3 — Weather shield.** A past week without a check-in is shielded (keeps the boot run, adds nothing) when on
  both its Saturday and Sunday every place on the user's path that month — and every place of a trip the user
  had planned for that weekend — was `not_now` or `seasonal_lock`. A job records each path / planned place's
  status at 12:00 Tashkent on Sat and Sun (`WeekendCondition`). `shieldedLastWeek` drives the shield badge.
- **AC4 — Freezes.** 2 per Tashkent month (config), shared by flame and boot, used automatically: a missed day
  (flame) or an unshielded missed week (boot) uses one if left, else that streak resets to 0. Shield is used
  before a freeze. Evaluation is lazy (on read and on each new activity), idempotent, Tashkent dates only.
- **AC5 — Feeding.** Lesson completion and accepted check-ins record the activity day (from `completedAt` /
  `recordedAt`). Guest lessons merged into an account (sign-up, log-in, demo) count on their own days.
- **AC6 — Path header.** For accounts (real and demo) the Path header shows flame (count, orange when done today,
  grey when at risk) and boot (count) next to XP, as on Home; a blue shield badge on the boot when
  `shieldedLastWeek`. Guests see no streaks. Tap → Streak sheet: both counts, "Today: done / not yet", "This week:
  checked in / not yet", freezes "{left} of {perMonth} left this month", one line on the weather shield; Irbis
  excited (all done), sleepy (at risk), sad (count 0 after a break).
- **AC7 — Elsewhere.** Summit shows the "{n} Week streak" tile (boot count after that check-in). The Lessons hub
  shows "One more 3-minute lesson keeps your {n}-day streak." when the flame is at risk. The account Profile
  shows a streak row (flame + boot). Data refreshes after lessons, check-ins and on app foreground.

### QA events (app)
`streaks_seen { flame, boot }` · `streak_sheet_open {}`

### testIDs (app)
`path.streak.flame`, `path.streak.boot`, `path.streak.shield`, `streak.sheet`, `streak.freezes`,
`summit.week-streak`, `lessons.streak-line`, `profile.streaks`

### Required UI states
- [ ] Loading (skeleton chips), error (hide chips, no toast), offline (last cached values)
- [ ] Tokens only, a11y labels ("12-day streak", "4-week explorer streak, protected by weather shield")

## Media
Flame, boot, shield glyphs: inline icons (exist). Irbis excited / sleepy / sad poses: existing mascot set,
placeholders where missing → `design/media/IMAGE-PROMPTS.md` § Check-in & streaks.

## Out of scope
Gems, paid freezes, streak milestone rewards, reminder pushes (toggle exists in profile settings), Bu qayer? days,
friends' streaks.

## Assumptions
- Q1 (owner, 2026-10-29): flame = 1 lesson or 1 check-in a day; daily goal 3 stays separate (resolves conflict
  "Daily goal 2/3 vs one more lesson").
- Q2: shield = weekend red at all path places (+ planned trip places).
- Q3: 2 free freezes / month, flame + boot (one shared pool — assumed), until `gems`.
- Q4: no flame for guests without an account.
