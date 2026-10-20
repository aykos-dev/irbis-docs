# weekly-path

- Status: Approved
- Surfaces: api | app
- Related ADRs: ADR-001 (guest-first), ADR-004 (jobs, Open-Meteo)
- Requirements: Product Overview § How the app works → Every week; § Weekly chest; § Condition statuses ·
  Screens: `design/canvas/Home.dc.html`, `design/canvas/HomeDark.dc.html` (notes `n_home`, `n_homedk`)

## Goal
The Path tab shows **This Month's Path**: 3 places picked for the user's level, interests and the season, then a
chest. Each place shows its live weekend status. A "Not now" place suggests a similar safe place, and checking in
at all 3 opens the chest for XP. (Owner Q1: monthly with 3 + 1 instead of the doc's weekly 7 nodes. The slug stays
`weekly-path`.)

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | `/v1/path` | `@Public` + `@OptionalUser` | `?interests=peaks,lakes` (guests only; ignored with a token) | `PathDto` | 400 `VALIDATION_FAILED` |
| POST | `/v1/path/chest/open` | user | — | `{ opened: true, xp, levelUps }` | 409 `PATH_CHEST_LOCKED`, 404 `PATH_NOT_FOUND` |
| POST | `/v1/qa/path/visits` | user + QA guard (`QA_TOOLS_ENABLED`) | `{ placeId }` | `PathDto` | 404 `PLACE_NOT_ON_PATH` |

`PathDto = { month: "2026-10", level, nodes: PathNode[], chest: { required, done, opened, xp } | null,
weather: { days: [{ date, day: fri|sat|sun, weatherCode, tMaxC, windKmh }] } }`
`PathNode = { position, place: { id, slug, name, type, difficulty, requiredLevel, elevationM }, status, reasons[],
weekendDay?, opensMonth?, done, swap: SwapSuggestion | null }`
`SwapSuggestion = { place: {...same shape}, status: "go", day, distanceFromOriginalKm, elevationDiffM }`

## Data model changes
Migration `weekly_path`:
- `PathMonth` (`path_months`): id, userId → User (cascade), `month` char(7) `YYYY-MM`, createdAt, `chestOpenedAt?`.
  Unique (userId, month).
- `PathNode` (`path_nodes`): id, pathMonthId → PathMonth (cascade), placeId → Place, `position` 1..n, `visitedAt?`.
  Unique (pathMonthId, placeId).
- `PointForecast` (`point_forecasts`): `key` PK (`tashkent`), lat, lng, `daily` Json, fetchedAt.
- `XpSource` + `path_chest`.
- GameConfig `path.config` = `{ nodes: 3, chestXp: 50, origin: { lat: 41.3111, lng: 69.2797 } }` (zod-validated).

## Acceptance criteria
- **AC1 — Build, frozen per month.** The month is the calendar month in Asia/Tashkent. Accounts: the first
  `GET /v1/path` in a month builds and stores the path, and it stays frozen until the 1st 00:00 Tashkent, even if
  level or interests change. Guests: built on each request from `interests` and level 1, never stored. Picking
  rules:
  - Eligible places have `requiredLevel ≤ level` and a type in the user's interests. Interest → types: peaks → peak;
    lakes → lake, waterfall; caves → cave; camping → camping; trails → trail, canyon. No interests means all types.
  - Places closed this month (season `closed`, or an active closure) are excluded.
  - Ranking: `best` season this month before `possible`, then distance from origin (Tashkent) ascending.
  - Distinct types are picked first while the interests allow.
  - Take `path.config.nodes` (3). Fewer candidates give a shorter path; zero gives `nodes: []` and `chest: null`.
- **AC2 — Live status per node.** Each node carries the place's current `PlaceCondition` (status, reasons,
  `weekendDay` = the worst weekend day, `opensMonth`) at request time, not at build time. The app shows a ring + icon
  + label: "Go · Sat", "Caution · wind", "Not now", "Opens in May". Dark mode uses brighter ring tints (≥3:1 on
  #131D22).
- **AC3 — Smart swap (suggest only, owner Q3).** For a `not_now` node, `swap` is the place nearest to the original
  with the same type, `requiredLevel ≤ level`, status `go` and not on the path; otherwise `null`. The card reads "Try
  {name} instead" plus "{±elevation} m, {km} km from {original}, clear skies on {day}". It has 2 buttons:
  - "See place" opens Place.
  - "Keep plan" hides the card for that node until the month ends (stored on the phone).
  The path itself never changes.
- **AC4 — Done nodes.** A node is done when `PathNode.visitedAt` falls in this month.
  `PathService.recordVisit(userId, placeId, at)` sets it (no-op if the place isn't on the user's path) and is the
  hook `check-in` will call. Until then `POST /v1/qa/path/visits` and the app link `irbis://debug/path/visit/<placeId>`
  set it. A done node turns gold with a star and "Done".
- **AC5 — Chest.** The chest is the last node and shows `done/required` (e.g. "1 / 3 · Check in at all 3 places").
  When all nodes are done, tapping it calls `POST /v1/path/chest/open`. That awards `path.chestXp` (50) once per
  user per month (`XpSource.path_chest`, refId `YYYY-MM`), sets `chestOpenedAt` and plays the open animation. A
  second call returns 200 `opened` with xp 0. Before then it returns 409 `PATH_CHEST_LOCKED`. Guests see the chest
  at 0 / n, and tapping it opens the log-in prompt sheet.
- **AC6 — Path screen (app).** The Path tab (initial route) replaces `ComingSoon`.
  - Header: the companion, plus the XP total for accounts (streak, boot and gems are added by `streaks` and `gems`,
    owner Q7). Guests see no XP.
  - Title "This Month's Path", subtitle "{Month} · built for {level name}, {season}".
  - A winding path of nodes. Tapping a node bounces it and opens a popover (name, status, "Open place" → Place).
  - A "Not now" node shows the worried Irbis with a sway and rain.
  - An info button opens a "How the path is built" sheet.
- **AC7 — Weather strip.** Fri / Sat / Sun of the coming weekend for Tashkent (`PointForecast`, fetched by the
  existing hourly conditions job as one extra point). Each day shows glyph, max °C and wind, with "Weather data by
  Open-Meteo.com". On Saturday the strip shows Sat/Sun, on Sunday only Sun.
- **AC8 — States.**
  - Loading: skeleton.
  - Empty (0 nodes): "No places match your level and interests this month" + "Explore the map" → Explore.
  - Error: message + Retry.
  - Offline: the last path cached for this month (MMKV, guests too) with an offline banner, else the offline
    message.
  - Pull to refresh refetches.
  - A month change while the app is open refetches on focus.

### QA events (app, dev/staging builds)
- `path_loaded { month, nodes, guest }` · `path_swap_shown { position }` · `path_swap_kept { position }` ·
  `path_chest_opened { month, xp }` · `path_visit_debug { placeId }`

### testIDs (app)
`path.screen` · `path.node.<n>` · `path.node.<n>.status` · `path.popover.open-place` · `path.swap.card` ·
`path.swap.see` · `path.swap.keep` · `path.chest` · `path.info` · `path.weather` · `path.empty` · `path.retry`

### Required UI states (every touched client)
- [ ] Loading · [ ] Empty · [ ] Error (message + retry) · [ ] Offline (cached path) · [ ] safe areas, haptics on
  node tap / chest open, press states · [ ] tokens + `src/shared/components` only

## Media
`design/media/weekly-path/MEDIA.md`. Canvas inline art is final (owner Q8). Placeholders (STATUS known issue):
the open chest (lid-tilted closed chest) and Reanimated chest-open, coin shower and rain/sway.

## Waivers
- none

## Out of scope
- Real check-ins (`check-in`): the path only exposes `recordVisit`.
- Streak, boot and gems in the header, plus the weather shield (`streaks`, `gems`).
- Seasonal collection card "Autumn Colors" (`seasons`).
- Swapping a place on the path (Q3: suggest only).
- Push notifications for a new month.
- Web admin.

## Assumptions
- Q1 (owner, 2026-10-20): not weekly — the path is monthly and has 3 places + the chest ("most people go on trips
  only once a week").
- Q2 (owner, 2026-10-20): the "+1" is the chest. It opens after check-ins at the 3 path places this month.
- Q3 (owner, 2026-10-20): smart swap is suggest only, and the path never changes.
- Q4 (owner, 2026-10-20): rebuild timing left open → default: lazy on first open in the month, frozen (accounts
  stored, guests rebuilt from the phone's interests).
- Q5 (owner, 2026-10-20): chest left open → default: progress now, +50 XP (server config) once per month, QA visit
  link until `check-in` ships.
- Q6 (owner, 2026-10-20): calendar month in Tashkent. Title "This Month's Path".
- Q7 (owner, 2026-10-20): header shows XP only. Streak, boot and gems come later.
- Q8 (owner, 2026-10-20): placeholders OK, canvas inline art final.
- Main session: weather strip location = Tashkent (no user location in the doc); interest → type mapping for
  waterfall/canyon; ranking origin = Tashkent.

## Open questions
- Does a check-in at the suggested swap place count toward the chest? (Now: no — only path places.)
- Product Overview and canvas still say weekly / 7 nodes — the owner updates the doc.
