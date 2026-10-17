# places

- Status: Approved (owner, 2026-10-17)
- Surfaces: api | app (web CRUD → next feature `places-admin`, Q1)
- Related ADRs: ADR-001 (guest-first: places are readable without an account), ADR-002 (lat/lng as Float, distance in
  the service layer), ADR-003 (REST, cursor pagination, error codes)
- Requirements: Product Overview § Places, conditions & safety (place types, place detail), § Levels (difficulty
  boots, required level, Companions unlocks) · Screens: `design/canvas/Explore`, `Place`, `PlaceDark`
- Seed source: `irbis-api/data.ts` (owner, 71 places: 34 peaks, 22 waterfalls, 11 lakes, 2 caves, 2 canyons)

## Goal
Anyone, guest or signed in, opens **Explore**: a map of Uzbekistan places with type-coloured pins and a list sorted by
distance, filtered by type, difficulty and distance. They open a **Place** to see its type, elevation, distance,
difficulty boots, the level it needs (and whether they qualify), its description, season and hazards.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | /v1/places | `@Public()` | query `lat?`, `lng?` (both or neither), `types?` (PlaceType[]), `difficultyMin?` `difficultyMax?` (1–5), `maxDistanceKm?` (1–1000), `cursor?`, `limit?` (1–200, default 50) | `{ items: PlaceListItem[], nextCursor, origin: 'device' \| 'tashkent', total }` | VALIDATION_FAILED |
| GET | /v1/places/{id} | `@Public()` | query `lat?`, `lng?` | `PlaceDetail` | VALIDATION_FAILED, PLACE_NOT_FOUND (404) |

`PlaceListItem` = `{ id, slug, name: { uz, ru: string|null, en: string|null }, type, latitude, longitude, elevationM,
difficulty, requiredLevel, distanceM }`. `PlaceDetail` = list item + `{ region: string|null, description: { uz, ru, en }
(each string|null), season: SeasonStatus[] (12 or empty), hazards: Hazard[], origin, viewer: { level, qualifies } }`.
Origin: request lat/lng if given, else Tashkent centre from server config (`PLACES_FALLBACK_LAT/LNG`, default
41.2995 / 69.2401). `viewer.level` = start level from server config (1) until `levels` ships; `qualifies` =
`requiredLevel <= viewer.level`.

## Data model changes
New migration `places_init`.
- `enum PlaceType { peak lake cave camping trail waterfall canyon }`
- `enum SeasonStatus { best possible closed }`, `enum Hazard { avalanche flood mudslide heat road }`
- `model Place` (table `places`): `id uuid`, `slug String @unique`, `nameUz`, `nameRu?`, `nameEn?`, `type PlaceType`,
  `latitude Float`, `longitude Float`, `elevationM Int`, `difficulty Int` (1–5), `requiredLevel Int` (1–7),
  `region String?`, `descriptionUz?`, `descriptionRu?`, `descriptionEn?`, `season SeasonStatus[] @default([])`,
  `hazards Hazard[] @default([])`, `createdAt`, `updatedAt`; index on `type`.
- Seed: `prisma/seed/places.data.ts` (moved from `data.ts`) + idempotent seed script (`npm run db:seed`).

## Acceptance criteria
- **AC1** — Seed: `npm run db:seed` imports all 71 rows from `places.data.ts`; running it twice still leaves 71 places
  (upsert by slug). Name: a parenthesised height (`(2943 m.)`, `(100 m)`, `(2285m)`) is removed and spaces trimmed
  (`Chuquraq (27 m.) (Kelin Ko'ylak)` → `Chuquraq (Kelin Ko'ylak)`), stored as `nameUz`; `ru`/`en` null.
  Slug = kebab-case ASCII of the cleaned name + `-` + elevation (`ozodbosh-1014`), unique. Type = the row's single
  category. Difficulty from elevation: <1500 m → 1, 1500–2499 → 2, 2500–3199 → 3, 3200–3799 → 4, ≥3800 → 5.
  Required level from difficulty: 1→1, 2→2, 3→3, 4→5, 5→7. `descriptionMd` → `descriptionUz`. Region, season,
  hazards empty.
- **AC2** — `GET /v1/places` works without a token and returns places sorted by distance from the origin ascending
  (ties by id), `distanceM` as integer metres (haversine), `total` = count after filters. Filters combine with AND:
  `types` any-of, `difficultyMin..Max` inclusive, `maxDistanceKm` inclusive. Only one of `lat`/`lng`, lat outside
  −90..90, lng outside −180..180, `difficultyMin > difficultyMax` or an unknown type → 400 VALIDATION_FAILED.
  `limit` 200 returns every seed place in one page.
- **AC3** — `GET /v1/places/{id}` works without a token and returns `PlaceDetail`; an unknown uuid → 404
  PLACE_NOT_FOUND, a non-uuid → 400 VALIDATION_FAILED. `viewer` is `{ level: 1, qualifies: requiredLevel <= 1 }` for
  guests and signed-in users alike.
- **AC4** — Explore tab (replaces Coming soon): full-screen MapLibre map (OpenFreeMap style URL from app config) with
  one pin per place, coloured + iconed by type (peak teal, lake blue, cave purple, camping green, trail orange,
  waterfall and canyon placeholder colours), clustered with a count when they overlap. A bottom sheet lists the
  same places: header "{n} places near you" (or "{n} places from Tashkent"), "Sorted by distance"; each card shows
  the type illustration, name (app locale, fallback uz), "{Type} · {distance}" and difficulty boots. Tapping a card
  or a single pin opens Place. Distance format: < 10 km → one decimal ("8.4 km"), else whole km ("112 km"), locale
  number format.
- **AC5** — Filters: chips Type (multi-select of the 7 types), Difficulty (range 1–5), Distance (≤ 50 / ≤ 100 /
  ≤ 150 km / Any; default Any). Apply refetches the map and list together; an active chip shows its value (e.g.
  "Peaks · Lakes", "Difficulty 1–3", "≤ 150 km"). No match → empty state "No places match these filters" with
  "Reset filters" (clears all). Filters last for the app session.
- **AC6** — Location: the first time Explore opens, the OS location prompt is shown. Granted → origin is the device
  position, distances read "from you", the map centres on the user. Denied, location off, or no fix in 10 s →
  origin Tashkent, distances read "from Tashkent", the map centres on Tashkent, and a banner "Turn on location to see
  distances from you" with "Turn on" (re-asks if the OS still allows it, else opens app settings). Returning from
  settings with permission granted switches to device origin without a restart.
- **AC7** — Place screen (light + dark per `Place`/`PlaceDark`): type illustration hero; type pill (colour + icon +
  label); name; region line only if set; Elevation "{n} m"; "{distance}" with label "From you" / "From Tashkent";
  "Difficulty {d}/5" with boots; the level card (AC8); description if set (locale, fallback uz); Best season bar
  (12 months J–D, today's month marked, legend Best / Possible / Closed) or "Season not set yet"; hazards list
  or "Hazards not set yet". No condition, weather, ratings, reports, trails, badges, verification, discoverer or
  "Start adventure" (later features). Back returns to Explore with filters and list position kept.
- **AC8** — Level card: `qualifies` → "Requires · Level {n} · {name} or higher" + green check "You qualify";
  otherwise a lock + "Requires · Level {n} · {name} or higher" + "Reach Level {n} to go here". Names: 1 Wanderer,
  2 Burrower, 3 Pathfinder, 4 Ridge Walker, 5 Mountain Guardian, 6 Sky Watcher, 7 Snow Legend.

### QA events (app, dev/staging builds)
- `explore_loaded { count, origin }` · `explore_filters_applied { types, difficultyMin, difficultyMax, maxKm, count }`
- `location_permission { result: granted|denied|blocked|unavailable }` · `place_viewed { slug, requiredLevel, qualifies }`

### testIDs (app)
`explore.screen`, `explore.map`, `explore.sheet`, `explore.count`, `explore.card.<slug>`, `explore.filter.type`,
`explore.filter.difficulty`, `explore.filter.distance`, `explore.filter.apply`, `explore.filter.reset`,
`explore.empty`, `explore.location-banner`, `explore.location-turn-on`, `place.screen`, `place.name`,
`place.type`, `place.elevation`, `place.distance`, `place.difficulty`, `place.level-card`, `place.level-qualify`,
`place.level-locked`, `place.description`, `place.season`, `place.season-empty`, `place.hazards`,
`place.hazards-empty`, `place.back`.

### Required UI states (every touched client)
- [ ] Loading (map + list skeleton; Place skeleton)
- [ ] Empty (no filter match, AC5)
- [ ] Error (message + retry) on list and Place
- [ ] Offline (last loaded list/place from the query cache, else offline message + retry)
- [ ] Permissions denied (AC6 banner, Tashkent fallback)
- [ ] App: safe areas, haptics on chip/filter toggles, press states; Russian/Uzbek copy wraps
- [ ] Design tokens and `src/shared/components` primitives only; light + dark

## Media
From `design/media/places/MEDIA.md` (Q8): peak, lake, cave canvas SVGs **final**; waterfall + canyon hero art and type
icons/colours are **placeholders** (STATUS known issue) until the owner drops files in `design/media/places/`; no photo
gallery (no photo storage yet).

## Waivers
- none

## Out of scope
- Web admin CRUD (`places-admin`, next) · trails and TrailMap (no trail data) · photo gallery/upload
- Condition status, weather, hazard levels "now", community reports (`conditions`) · ratings, badges, verification,
  First Discoverer (later features) · Start adventure (`trip-plan`) · real user levels (`levels`) · search (`search`)
- iOS map build (pods never installed — existing known issue)

## Assumptions
- Q1 (owner, 2026-10-17): places = api + app; web admin is the next feature `places-admin`; trails later.
- Q2 (owner, 2026-10-17): map = `@maplibre/maplibre-react-native` + OpenFreeMap tiles (no key) — package approved.
- Q3 (owner, 2026-10-17): seed derives difficulty from elevation bands and required level from the Companions unlocks;
  all seeded places are published; season/hazards/region empty, shown as "not set yet".
- Q4 (owner, 2026-10-17): add types waterfall + canyon; keep all 71 rows (same-name rows are separate places).
- Q5 (owner, 2026-10-17): ask for location on first Explore open; denied → distances from Tashkent centre + banner.
- Q6 (owner, 2026-10-17): show the level gate against Level 1 (API returns `viewer.level` = 1 until `levels`).
- Q7 (owner, 2026-10-17): names stored as uz + optional ru/en (fallback uz); seed strips "(… m)" from names.
- Q8 (owner, 2026-10-17): canvas peak/lake/cave SVGs final; waterfall/canyon placeholders; no photos.
- Sorting is by distance, not the canvas's "Sorted by fit" (fit belongs to `weekly-path`).
- Device location comes from MapLibre's location manager; a separate geolocation package needs approval first.

## Open questions
- none
