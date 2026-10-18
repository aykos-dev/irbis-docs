# Brief levels-2-irbis-api — level endpoints, QA grant, real viewer level on places

- Spec: features/levels.md · ACs in this slice: AC3, AC4
- Repo / branch: irbis-api · `feat/levels`
- Depends on: levels-1-irbis-api (ledger + engine on the branch)

## Files
- Touch: `src/features/levels/` (add `levels.controller.ts`, `me-level.controller.ts` or one controller,
  `qa-grant.controller.ts`, `dto/`, tests) · `src/features/auth/dto/me.response.dto.ts` + me service (add `level`,
  `xpTotal`) · `src/features/auth/dto/admin.dto.ts:269` + `admin-users.service.ts:131` (real level) ·
  `src/features/places/places.service.ts:60-72` + controller (optional viewer) · `src/common/guards/jwt-auth.guard.ts`
  (optional auth on `@Public()` routes) · `src/config/config.schema.ts:57` + `app-config.ts:122` (remove
  `LEVELS_START_LEVEL`; add `QA_TOOLS_ENABLED`) · `openapi.json` (export)
- Read for patterns: `src/features/auth/me.controller.ts`, `src/features/conditions/` controllers + e2e tests,
  `src/common/decorators/public.decorator.ts`. Cross-feature use goes through exported module services (places
  reads the level via `LevelsService.getState` or a `User.level` read in its own repository — pick the one the
  boundaries lint allows).

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | /v1/levels | `@Public()` | — | `{ items: LevelDef[] }` | — |
| GET | /v1/me/level | user | — | `MyLevel` | — |
| POST | /v1/me/level-ups/{id}/seen | user | uuid param | 204 | LEVEL_UP_NOT_FOUND 404 · VALIDATION_FAILED |
| POST | /v1/qa/levels/grant | user | `QaGrantDto` | `MyLevel` | NOT_FOUND 404 when disabled · VALIDATION_FAILED |

- `LevelDef` = `{ level, xp, lessons: {kind, tier|null, required}, checkIns: {required, minDifficulty},
  verifiedSpots, maxDifficulty, newPlacesCount }` — `newPlacesCount` = count of places with `requiredLevel = level`.
- `MyLevel` = `{ level, xpTotal, reachedAt, next: NextLevel|null, pendingLevelUps: PendingLevelUp[] }`;
  `NextLevel` = `{ level, xp: {current, required}, lessons: {current, required, kind, tier}, checkIns: {current,
  required, minDifficulty}, verifiedSpots: {current, required} | null (null when required 0) }` — `current` counted
  with the same rules as the engine; `next` null at L7. `PendingLevelUp` = `{ id, fromLevel, toLevel, maxDifficulty,
  newPlacesCount }`, unseen only, oldest first.
- `QaGrantDto` = `{ xp?: int 1–20000, lessons?: {tier: string 1–20 chars}[] ≤50, checkIns?: {difficulty: int 1–5}[] ≤50,
  verifiedSpots?: int 0–10 }`; each item → `award(qa_grant, refId "qa:<uuid>")` / `recordFact(…, refId "qa:<uuid>")`.
- All DTOs with class-validator + Swagger decorators so orval generates `useLevelsList`, `useMeLevelGet` etc.

## Behaviour
- AC3 — `seen`: sets `seenAt` if null (already seen → 204 again); id of another user → 404 LEVEL_UP_NOT_FOUND.
  `GET /v1/me` gains `level`, `xpTotal`. Admin list + detail `level` = `User.level` (update the DTO description).
  QA grant: when `QA_TOOLS_ENABLED !== true` the route answers exactly like an unknown route (404 NOT_FOUND).
  `QA_TOOLS_ENABLED` zod: boolean string, default false; refine: `NODE_ENV=production` + true → config error at boot.
- AC4 — Optional auth: on `@Public()` routes the JWT guard, when an `Authorization: Bearer` header is present and
  valid, attaches the user; missing/invalid/expired → continue as guest (never 401 on a public route). Blocked
  account → guest. `GET /v1/places/{id}`: `viewer.level` = user's level or 1; `qualifies = requiredLevel ≤ level`.
  Remove `LEVELS_START_LEVEL` everywhere (config, .env.example, tests that set it — if an existing test depends on it,
  report it instead of editing it).

## Approved packages
none

## Done when
- [ ] e2e: `/v1/levels` 7 items with doc numbers + newPlacesCount from seeded places; `/v1/me/level` after a QA
  grant of 300 XP + 2 lessons + 2 check-ins(d1) → level 2, one pending (1→2), next = L3 bars; `seen` 204 then
  pending empty; other user's id → 404; grant 404 when disabled; place detail with token at L2 → `viewer.level 2`,
  bad token → level 1 + 200; admin user detail `level` 2
- [ ] `npm run check` green (output in summary) · `npm run openapi:export` committed · `graphify update .`
