# Brief check-in-1-irbis-api — verified check-in endpoint

- Spec: features/check-in.md · ACs: AC1, AC2, AC3 (api side)
- Repo / branch: irbis-api · `feat/check-in` (create from `fix/open-bugs-1029`)
- Depends on: none

## Files
- Touch: `src/features/check-in/` (new: module, controller, service, repository, errors, dto, `check-in.rules.ts`) ·
  `src/app.module.ts` · `prisma/schema.prisma` + new migration `check_in` · `src/features/levels/game-config.schema.ts`
  + `game-config.service.ts` (new getter `checkInConfig`) · `prisma/seed/game-config.data.ts` + seed keys ·
  place detail DTO + mapper in `src/features/places/` (add `checkInRadiusM`)
- Read for patterns: `src/features/trip-plan/trip-safety.service.ts` `checkInWaypoint` + `waypoint.rules.ts`
  (fix rules, skew, insert/retry, award) · `src/features/levels/levels.service.ts` `award` / `recordFact` ·
  `src/features/weekly-path/weekly-path.service.ts` `recordVisit` · `src/features/places/place.rules.ts` `haversineM` ·
  `src/lib/dates` (Tashkent)

## Behaviour
- GameConfig `checkIn.config` (zod): `{ xpByDifficulty: [40,60,80,100,120], radiusMByType: { peak: 300,
  waterfall: 300, cave: 200, lake: 1000, canyon: 1000, camping: 1000, trail: 1000 }, maxAccuracyM: 50,
  maxAgeHours: 72, demoPerIpPerDay: 5 }` (demoPerIpPerDay is used by brief 2; seed it now).
- Model `CheckIn` (`check_ins`): id uuid7, userId → User (cascade), placeId → Place, clientId uuid, lat, lng,
  accuracyM, recordedAt timestamptz(3), month char(7), counted bool, xpAwarded int, createdAt. Unique (userId,
  clientId). Partial unique index (user_id, place_id, month) WHERE counted — raw SQL inside the new migration.
- `POST /v1/check-ins` (user) body `{ clientId uuid, placeId uuid, lat [-90..90], lng [-180..180], accuracyM ≥ 0,
  recordedAt ISO }`:
  1. Existing (userId, clientId) → return its stored result, 200 (no new XP).
  2. recordedAt > now + 2 min → 400 VALIDATION_FAILED; recordedAt < now − 72 h → 422 CHECK_IN_TOO_OLD.
  3. Place missing → 404 PLACE_NOT_FOUND. accuracyM > 50 → 422 LOCATION_INACCURATE.
  4. distance > radius for place.type → 422 CHECK_IN_TOO_FAR with `details { distanceM (rounded), radiusM }`.
  5. month = Tashkent `YYYY-MM` of recordedAt. In one transaction: insert; if no counted row for (user, place,
     month) → counted = true, xp = xpByDifficulty[difficulty−1]. Race on the partial unique → insert as not counted.
  6. Counted: `LevelsService.award({ userId, source: 'check_in', refId: checkIn.id, amount: xp })`,
     `recordFact({ kind: 'check_in', refId: checkIn.id, difficulty })`, `WeeklyPathService.recordVisit(userId,
     placeId, recordedAt)`; store xpAwarded = granted amount.
  Response 201 `CheckInResultDto { id, placeId, recordedAt, counted, xp, levelUps, pathVisited }` (levelUps as in
  lessons completion). operationId `checkInsCreate`. Error codes in `check-in.errors.ts`.
- Place detail (and list item if it has the type) gains `checkInRadiusM` from config.
- Don't log lat/lng.

## Done when
- [ ] unit: rules (accuracy, radius per type, age, future), XP table, counted vs repeat-in-month, next-month counts again
- [ ] e2e: 201 counted (+XP, fact, path visit), same month repeat → counted false xp 0, same clientId → 200 same
  body, 422 too far (details), 404; `npm run check` green
- [ ] `npm run openapi:export` committed; commits on `feat/check-in`, no push
