# Brief weekly-path-2-irbis-api — visits, chest open, QA visit endpoint

- Spec: features/weekly-path.md · ACs in this slice: AC4, AC5
- Repo / branch: irbis-api · `feat/weekly-path`
- Depends on: brief weekly-path-1-irbis-api (on the branch)

## Files
- Touch: `src/features/weekly-path/` (service, repository, controller, errors, dto, QA controller, specs) ·
  `openapi.json` (export) · `test/weekly-path.e2e-spec.ts`.
- Read for patterns (don't change): `src/features/levels/qa-grant.controller.ts` + `qa-tools.guard.ts` (QA route
  guard, `QA_TOOLS_ENABLED`), `src/features/levels/levels.service.ts` (`award` :92 → `{ entry, created, capped,
  levelUps }`), `src/features/lessons/` (award flow, error classes), `src/features/weekly-path/` (slice 1).

## Behaviour
- AC4 — `WeeklyPathService.recordVisit(userId, placeId, at = now)`, exported from the module for `check-in` later.
  - Find the user's `PathMonth` for the Tashkent month of `at`, and in it the `PathNode` for `placeId`.
  - If both exist and `visitedAt` is null, set `visitedAt = at`. Otherwise it is a no-op. Returns
    `{ recorded: boolean }`.
  - No XP is given here (check-in XP belongs to `check-in`).
  - `POST /v1/qa/path/visits` (user + the existing QA guard; 404 like the other QA routes when disabled), body
    `{ placeId: uuid }`. It builds the month's path first if missing (same as GET), then calls `recordVisit`.
  - If the place isn't on the path → 404 `PLACE_NOT_ON_PATH`. Otherwise it returns the full `PathDto` (same mapper as
    GET), with `done` true for the node.
- AC5 — `POST /v1/path/chest/open` (user, operationId `Path_openChest`).
  - No PathMonth this month → 404 `PATH_NOT_FOUND`.
  - Not all nodes done (or 0 nodes) → 409 `PATH_CHEST_LOCKED`.
  - Already opened → 200 `{ opened: true, xp: 0, levelUps: [] }`.
  - Otherwise: `levels.award({ userId, source: 'path_chest', refId: month, amount: path.config.chestXp })`, set
    `chestOpenedAt = now`, and return `{ opened: true, xp: entry?.amount ?? 0, levelUps }`. The ledger unique
    `(user, path_chest, month)` makes a race award once. A concurrent second call returns xp 0.
  - GET `/v1/path` then shows `chest.opened: true`, `chest.done` = the count of done nodes.

## API
| Method | Path | Request | Response | Errors (code → status) |
|---|---|---|---|---|
| POST | `/v1/path/chest/open` | — | `{ opened, xp, levelUps }` | `PATH_NOT_FOUND` → 404, `PATH_CHEST_LOCKED` → 409, 401 |
| POST | `/v1/qa/path/visits` | `{ placeId }` | `PathDto` | `PLACE_NOT_ON_PATH` → 404, `VALIDATION_FAILED` → 400 |

## Copy
None.

## testIDs · QA events
—

## Approved packages
none

## Done when
- [ ] Unit: recordVisit (sets once, no-op off path / other month / no path).
- [ ] e2e: QA visit → GET shows done. Chest locked at 2/3 → 409. 3/3 → +50 XP and `xpTotal` up. 2nd open → xp 0.
  Guest → 401. Another month's path doesn't count.
- [ ] `npm run check` green, `npm run openapi:export` committed, committed on the branch
