# Brief streaks-1-irbis-api — flame, boot, freezes, GET /v1/me/streaks

- Spec: features/streaks.md · ACs: AC1, AC2, AC4, AC5 (api) — AC3 shield is brief 2 (leave a seam: a
  `isWeekShielded(userId, monday)` method returning false for now)
- Repo / branch: irbis-api · `feat/streaks` (create from `feat/check-in`)
- Depends on: check-in-1/2-irbis-api

## Files
- Touch: `src/features/streaks/` (new) · `prisma/schema.prisma` + migration `streaks` · game-config schema/service/seed
  (`streaks.config = { freezesPerMonth: 2 }`) · `src/features/lessons/lessons.service.ts` and
  `src/features/check-in/check-in.service.ts` (call the streak recorder) · lessons guest-merge handler (merged lessons
  record days)
- Read for patterns: `src/lib/dates` (Tashkent day/week/month), levels service (idempotent writes), `/v1/me/level` controller

## Behaviour
- Tables: `ActivityDay` (userId, day date, lessons int, checkIns int; PK (userId, day)), `StreakState` (userId PK,
  flameCount, flameLastDay date?, bootCount, bootLastWeek date? (Monday), evaluatedThrough date?, updatedAt),
  `StreakFreeze` (id, userId, kind flame|boot, coversDate date, month char(7); unique (userId, kind, coversDate)).
- `StreaksService.recordActivity(userId, kind: 'lesson'|'check_in', at)` upserts the Tashkent day (+1 to the
  counter), then evaluates. Called after lesson completion (first and practice) and after every accepted check-in
  (counted or not) with `recordedAt`. Must never fail the caller's request (log + continue).
- Evaluation (pure function + persisted state, idempotent, lazy on read and on record):
  - Flame: walk Tashkent days after `flameLastDay` up to yesterday. A day without activity uses a freeze if the
    month (of that day) has < freezesPerMonth freezes, else flame = 0. A day with activity +1. Today with activity
    +1 once. Late/backdated activity (queued check-ins) within the already-evaluated window: recompute from
    ActivityDay rows for the last 60 days (simplest correct approach is fine).
  - Boot: same per Monday–Sunday week with ≥ 1 check-in; missed past week → `isWeekShielded` true keeps the run
    (adds nothing); else a freeze from the shared monthly pool (month of that Monday); else 0.
  - Freezes are one pool per Tashkent month across both kinds.
- `GET /v1/me/streaks` → `StreaksDto { today, flame { count, doneToday, atRisk }, boot { count, doneThisWeek,
  shieldedLastWeek }, freezes { left, perMonth, usedThisMonth [{ kind, date }] } }`. operationId `meStreaks`.

## Done when
- [ ] unit (pure evaluator): consecutive days, gap with freeze, gap without freeze → 0, month boundary resets pool,
  boot week run, shared pool across kinds, backdated check-in fills a past day
- [ ] e2e: lesson today → flame 1 doneToday; check-in → boot 1; GET for a fresh user → zeros + 2 freezes
- [ ] `npm run check` green, openapi exported, commits on `feat/streaks`
