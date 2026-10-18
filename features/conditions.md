# conditions

- Status: Approved (owner, 2026-10-18)
- Surfaces: api | web | app
- Related ADRs: ADR-001 (conditions readable without an account), ADR-002, ADR-003 (REST, cursor, error codes),
  **ADR-004 (new): job runner `@nestjs/schedule` + weather provider Open-Meteo**
- Requirements: Product Overview § Places, conditions & safety (status table, sources, place detail) ·
  Screens: `design/canvas/Place`, `PlaceDark` (condition card "Go this weekend", "Weather at the lake", "Hazards now"),
  `Explore` (status chip on cards) · tokens `design/design.md` § Condition status
- Builds on: `places` (Place model with `season[12]`, `hazards[]`; public list + detail; app Explore + Place)

## Goal
Every place has a live status — Go / Caution / Not now / Seasonal lock, always colour + icon + label — for the coming
weekend, with the reasons and the weekend weather. It is computed hourly from the Open-Meteo forecast, the place's
hazards, its season bar, official/admin closures and admin overrides. Admins manage closures and overrides in the web
panel. Guests and users see it on Place and on Explore cards.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | /v1/places/{id}/condition | `@Public()` | — | `PlaceCondition` | VALIDATION_FAILED, PLACE_NOT_FOUND |
| GET | /v1/places (existing) | `@Public()` | unchanged | `PlaceListItem` + `conditionStatus: ConditionStatus \| null` | unchanged |
| GET | /v1/admin/conditions | admin | `status?`, `cursor?`, `limit?` (1–200, default 50) | `{ items: AdminConditionRow[], nextCursor, total }` | VALIDATION_FAILED |
| GET | /v1/admin/places/{id}/condition-controls | admin | — | `{ condition: PlaceCondition, closures: Closure[], overrides: Override[] }` (newest first) | PLACE_NOT_FOUND |
| POST | /v1/admin/places/{id}/closures | admin | `{ startsAt, endsAt?, reason: {uz, ru?, en?}, source: official\|admin }` | `Closure` (201) | VALIDATION_FAILED, PLACE_NOT_FOUND |
| POST | /v1/admin/closures/{id}/end | admin | — | `Closure` | CLOSURE_NOT_FOUND, CLOSURE_ALREADY_ENDED (409) |
| POST | /v1/admin/places/{id}/overrides | admin | `{ status, reason: {uz, ru?, en?}, expiresAt }` | `Override` (201) | VALIDATION_FAILED, PLACE_NOT_FOUND |
| POST | /v1/admin/overrides/{id}/end | admin | — | `Override` | OVERRIDE_NOT_FOUND, OVERRIDE_ALREADY_ENDED (409) |
| POST | /v1/admin/conditions/recompute | admin | — | `{ startedAt }` (202) | RECOMPUTE_RUNNING (409) |

`PlaceCondition` = `{ placeId, status: ConditionStatus | null, source: forecast|hazard_rule|closure|season|manual|null,
reasons: Reason[] (worst first, ≤ 3), text: {uz, ru|null, en|null} | null (closure/override reason), opensMonth: 1–12 |
null, hazards: { hazard, level: low|raised|high|open|closed }[], weekend: WeekendDay[], forecastAt | null, computedAt }`.
`Reason` = `{ code, day?: sat|sun, value?: int }`. `WeekendDay` = `{ date, day: sat|sun, weatherCode, tMaxC, tMinC,
windKmh, gustKmh, precipMm, precipProbPct, snowCm }` (integers). `AdminConditionRow` = `{ placeId, slug, name, type,
status, source, computedAt, forecastAt, activeClosureId?, activeOverrideId? }`.

## Data model changes
New migration `conditions_init`.
- `enum ConditionStatus { go caution not_now seasonal_lock }`, `enum ConditionSource { forecast hazard_rule closure season manual }`,
  `enum ClosureSource { official admin }`
- `model PlaceCondition` (`place_conditions`): `placeId` PK/FK, `status ConditionStatus?`, `source ConditionSource?`,
  `reasons Json`, `hazardLevels Json`, `weekend Json`, `forecastAt DateTime?`, `computedAt`; index on `status`.
- `model PlaceForecast` (`place_forecasts`): `placeId` PK/FK, `daily Json` (Open-Meteo daily, past 3 + next 7 days), `fetchedAt`.
- `model Closure` (`closures`): `id uuid`, `placeId`, `startsAt`, `endsAt?`, `reasonUz`, `reasonRu?`, `reasonEn?`,
  `source ClosureSource`, `createdById`, `createdAt`, `endedAt?`, `endedById?`; index `(placeId, endedAt)`.
- `model ConditionOverride` (`condition_overrides`): `id uuid`, `placeId`, `status ConditionStatus`, `reasonUz`,
  `reasonRu?`, `reasonEn?`, `expiresAt`, `createdById`, `createdAt`, `endedAt?`, `endedById?`.
  Closures and overrides are never deleted: ending sets `endedAt`/`endedById` (that is the audit trail).

## Acceptance criteria
- **AC1** — Forecast job: `@nestjs/schedule` cron at minute 5 of every hour (Asia/Tashkent) fetches Open-Meteo daily
  forecast (`timezone=Asia/Tashkent`, `past_days=3`, `forecast_days=7`; `weather_code, temperature_2m_max/min,
  precipitation_sum, precipitation_probability_max, wind_speed_10m_max, wind_gusts_10m_max, snowfall_sum`) for every
  place in batches of 50 coordinates, stores it in `PlaceForecast`, then recomputes every `PlaceCondition`. A failed
  or timed-out (10 s) batch keeps that batch's previous forecast, logs `CONDITIONS_FETCH_FAILED` (no PII) and the
  recompute still runs. Base URL and every threshold below come from server config with these defaults.
- **AC2** — Weather + hazard rules over the window (Tashkent date: Mon–Fri → coming Sat + Sun; Sat → Sat + Sun; Sun →
  Sun); worst day wins. **Not now:** weather code 95/96/99 (THUNDERSTORM), gusts ≥ 60 km/h (GUSTS), precipitation
  ≥ 20 mm/day (HEAVY_PRECIP). **Caution:** wind ≥ 35 km/h (WIND), precipitation chance ≥ 60 % (PRECIP_LIKELY),
  max ≥ 35 °C (HEAT), min ≤ −10 °C (COLD). Only for hazards the place has: mudslide/flood rain ≥ 10 mm → Caution,
  ≥ 30 mm → Not now (MUDSLIDE_RISK / FLOOD_RISK); avalanche snowfall in last 3 days + window ≥ 10 cm → Caution,
  ≥ 30 cm → Not now (AVALANCHE_RISK); heat max ≥ 35 → Caution, ≥ 40 → Not now (HEAT). Hazard levels: below the
  Caution value = low, Caution = raised, Not now = high; road = `open`, or `closed` while a closure is active.
  Nothing triggered → Go with reason `GOOD_WEATHER { day, value: windKmh }`. Source = `hazard_rule` if a hazard rule
  set the worst status, else `forecast`.
- **AC3** — Precedence: active override (`endedAt` null, `expiresAt` > now) → its status, source `manual`, its text;
  else active closure (`startsAt` ≤ now, `endsAt` null or > now, not ended) → Not now, source `closure`, its text;
  else the current Tashkent month is `closed` in the season bar → Seasonal lock, `opensMonth` = next non-closed month
  (wrapping); else AC2. No stored forecast and nothing above → `status null`. Creating/ending a closure or override
  recomputes that place at once (no refetch); the hourly job ends expired overrides' effect without writing `endedAt`.
- **AC4** — `GET /v1/places/{id}/condition` works without a token and returns `PlaceCondition` (404 PLACE_NOT_FOUND for
  an unknown uuid, 400 for a non-uuid). `GET /v1/places` items carry `conditionStatus` (null when none). A forecast
  older than 6 h keeps the last status; `forecastAt` tells clients how old it is.
- **AC5** — Admin API (all `@Roles('admin')`; user token → 403, none → 401): list with status filter; condition
  controls per place; create closure (`endsAt` > `startsAt` when set, `reason.uz` 1–280 chars, ru/en ≤ 280);
  create override (`expiresAt` in (now, now + 14 days], same reason rules; an active override for the place is ended
  first, so at most one is active); end closure/override (409 if already ended); recompute (202, 409 RECOMPUTE_RUNNING
  while a run is in progress). `createdById`/`endedById` = the admin.
- **AC6** — Web admin **Conditions** (sidebar item, admin only): table of places — name, type, status chip (colour +
  icon + label from design tokens, "No data" grey when null), source, "Updated {relative}", closure/override flags;
  status filter; "Recompute now" button (disabled + spinner while 409/running). Row → place panel: current status,
  reasons, forecast time; closures list with "Add closure" form (start, optional end, reason uz/ru/en, source) and
  "End"; override form (status, reason uz/ru/en, expiry, max 14 days) and "End override"; confirm dialog before End.
- **AC7** — App Place: a condition card under the level card — chip + title "{Status} this weekend" (Seasonal lock:
  "Closed for the season · Opens in {Month}"), "Updated {relative} · {source label}", up to 3 reason lines from
  templates (closure/override: the admin text in app locale, fallback uz); Not now adds worried Irbis; `status null`
  → grey "Condition not available yet". A weather card "Weather this weekend": per window day glyph + "{day} {max}° /
  {min}°", then wind and rain chance of the worst day, and "Weather data by Open-Meteo.com". "Hazards now" lists
  each place hazard with its level (Low / Raised / High / Open / Closed); places without hazards keep "Hazards not set
  yet". Light + dark.
- **AC8** — App Explore: each card shows the status chip (colour + icon + label) next to the type line; none when
  null. Offline: Place and Explore show the last cached condition with its "Updated …" age; nothing cached → condition
  card shows offline message + retry. Condition fetch error → card error + retry; the rest of Place still renders.

### QA events (app, dev/staging builds)
- `condition_viewed { slug, status, source, ageMin }` · `explore_loaded` gains `{ withStatus }` (count of cards with a chip)

### testIDs (app)
`place.condition`, `place.condition-status`, `place.condition-updated`, `place.condition-reason.<n>`,
`place.condition-empty`, `place.condition-error`, `place.condition-retry`, `place.weather`, `place.weather-day.<sat|sun>`,
`place.hazard.<hazard>`, `explore.card.<slug>.status`.

### Required UI states (every touched client)
- [ ] Loading (condition card + weather skeleton; admin table skeleton)
- [ ] Empty (status null; admin: no places for filter)
- [ ] Error (message + retry) — app condition card, admin table/panel and every form action
- [ ] Offline (app: cached condition with age, else offline message + retry)
- [ ] App: safe areas, press states, ru/uz copy wraps; web: keyboard + focus, form validation messages
- [ ] Design tokens (`design.md` § Condition status) and shared primitives only; light + dark

## Media
From `design/media/conditions/MEDIA.md` (Q8): canvas status icons and worried Irbis are **final**; weather glyphs
(sun, cloud, rain, storm, wind, snow) are **placeholders** — STATUS known issue until the owner drops files in
`design/media/conditions/`.

## Waivers
- none

## Out of scope
- Community condition reports (submit, list, "See all", feeding status) → `conditions-reports`
- Home path rings, Smart swap, weather shield → `weekly-path` · push notifications on status change
- Threshold editor in admin (config stays server-side) · per-user status by level (level card covers it)
- Community ratings, trails, safety tips, badges, verification, Start adventure / "Go there" button
- Status on map pins (cards only)

## Assumptions
- Q1 (owner, 2026-10-18): scope = api engine + app (Place, Explore cards) + web admin closures/overrides; community
  reports split to `conditions-reports`; Home rings come with `weekly-path`.
- Q2 (owner, 2026-10-18): Open-Meteo (no key) + `@nestjs/schedule` (package approved); ADR-004. Free tier is
  non-commercial — paid plan before launch (open question).
- Q3 (owner, 2026-10-18): window = coming weekend (Tashkent), thresholds as AC2, all in server config, to be tuned.
- Q4 (owner, 2026-10-18): override > closure > season > weather; status per place, same for every user; stale (> 6 h)
  keeps the last status with its age.
- Q5 (owner, 2026-10-18): hazard rules + "Hazards now" levels as AC2; road only via closures.
- Q6 (owner, 2026-10-18): admin = closures + overrides (expiry ≤ 14 days) + recompute; changes audited by the
  created/ended columns.
- Q7 (owner, 2026-10-18): reason text = client templates from reason codes; closures/overrides show admin text.
- Q8 (owner, 2026-10-18): canvas status icons + worried Irbis final; weather glyphs placeholder.

- Q9 (owner, 2026-10-18): the places Explore test's expected `explore_loaded` event gains `withStatus: 0` (app
  92887f9); no other change to that test.
- Impl (2026-10-18, app 92887f9): condition components live in `src/shared/components/conditions/` (no
  feature→feature imports), hook in `features/places/hooks/usePlaceCondition.ts`; reason testIDs count from 1;
  extra testIDs `place.condition-offline`, `-skeleton`, `-title`, `-mascot`, `place.weather-summary`, `place.hazard.<h>.level`.
- Impl (2026-10-18, api 2e52ef3): `conditionStatus` is omitted from list items of places with no condition row
  (optional field) so the existing places e2e `toEqual` stays untouched — clients treat absent as null. The cron is
  registered but no-ops when `CONDITIONS_JOB_ENABLED=false`. 401 code is the repo's `UNAUTHENTICATED`.

## Open questions
- Open-Meteo commercial plan before production launch (owner).
