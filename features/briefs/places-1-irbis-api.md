# Brief places-1-irbis-api — Place model, seed, public list + detail

- Spec: features/places.md · ACs in this slice: AC1, AC2, AC3
- Repo / branch: irbis-api · `feat/places` (create from main)
- Depends on: none

## Files
- Touch: `prisma/schema.prisma` (+ new migration `places_init` via `prisma migrate dev --name places_init`) ·
  `prisma/seed/places.data.ts` (move the untracked `data.ts` from the repo root here; keep the data as-is) ·
  `prisma/seed/seed.ts` + pure `prisma/seed/place-seed.rules.ts` (name clean, slug, difficulty, required level) ·
  `package.json` script `db:seed` (and Prisma seed config if that is the 7.x pattern) ·
  `src/features/places/` (new: controller, service, repository, `place.rules.ts` (haversine, filters), errors, `dto/`) ·
  `src/config/config.schema.ts` + `app-config.ts` (PLACES_FALLBACK_LAT default 41.2995, PLACES_FALLBACK_LNG default
  69.2401, LEVELS_START_LEVEL default 1) · `src/app.module.ts` · `test/places.e2e-spec.ts` · `openapi.json`
- Read for patterns (don't change): `src/features/auth/` (controller/service/repository/errors/dto split, `@Public()`),
  `src/lib/cursor.ts`, `src/health/`, `test/onboarding.e2e-spec.ts`, `docs/architecture.md`

## Behaviour
- Schema (spec § Data model): enums `PlaceType { peak lake cave camping trail waterfall canyon }`,
  `SeasonStatus { best possible closed }`, `Hazard { avalanche flood mudslide heat road }` (snake_case `@@map` like
  existing enums); `Place` → table `places`; fields per spec; `@@index([type])`.
- AC1 seed — upsert by slug, so a re-run keeps 71 rows. Name cleanup: remove every `\(\s*\d+\s*m\.?\s*\)` group,
  collapse spaces, trim. Slug: transliterate `ʻ ‘ ' ’` away, lowercase ASCII, non-alnum → `-`, collapse, trim, then
  `-<elevation>`; the seed fails loudly on a duplicate slug. Difficulty: <1500 → 1, 1500–2499 → 2, 2500–3199 → 3,
  3200–3799 → 4, ≥3800 → 5 (from `elevation`). requiredLevel: {1:1, 2:2, 3:3, 4:5, 5:7}. type = `destinationCategories[0]`.
  `descriptionMd` → `descriptionUz`. Unit-test the rules with the real examples: `Qorangur (2943 m.)` →
  `Qorangur`/`qorangur-2941`; `Chuquraq (27 m.) (Kelin Ko'ylak)` → `Chuquraq (Kelin Ko'ylak)`; `Bayroq (2285m)`;
  elevations 1499/1500/3800.
- AC2 `GET /v1/places` (`@Public()`): query DTO with class-validator: `lat`/`lng` numbers (both or neither,
  −90..90 / −180..180), `types` (enum array; accept `types=peak&types=lake` and a comma list), `difficultyMin/Max`
  int 1–5 with min ≤ max, `maxDistanceKm` int 1–1000, `cursor`, `limit` int 1–200 default 50. Origin = lat/lng or
  config fallback; `origin: 'device'|'tashkent'`. Service loads candidates filtered by type/difficulty in the
  repository, computes haversine `distanceM` (integer, earth radius 6371008.8 m) in the service, filters by
  maxDistanceKm, sorts distance asc then id, paginates (cursor = offset token via `src/lib/cursor.ts`), `total` =
  filtered count. (≈71 rows — in-memory distance is fine per ADR-002.)
- AC3 `GET /v1/places/:id` (`@Public()`): `ParseUUIDPipe` → 400 VALIDATION_FAILED; unknown → 404 `PLACE_NOT_FOUND`.
  Same optional lat/lng → `distanceM` + `origin`. `viewer = { level: LEVELS_START_LEVEL, qualifies: requiredLevel <=
  level }` — no token needed; same answer with or without a token.
- Response DTOs with `@ApiProperty` (enums named `PlaceType`, `SeasonStatus`, `Hazard` so orval emits them):
  `PlaceListItemDto`, `PlaceListResponseDto`, `PlaceDetailDto`, `PlaceViewerDto`, `PlaceNameDto { uz, ru|null, en|null }`,
  `PlaceDescriptionDto { uz|null, ru|null, en|null }`.

## API
| Method | Path | Request | Response | Errors (code → status) |
|---|---|---|---|---|
| GET | /v1/places | query above | `{ items, nextCursor, origin, total }` | VALIDATION_FAILED → 400 |
| GET | /v1/places/{id} | `lat?`, `lng?` | `PlaceDetail` | VALIDATION_FAILED → 400, PLACE_NOT_FOUND → 404 |

## Tests (1–3 per AC)
- Unit: seed rules (above); haversine (Tashkent → Qorangur ≈ known km ±1%); filter + sort.
- e2e (Testcontainers, seed a few synthetic places in the test, not the full file): list without token sorted by
  distance with `origin`; filters AND + validation 400s; detail 200 with `viewer`, 404, 400.

## Approved packages
none

## Done when
- [ ] tests for AC1–AC3, `npm run check` green, committed on `feat/places` (Conventional Commits)
- [ ] `npm run openapi:export` committed · migration is new (no existing migration touched)
- [ ] reply ≤ 10 lines: commits, check tail, anything open
