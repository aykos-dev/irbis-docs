# Brief weekly-path-1-irbis-api — monthly path build, live status, smart swap, Tashkent weather

- Spec: features/weekly-path.md · ACs in this slice: AC1, AC2, AC3, AC7
- Repo / branch: irbis-api · `feat/weekly-path` (create from main)
- Depends on: none

## Files
- Touch: `src/features/weekly-path/` (new: controller, service, repository, errors, dto, picker (pure function),
  module, unit specs) · `prisma/schema.prisma` + new migration `weekly_path` (PathMonth, PathNode, PointForecast,
  `XpSource.path_chest` — add the enum value now so slice 2 needs no migration) ·
  `src/features/levels/game-config.schema.ts`, `game-config.service.ts`, `levels.constants.ts` (key `path.config` +
  getter) · `prisma/seed/game-config.data.ts` · `src/features/conditions/conditions.job.ts` / its forecast client
  (one extra point `tashkent`) · `src/app.module.ts` · `openapi.json` (export) · `test/weekly-path.e2e-spec.ts`.
- Read for patterns (don't change): `src/features/conditions/` (`weekend-window.ts`, `condition.rules.ts`
  `isSeasonClosed`, `conditions.service.ts` ~:210, forecast fetch), `src/features/places/places.controller.ts:58`
  (`@Public()` + `@OptionalUser()`), `places.response.dto.ts` (L10n names), `src/features/levels/levels.service.ts`
  (`getState` :192), `src/lib/dates.ts` (Tashkent helpers), `test/levels-api.e2e-spec.ts` (e2e setup).

## Behaviour
- AC1 — `GET /v1/path` (`@Public()` + `@OptionalUser()`, operationId `Path_get`). Month = `YYYY-MM` of now in
  Asia/Tashkent.
  - Signed in: if a `PathMonth(userId, month)` exists, return it (frozen). Otherwise pick with level = `getState().level`
    and interests = `User.interests`, store PathMonth + PathNodes (position 1..n), and return it. Unique race → re-read.
  - Guest: `interests` query param (comma list of the `Interest` enum, optional, 400 `VALIDATION_FAILED` on unknown);
    level 1; nothing stored. The param is ignored when a user is present.
  - Picker (pure, unit-tested):
    - Interest → types: peaks→peak; lakes→lake, waterfall; caves→cave; camping→camping; trails→trail, canyon. An
      empty list means all types.
    - Eligible: `requiredLevel ≤ level`, type allowed, not season-closed this Tashkent month (`isSeasonClosed`), no
      closure active now.
    - Sort: season this month `best` before `possible` (an empty season array counts as `possible`), then haversine
      distance from `path.config.origin` ascending, then slug.
    - Fill `nodes` (3) taking distinct types first in sorted order, then fill the remaining slots from the rest.
    - Zero eligible → `nodes: []`, `chest: null`.
  - `path.config` GameConfig (zod: `nodes` int 1–7, `chestXp` int ≥ 0, `origin { lat, lng }`), seed
    `{ nodes: 3, chestXp: 50, origin: { lat: 41.3111, lng: 69.2797 } }`.
- AC2 — Each node: `{ position, place: { id, slug, name (L10n like places), type, difficulty, requiredLevel,
  elevationM }, status, reasons, weekendDay, opensMonth, done, swap }`.
  - `status`, `reasons` and `opensMonth` come from the current `PlaceCondition`. A missing row or null status is
    passed as null (the app shows a neutral ring with no label).
  - `weekendDay` = the `day` (`sat`|`sun`) of the first reason that has one, else the first weekend day.
  - `done` = `visitedAt` within this month (always false in this slice).
  - `chest` = `{ required: nodes.length, done: count(done), opened: chestOpenedAt != null, xp: path.config.chestXp }`;
    guests `{ required, done: 0, opened: false, xp }`.
- AC3 — `swap` only when the node status is `not_now`, else null. Pick the place with the same type,
  `requiredLevel ≤ level` and current status `go`, not on the path, nearest (haversine) to the original. Return
  `{ place, status: 'go', day: its weekendDay, distanceFromOriginalKm (int), elevationDiffM (int, swap − original) }`,
  or null if there is none.
- AC7 — `weather: { days }`.
  - The hourly conditions job also fetches Open-Meteo daily for `PointForecast` key `tashkent` (origin coords) in the
    same batch and upserts it. A failure logs and keeps the old row.
  - `days` = Fri, Sat, Sun of the coming weekend from that row. On Saturday only Sat+Sun, on Sunday only Sun; Mon–Thu
    give the coming Fri–Sun.
  - Each day `{ date, day: fri|sat|sun, weatherCode, tMaxC (int), windKmh (int) }`. No row → `days: []`.

## API
| Method | Path | Request | Response | Errors (code → status) |
|---|---|---|---|---|
| GET | `/v1/path` | `?interests=peaks,lakes` (guest) | `PathDto { month, level, nodes, chest, weather }` | `VALIDATION_FAILED` → 400 |

## Copy
None (API returns data, L10n names only).

## testIDs · QA events
— (app slices)

## Approved packages
none

## Done when
- [ ] Unit: picker (level filter, interest mapping incl. waterfall/canyon, season closed excluded, best-before-possible,
  distinct types, fewer than 3, zero). Swap picker (same type, go only, excludes path places, null case). Weekend
  days Mon/Sat/Sun.
- [ ] e2e: guest GET with interests, signed-in GET stores and returns the same nodes on a 2nd call after the user's
  interests change.
- [ ] `npm run check` green, `npm run openapi:export` committed, committed on the branch
