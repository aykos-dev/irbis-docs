# Brief conditions-1-irbis-api — condition engine (forecast job, rules, precedence)

- Spec: features/conditions.md · ACs in this slice: AC1, AC2, AC3
- Repo / branch: irbis-api · `feat/conditions` (create from main)
- Depends on: none (places is on main)
- ADR: `irbis-docs/decisions/ADR-004-jobs-and-weather.md` (job runner + Open-Meteo)

## Files
- Touch: `prisma/schema.prisma` + new migration `conditions_init` (models below) · `src/features/conditions/` (new:
  `conditions.module.ts`, `conditions.service.ts`, `conditions.repository.ts`, `condition.rules.ts` (pure),
  `weekend-window.ts` (pure), `open-meteo.client.ts`, `conditions.job.ts`, `conditions.constants.ts`, specs) ·
  `src/config/config.schema.ts` + `app-config.ts` (new keys, defaults) · `src/app.module.ts` (ScheduleModule + module)
- Read for patterns: `src/features/places/*` (module/service/repository/rules split), `src/features/auth/sms-sender.ts`
  (outbound HTTP + error logging), `src/config/*`, `src/logging.ts`, `test/places.e2e-spec.ts`

## Data model (migration `conditions_init`)
- enums `ConditionStatus { go caution not_now seasonal_lock }`, `ConditionSource { forecast hazard_rule closure season manual }`,
  `ClosureSource { official admin }`
- `PlaceCondition` (`place_conditions`): `placeId` PK/FK→places, `status?`, `source?`, `reasons Json`, `hazardLevels Json`,
  `weekend Json`, `forecastAt?`, `computedAt`; index `status`
- `PlaceForecast` (`place_forecasts`): `placeId` PK/FK, `daily Json`, `fetchedAt`
- `Closure` (`closures`): `id uuid`, `placeId`, `startsAt`, `endsAt?`, `reasonUz`, `reasonRu?`, `reasonEn?`, `source`,
  `createdById` FK users, `createdAt`, `endedAt?`, `endedById?`; index `(placeId, endedAt)`
- `ConditionOverride` (`condition_overrides`): `id uuid`, `placeId`, `status`, `reasonUz/Ru?/En?`, `expiresAt`,
  `createdById`, `createdAt`, `endedAt?`, `endedById?`; index `(placeId, endedAt)`

## Behaviour
- AC1 — Cron `5 * * * *`, timeZone `Asia/Tashkent`; in-process guard: a run while one is running is skipped
  (expose `isRunning()` + `runNow()` for slice 2). Fetch Open-Meteo `GET {OPEN_METEO_BASE_URL}/v1/forecast` with
  comma lists of `latitude`/`longitude` for ≤ 50 places per call, `daily=weather_code,temperature_2m_max,
  temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,snowfall_sum`,
  `timezone=Asia/Tashkent&past_days=3&forecast_days=7&wind_speed_unit=kmh`; `apikey` only if `OPEN_METEO_API_KEY`
  set. Timeout 10 s. Upsert `PlaceForecast` per place. Failed batch: keep old rows, log
  `CONDITIONS_FETCH_FAILED { batch, status }` (no coordinates needed, never secrets); recompute still runs for all.
- AC2 — Pure `condition.rules.ts`. Window from Tashkent date (`weekend-window.ts`): Mon–Fri → next Sat+Sun; Sat →
  Sat+Sun; Sun → Sun. Integers (round). Per day: Not now — `weather_code` ∈ {95,96,99} THUNDERSTORM, gust ≥ 60 GUSTS,
  precip ≥ 20 mm HEAVY_PRECIP; Caution — wind ≥ 35 WIND, precip prob ≥ 60 PRECIP_LIKELY, tMax ≥ 35 HEAT, tMin ≤ −10
  COLD. Place hazards only: mudslide/flood precip ≥ 10 Caution, ≥ 30 Not now (MUDSLIDE_RISK/FLOOD_RISK); avalanche:
  snowfall sum of past 3 days + window days ≥ 10 cm Caution, ≥ 30 Not now (AVALANCHE_RISK, no day); heat ≥ 35
  Caution, ≥ 40 Not now (HEAT). Worst status wins; reasons sorted worst first, max 3, `{code, day?, value?}`.
  hazardLevels for each place hazard: low/raised/high by the same bands; road → `open` (`closed` comes from AC3).
  Nothing → `go` with `GOOD_WEATHER {day: first window day, value: max wind of window}`. Source `hazard_rule` if
  the worst-status reason is a hazard rule else `forecast`. `weekend` = window days mapped to `WeekendDay`.
- AC3 — Precedence in the service: active override (not ended, `expiresAt` > now) → its status, source `manual`,
  reason `{code:'OVERRIDE'}`; else active closure (`startsAt` ≤ now, `endsAt` null or > now, not ended) → `not_now`,
  `closure`, `{code:'CLOSURE'}`, road level `closed`; else current Tashkent month `closed` in `season` → `seasonal_lock`,
  `season`, `opensMonth` = next non-closed month (wrap; all 12 closed → null); else rules. No forecast + none of the
  above → status/source null. Hazard levels and `weekend` are filled from the forecast in every case when present.
  Export `recomputePlace(placeId)` (no refetch) for slice 2.
- Config keys (defaults): `OPEN_METEO_BASE_URL=https://api.open-meteo.com`, `OPEN_METEO_API_KEY` optional,
  `CONDITIONS_FETCH_TIMEOUT_MS=10000`, `CONDITIONS_BATCH_SIZE=50`, `COND_GUST_NOT_NOW_KMH=60`,
  `COND_PRECIP_NOT_NOW_MM=20`, `COND_WIND_CAUTION_KMH=35`, `COND_PRECIP_PROB_CAUTION_PCT=60`, `COND_HEAT_CAUTION_C=35`,
  `COND_HEAT_NOT_NOW_C=40`, `COND_COLD_CAUTION_C=-10`, `COND_RAIN_HAZARD_CAUTION_MM=10`, `COND_RAIN_HAZARD_NOT_NOW_MM=30`,
  `COND_SNOW_CAUTION_CM=10`, `COND_SNOW_NOT_NOW_CM=30`, `COND_STALE_HOURS=6`. Update `.env.example` (no values beyond defaults).

## Tests (1–3 per AC)
- rules: thresholds at boundary (34/35 wind, 59/60 gust), hazard only when place has it, window per weekday
- precedence: override > closure > season > rules; null with no forecast; opensMonth wrap
- client: batch of 50, failure keeps old forecast (mock HTTP at the client boundary only)

## Approved packages
`@nestjs/schedule` (latest stable compatible with Nest 12 — pin exact version)

## Done when
- [ ] tests per AC green, `npm run check` green, committed on `feat/conditions` (no endpoints in this slice)
