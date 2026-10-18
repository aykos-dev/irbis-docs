# Brief levels-1-irbis-api — XP ledger, GameConfig, level engine

- Spec: features/levels.md · ACs in this slice: AC1, AC2
- Repo / branch: irbis-api · `feat/levels` — create it from `feat/conditions` (head 7974da3), not from main (owner Q8)
- Depends on: none

## Files
- Touch: `prisma/schema.prisma` + new migration `levels_init` (never edit old ones) · seed: add the two GameConfig
  rows to the existing seed (find it next to the places seed; upsert, idempotent) ·
  `src/features/levels/` (new): `levels.module.ts`, `game-config.service.ts` (typed loader), `game-config.schema.ts`
  (zod), `level-engine.ts` (pure: no Prisma, no Nest), `levels.service.ts` (`award`, `recordFact`, `evaluate`),
  `levels.repository.ts` (Prisma only), `levels.errors.ts`, `__tests__/` · `src/app.module.ts` (import the module)
- Read for patterns (don't change): `src/features/conditions/` (service → repository split, config use, tests),
  `docs/architecture.md` §§ levels / GameConfig / XpEntry (lines ~100, 136–189), `src/config/app-config.ts`
- `graphify` is at `~/.local/bin/graphify` if it isn't on PATH.

## Data model (migration `levels_init`)
- `GameConfig { key String @id, value Json, updatedAt DateTime @updatedAt }` → table `game_config`
- `enum XpSource { lesson check_in waypoint discoverer top_shots post game campfire qa_grant }`
- `XpEntry { id uuid, userId, source XpSource, refId String, amount Int, createdAt }` → `xp_entries`,
  `@@unique([userId, source, refId])`, index `(userId, source, createdAt)`; FK user onDelete Cascade
- `enum LevelFactKind { lesson check_in verified_spot }`; `LevelFact { id, userId, kind, refId, tier String?,
  difficulty Int?, createdAt }` → `level_facts`, `@@unique([userId, kind, refId])`, index `(userId, kind)`
- `LevelUp { id, userId, fromLevel Int, toLevel Int, createdAt, seenAt DateTime? }` → `level_ups`, index `(userId, seenAt)`
- `User` + `level Int @default(1)`, `xpTotal Int @default(0) @map("xp_total")`, `levelReachedAt DateTime @default(now())`

## Config (seeded GameConfig rows; values from the doc, "decided after testing")
- `levels.table`: array of 7 `{ level, xp, lessons: {kind: "count"|"tier"|"all", tier: string|null, required},
  checkIns: {required, minDifficulty}, verifiedSpots, maxDifficulty }`:
  L1 0 · count null 0 · 0 ≥1 · 0 · max 1 | L2 300 · count null 2 · 2 ≥1 · 0 · 2 | L3 1000 · tier "2" 6 · 5 ≥2 · 0 · 3 |
  L4 2500 · tier "3" 6 · 8 ≥3 · 0 · 3 | L5 5000 · tier "first-aid" 6 · 12 ≥3 · 0 · 4 | L6 9000 · tier "5" 6 · 15 ≥4 · 0 · 4 |
  L7 15000 · all null 36 · 25 ≥5 · 3 · 5
- `xp.dailyCaps`: `{ "post": 5, "game": 30, "campfire": 30 }` (sources not listed = no cap)
- Loader validates with zod (7 rows, levels 1..7 ascending, xp non-decreasing); invalid/missing → throws at use
  with a clear error (no silent defaults). Cache in memory ≤ 60 s.

## Behaviour
- AC1 — `award({userId, source, refId, amount>0})` in one transaction: existing `(userId, source, refId)` → return
  `{ entry: existing, created: false }`, no change. Capped source: sum today's entries for that source (today =
  Asia/Tashkent calendar day, boundary 00:00 +05:00, UTC stored) and trim to `cap - used`; 0 left → no entry,
  `{ entry: null, created: false, capped: true }`. Else insert, `xpTotal += amount`, then `evaluate`. Returns
  `{ entry, created, capped, levelUps: LevelUp[] }`. `recordFact({userId, kind, refId, tier?, difficulty?})` same
  idempotency, then `evaluate`. Concurrency: unique constraint is the guard — catch P2002 and return the existing row.
- AC2 — `evaluate(userId)`: load user, table, fact counts (lessons total, lessons by tier, check-ins by difficulty,
  verified spots); pure `nextReachableLevels(table, state)` returns every level above the current one whose
  requirements are all met, stopping at the first unmet level (no skipping over an unmet level). For each, insert a
  `LevelUp {fromLevel, toLevel}` (one per step), set `User.level` and `levelReachedAt = now`. Never lowers `level`.
  Gate rules: count → lesson facts ≥ required; tier → lesson facts with `tier = X` ≥ required; all → lesson facts ≥
  required; check-ins → facts with `difficulty ≥ minDifficulty` ≥ required (lifetime); spots ≥ verifiedSpots.
- Export from the module for later features: `LevelsService.award`, `recordFact`, `getState(userId)` (level, xpTotal,
  reachedAt, counts — slice 2 builds endpoints on it).

## Errors
- `GAME_CONFIG_INVALID` (500, internal only) · amount ≤ 0 / bad difficulty (1–5) → programmer error, throw.

## Approved packages
none

## Done when
- [ ] tests: idempotent award (same refId twice → one entry, xpTotal once); cap trims 28+5 → 2 and a Tashkent-day
  boundary case (23:59 vs 00:01 +05:00); engine: all three gates needed (XP alone doesn't level), multi-level jump
  writes 2 LevelUps, never down after a threshold rise, tier gate counts only that tier, L7 needs 3 spots;
  config zod rejects a bad table
- [ ] `npm run check` green (output in your summary), migration created with `prisma migrate dev` on a local DB,
  committed on `feat/levels`; `graphify update .`
