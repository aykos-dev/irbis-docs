# Brief conditions-2-irbis-api — public + admin endpoints

- Spec: features/conditions.md · ACs in this slice: AC4, AC5
- Repo / branch: irbis-api · `feat/conditions`
- Depends on: brief conditions-1-irbis-api (engine, models, `recomputePlace`, `runNow`, `isRunning`)

## Files
- Touch: `src/features/conditions/` (add `conditions.controller.ts`, `admin-conditions.controller.ts`, `conditions.errors.ts`,
  `dto/*`) · `src/features/places/places.service.ts` + dto (add `conditionStatus` to list items — read it via the
  conditions repository export or a join; features don't import each other's internals: export a small query from
  the conditions module) · `test/conditions.e2e-spec.ts` (new) · `openapi.json` (export)
- Read for patterns: `src/features/places/places.controller.ts` + dto, `src/features/auth/admin-users.controller.ts`
  (@Roles('admin'), cursor list, errors), `src/common/decorators/*`, `src/common/errors/*`, `test/admin.e2e-spec.ts`

## Behaviour
- AC4 — `GET /v1/places/{id}/condition` `@Public()`: `ParseUUID` → 400 VALIDATION_FAILED; unknown → 404 PLACE_NOT_FOUND;
  place without a condition row → `{ placeId, status: null, source: null, reasons: [], text: null, opensMonth: null,
  hazards: [], weekend: [], forecastAt: null, computedAt: null }`. `text` = active closure/override reason
  `{uz, ru|null, en|null}` when source is closure/manual. `GET /v1/places` items gain `conditionStatus` (null when none);
  no other change to places behaviour or its tests (only add assertions in new tests).
- AC5 — `@Roles('admin')` on every admin route (user token → 403, none → 401):
  - `GET /v1/admin/conditions?status=&cursor=&limit=` (1–200, default 50, order by place name uz then id) →
    `{ items: AdminConditionRow[], nextCursor, total }`; `status` ∈ ConditionStatus or `none` (null status).
  - `GET /v1/admin/places/{id}/condition-controls` → `{ condition, closures, overrides }` newest first.
  - `POST /v1/admin/places/{id}/closures` body `{ startsAt, endsAt?, reason: {uz, ru?, en?}, source }`: ISO dates,
    `endsAt` > `startsAt`, `reason.uz` 1–280 chars trimmed, ru/en ≤ 280 → else 400 with fieldErrors. 201 `Closure`.
  - `POST /v1/admin/closures/{id}/end` → sets `endedAt`/`endedById`; 404 CLOSURE_NOT_FOUND; 409 CLOSURE_ALREADY_ENDED.
  - `POST /v1/admin/places/{id}/overrides` body `{ status, reason, expiresAt }`: `expiresAt` in (now, now + 14 d] →
    else 400; ends the current active override of that place in the same transaction, then creates. 201 `Override`.
  - `POST /v1/admin/overrides/{id}/end` → 404 OVERRIDE_NOT_FOUND; 409 OVERRIDE_ALREADY_ENDED.
  - Each create/end calls `recomputePlace(placeId)` before responding (response reflects the new status on the next read).
  - `POST /v1/admin/conditions/recompute` → 202 `{ startedAt }` and runs the full job (fetch + recompute) in the
    background; 409 RECOMPUTE_RUNNING while running. `createdById`/`endedById` from the admin token.
  - Response DTOs: `Closure { id, placeId, startsAt, endsAt, reason{uz,ru,en}, source, createdAt, endedAt, active }`,
    `Override { id, placeId, status, reason, expiresAt, createdAt, endedAt, active }` — never admin passwords/phones;
    ids of creator/ender not exposed.

## From slice 1 (api 44e08b5)
- `opensMonth` is not stored: derive it at read time with the exported `nextOpenMonth(season, month)` (Tashkent month)
  when status is `seasonal_lock`; no new column.
- Seasonal lock has empty `reasons` — fine; clients use `opensMonth`.
- The cron is active in e2e and may call the real Open-Meteo: add config `CONDITIONS_JOB_ENABLED` (default `true`,
  `false` in the e2e/test env) and skip registering/running the cron when false; `runNow()` still works (stubbed client).

## Errors (code → status)
VALIDATION_FAILED 400 · PLACE_NOT_FOUND 404 · CLOSURE_NOT_FOUND 404 · OVERRIDE_NOT_FOUND 404 ·
CLOSURE_ALREADY_ENDED 409 · OVERRIDE_ALREADY_ENDED 409 · RECOMPUTE_RUNNING 409 · UNAUTHORIZED 401 · FORBIDDEN 403

## Tests (e2e against the test DB; Open-Meteo is never called in e2e — stub the client provider)
- public condition: guest 200 shape, 404, 400; list has `conditionStatus`
- closure makes status not_now immediately; override beats closure; second override ends the first; end twice → 409
- user token → 403 on an admin route; expiresAt > 14 d → 400

## Approved packages
none

## Done when
- [ ] tests per AC green, `npm run check` green, `npm run openapi:export` committed, all on `feat/conditions`
