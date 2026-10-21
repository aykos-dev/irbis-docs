# Brief active-trip-2-irbis-api — waypoint check-ins + SOS

- Spec: features/active-trip.md · ACs in this brief: AC6 (api side), AC7 (api side)
- Repo / branch: irbis-api · `feat/active-trip`
- Depends on: brief active-trip-1-irbis-api (tables `TripWaypoint`, `TripSos`, config `trip.active`, env `SOS_CALL_NUMBER`)

## Files
- Touch: `src/features/trip-plan/` (controller, service, repository, errors, dto, new `waypoint.rules.ts`,
  `sos.sms.ts`) · `trip-plan.module.ts` (import LevelsModule if not already)
- Read for patterns: `src/features/levels/levels.service.ts` (`award` input/result), `trip-alert.sms.ts`
  (locale text, maps link), `src/features/auth/` `SmsSender`
- Copy: `irbis-docs/features/briefs/active-trip-copy.md` → `sms.sos` (= `active.sos.smsText` en/ru/uz)

## Behaviour
- AC6 — `POST /v1/trips/{id}/waypoints` {lat, lng, accuracyM, recordedAt}. Trip must be active|alerted (else 409
  TRIP_NOT_ACTIVE). recordedAt between startedAt and now + 2 min (queued offline check-ins arrive late — allowed).
  Rules from config `trip.active.waypoint`, in this order: accuracyM > 50 → 422 LOCATION_INACCURATE; count ≥ 5 → 409
  WAYPOINT_LIMIT; haversine < 500 m from ANY earlier waypoint of the trip → 422 WAYPOINT_TOO_CLOSE with
  `details.remainingM` (int, rounded up); recordedAt < previous recordedAt + 10 min → 422 WAYPOINT_TOO_SOON with
  `details.remainingMin`. (Check how DomainError carries extra fields; add a `details` object if needed.)
  Success: insert TripWaypoint n = count+1 and `LevelsService.award({ userId, source: 'waypoint', refId: waypoint.id,
  amount: 10 })` → `WaypointResultDto` {waypoint {n, lat, lng, recordedAt}, xpAwarded (what award granted, may be
  0 if capped)}. Serialise per trip (row lock or unique (tripId, n) + retry) so two fast taps can't make 2 × n.
  `TripDto.waypoints` now lists them.
- AC7 — `POST /v1/trips/{id}/sos` {lat?, lng?, accuracyM?} → active|alerted only (409). Cooldown: last TripSos
  sentAt within 60 s → 429 SOS_TOO_SOON with `details.retryInSec`. Location = body fix → last ping → start fix →
  place. Send one SMS via `SmsSender.sendText` to the trip's snapshot phone, user's locale, text `sms.sos`:
  "SOS from {name} near {place}. Location: {maps}. Live: {url} — Irbis" (name = username, maps =
  `https://maps.google.com/?q=lat,lng` 5 decimals, url = liveUrl). Store TripSos (status sent|failed). Send failure
  → row `failed`, 502 SOS_SEND_FAILED (the app then opens the phone SMS app). Trip status unchanged.
  Response `SosResultDto` {sentAt, contactName, sosCallNumber}.
- `GET /v1/trips/{id}/sos-contact` (owner, active|alerted) → {phone (full E.164, decrypted from the snapshot),
  sosCallNumber (env `SOS_CALL_NUMBER`)}. `Cache-Control: no-store`. Never log the phone; add any new key to pino redaction.
- The SOS call number comes only from env; never hard-code or seed a value.

## API
| Method | Path | Request | Response | Errors |
|---|---|---|---|---|
| POST | /v1/trips/{id}/waypoints | as above | WaypointResultDto | 404, 409 TRIP_NOT_ACTIVE, 409 WAYPOINT_LIMIT, 422 WAYPOINT_TOO_CLOSE, 422 WAYPOINT_TOO_SOON, 422 LOCATION_INACCURATE |
| POST | /v1/trips/{id}/sos | as above | SosResultDto | 404, 409, 429 SOS_TOO_SOON, 502 SOS_SEND_FAILED |
| GET | /v1/trips/{id}/sos-contact | — | SosContactDto | 404, 409 |
operationIds: `tripsCheckInWaypoint`, `tripsSendSos`, `tripsGetSosContact`.

## Approved packages
none

## Done when
- [ ] unit: each waypoint rule + XP award, SOS cooldown + location fallback + failure path
- [ ] e2e: waypoint 200 + 409 + 422, sos 200 + 429, sos-contact 200 + 404 (other user's trip); `npm run check` green
- [ ] `npm run openapi:export` committed; commit on `feat/active-trip`
