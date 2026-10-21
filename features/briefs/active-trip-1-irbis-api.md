# Brief active-trip-1-irbis-api — pings, live link, public live endpoint, check-out stats

- Spec: features/active-trip.md · ACs in this brief: AC3, AC4, AC5 (api side), AC8 (api side)
- Repo / branch: irbis-api · `feat/active-trip` — create from `feat/trip-plan` (trip-plan is not on main yet)
- Depends on: none

## Files
- Touch: `src/features/trip-plan/` (controller, service, repository, errors, dto, trip-alert.sms.ts) — active-trip
  extends the trip domain, no new feature module · new `src/features/trip-plan/live.controller.ts` for the public route
  · `prisma/schema.prisma` + NEW migration `active_trip` · `src/config/` (add `WEB_PUBLIC_URL`, `SOS_CALL_NUMBER`
  for brief 2 too — both zod, `.env.example` gets placeholder lines only: `WEB_PUBLIC_URL=http://localhost:3001`,
  `SOS_CALL_NUMBER=+998XXXXXXXXX`) · GameConfig seed key `trip.active` (schema next to `trip.config`)
- Read for patterns: `trip-plan.service.ts`, `trip-alert.job.ts`, `src/common/` (`@Public()`, `@Throttled()`),
  `src/features/levels/game-config.service.ts`

## Data (migration `active_trip`, never edit old migrations)
- `Trip` + `liveToken` char(22) unique nullable (base64url of `crypto.randomBytes(16)`), `lastLat?` `lastLng?`
  `lastAccuracyM?` `lastLocationAt?`, `distanceM Int @default(0)`, `climbM Int @default(0)`.
- `TripWaypoint` (id uuid7, tripId FK cascade, n, lat, lng, accuracyM, recordedAt, xpAwarded, createdAt; unique tripId+n)
  and `TripSos` (id uuid7, tripId FK cascade, lat?, lng?, sentAt, status enum sent|failed) — create both tables
  here (brief 2 uses them) so there is one migration.
- GameConfig `trip.active` = `{ pingEveryMin: 5, waypoint: { xp: 10, minDistanceM: 500, minGapMin: 10, maxPerTrip: 5,
  maxAccuracyM: 50 }, sosCooldownSec: 60, liveAfterCheckoutH: 2 }`.

## Behaviour
- AC4 — `start` sets `liveToken`. `GET /v1/trips/current` back-fills a token for an active trip without one.
  `TripDto` gains `liveUrl` (`${WEB_PUBLIC_URL}/t/${token}`, for active / alerted / checked_out), `lastLocationAt`,
  `distanceM`, `climbM`, `waypoints[]` {n, lat, lng, recordedAt} (empty until brief 2), `pingEveryMin`.
- AC3 — `POST /v1/trips/{id}/locations` {lat −90..90, lng −180..180, accuracyM 0..5000, recordedAt ISO (not in the
  future by >2 min, not before startedAt), distanceM 0..1 000 000 int, climbM 0..20 000 int} → 204. Only status
  active|alerted; ignore (still 204) a recordedAt older than the stored lastLocationAt. Stores last fix + stats.
  Never log coordinates with the user id. Auto-alert link (`trip-alert.sms.ts`): last ping → start fix → place.
  Existing alert tests must stay unchanged and green; add one test for the ping case.
- AC5 — `GET /v1/live/{token}` `@Public()` + throttle 30/min/IP → `LiveTripDto` {displayName (username),
  placeNames {uz,ru,en}, backBy, status `on_trip|late|alerted|back_safe|ended`, lastLocationAt?, mapsUrl?}.
  late = active and now > backBy; back_safe = checked_out and now < checkedOutAt + 2 h; after that `ended` with no
  lastLocationAt / mapsUrl. Planned trips or unknown token → 404 LIVE_NOT_FOUND. Never contact, phone or ids.
- AC8 — `check-out` accepts optional body {distanceM?, climbM?} (same ranges) and stores them; no body = as today.
- Errors: 409 TRIP_NOT_ACTIVE (new), 404 LIVE_NOT_FOUND (new); others reuse trip-plan errors.

## API
| Method | Path | Request | Response | Errors |
|---|---|---|---|---|
| POST | /v1/trips/{id}/locations | as above | 204 | 404 TRIP_NOT_FOUND, 409 TRIP_NOT_ACTIVE, 400 |
| POST | /v1/trips/{id}/check-out | {distanceM?, climbM?} | TripDto | as before |
| GET | /v1/live/{token} | — | LiveTripDto | 404 LIVE_NOT_FOUND, 429 |
operationIds: `tripsPostLocation`, `liveGet` (check-out keeps its id).

## Copy
none (SMS for SOS is brief 2).

## Approved packages
none

## Done when
- [ ] unit tests: token at start + back-fill, ping ordering, live status (on_trip/late/back_safe/ended), alert link uses ping
- [ ] e2e: locations 204 + 409, live 200 + 404, check-out with stats; `npm run check` green
- [ ] `npm run openapi:export` committed; commit on `feat/active-trip`
