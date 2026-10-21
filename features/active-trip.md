# active-trip

- Status: Approved
- Surfaces: api | app | web (one public page only)
- Related ADRs: ADR-001 (log-in for trips; SOS never needs an account), ADR-003 (api style), ADR-004 (jobs)
- Requirements: Product Overview § Core loop step 4 (Active trip), § Safety (Active trip, SOS), § XP (Waypoint 10) ·
  Screens: `design/canvas/ActiveTrip.dc.html` (+ canvas note `n_active`) · builds on `features/trip-plan.md`

## Goal
While a trip is active the user sees live distance, climb and time on a map, logs free waypoint check-ins (+10 XP),
can send an SOS with a 3 s hold, shares a public live link with their contact, and ends with "Check out safely" and a
trip summary.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| POST | `/v1/trips/{id}/locations` | owner | lat, lng, accuracyM, recordedAt, distanceM, climbM | 204 | 404 TRIP_NOT_FOUND, 409 TRIP_NOT_ACTIVE, 400 |
| POST | `/v1/trips/{id}/waypoints` | owner | lat, lng, accuracyM, recordedAt | `WaypointResultDto` (waypoint {n, lat, lng, recordedAt}, xpAwarded) | 404, 409 TRIP_NOT_ACTIVE, 409 WAYPOINT_LIMIT, 422 WAYPOINT_TOO_CLOSE, 422 WAYPOINT_TOO_SOON, 422 LOCATION_INACCURATE |
| POST | `/v1/trips/{id}/sos` | owner | lat?, lng?, accuracyM? | `SosResultDto` (sentAt, contactName, sosCallNumber) | 404, 409 TRIP_NOT_ACTIVE, 429 SOS_TOO_SOON, 502 SOS_SEND_FAILED |
| GET | `/v1/trips/{id}/sos-contact` | owner | — | `{ phone, sosCallNumber }` (full, owner's own contact) | 404, 409 TRIP_NOT_ACTIVE |
| POST | `/v1/trips/{id}/check-out` (changed) | owner | optional distanceM, climbM | `TripDto` | as before |
| GET | `/v1/live/{token}` | **@Public**, throttled 30/min/IP | — | `LiveTripDto` | 404 LIVE_NOT_FOUND |

`TripDto` gains: liveUrl? (active / checked_out / alerted), lastLocationAt?, distanceM, climbM, waypoints[] {n, lat, lng, recordedAt}.
`LiveTripDto`: displayName (username), placeName (all locales), backBy, status (`on_trip|late|alerted|back_safe|ended`),
lastLocationAt?, mapsUrl? (only while not ended). Never the contact, phone or user id.

## Data model changes
Migration `active_trip`:
- `Trip` + liveToken (char 22, base64url of 16 random bytes, unique, set at Start), lastLat?, lastLng?, lastAccuracyM?,
  lastLocationAt?, distanceM Int default 0, climbM Int default 0.
- `TripWaypoint`: id uuid7, tripId FK cascade, n (1…), lat, lng, accuracyM, recordedAt, xpAwarded Int, createdAt; unique (tripId, n).
- `TripSos`: id uuid7, tripId FK cascade, lat?, lng?, sentAt, status (`sent|failed`).
- GameConfig `trip.active` = `{ pingEveryMin: 5, waypoint: { xp: 10, minDistanceM: 500, minGapMin: 10, maxPerTrip: 5,
  maxAccuracyM: 50 }, sosCooldownSec: 60, liveAfterCheckoutH: 2 }` (zod).

## Acceptance criteria
- **AC1** — ActiveTrip screen opens after "Start adventure" and when the Home active-trip card is tapped. Top card:
  status "LIVE · On track" (before back-by), "Running late" (after back-by), "Contact alerted" (alert sent); "Back by
  17:30"; three stats km (1 decimal) / "+310 m climbed" / elapsed h:mm since startedAt (ticks each minute). Below a
  MapLibre map: the recorded route line, waypoint pins (✓) and the "You are here" dot. Guests never reach it (trips need an account).
- **AC2** — Tracking (foreground only): `watchPosition` while the app is in the foreground, distanceFilter 10 m. Fixes
  with accuracy > 50 m are dropped. Distance = sum of haversine between accepted fixes; climb = sum of altitude gains
  ≥ 3 m since the last counted altitude. Route points + stats are stored on the device per trip and survive an app
  restart. Location denied → stats show "—", a "Turn on location" row opens Settings, the trip continues.
- **AC3** — Pings: every 5 min (config) while foreground and online the app POSTs the latest fix + distanceM/climbM;
  offline → the latest one is sent on reconnect (no backlog). Server keeps the last location on the trip. Contact row:
  "{name} is following · last location sent {n} min ago" ("not sent yet" before the first). The auto-alert SMS link
  and the SOS link use last ping → start fix → place coords.
- **AC4** — Live link: a token is created at Start; `TripDto.liveUrl` = `{WEB_PUBLIC_URL}/t/{token}`. The share icon
  on the contact row opens the native share sheet with "Follow my trip to {place}, back by {time}: {liveUrl}".
  Trips started before this feature get a token on their next `GET /v1/trips/current`.
- **AC5** — Public page irbis-web `/t/{token}` (no login, own layout, en/ru/uz from `Accept-Language`, default en):
  username, place, back-by, status chip (On trip / Running late / Contact alerted / Back safe), "Last location {n}
  min ago" and "Open in Maps". Refreshes every 60 s. After check-out: "Back safe" for 2 h, then "This trip has ended"
  with no location. Unknown token → "Link not found". Loading / error + retry states. `noindex`.
- **AC6** — Waypoint check-in (free): "Check in at waypoint" takes one fix (accuracy ≤ 50 m, timeout 10 s). Rules
  (server, config): ≥ 500 m from every earlier waypoint of the trip, ≥ 10 min after the previous one, max 5 per trip,
  trip active; +10 XP via `LevelsService.award` (source `waypoint`, refId = waypoint id). Sheet: "Next: Waypoint {n}"
  · "Check in to log your route and earn +10 XP"; after 5: "All 5 waypoints logged", button disabled. On success
  the ring fills and a "+10 XP" chip floats up (after the server answer, never optimistic). Too close / too soon /
  inaccurate → inline message with the number (e.g. "Walk 320 m more"). Offline → queued with recordedAt, label
  "Saved — syncs when online"; sent on reconnect (server checks recordedAt between startedAt and now).
- **AC7** — SOS: red button, press and hold 3 s with a radial ring (released early = cancelled, nothing sent; haptic at
  start and at send). Then: online → POST `sos` → server sends one SMS through `SmsSender` to the trip's contact in
  the user's locale: "SOS from {name} near {place}. Location: {maps link}. Live: {liveUrl} — Irbis"; offline or
  error → the phone's SMS app opens with that text to the contact's number (fetched via `sos-contact` when the
  screen opens, kept on the device until check-out). Red sheet: "SOS sent to {name}" (or "Tap Send in your SMS
  app"), "Call for help" showing the rescue number from api config `SOS_CALL_NUMBER` (returned by `sos-contact` and
  `sos`; opens the dialer, never automatic; not 112), "Close". Next SOS after 60 s (429). Trip status unchanged.
- **AC8** — Check out: "Check out safely" → confirm sheet → `check-out` with final distanceM/climbM → TripSummary
  screen: distance, climb, time, waypoints logged, XP earned, "Welcome back!" (haptic) and "Done" → Path. Offline →
  button disabled with "You're offline". The Home card's "I'm back safe" (trip-plan AC7) keeps working.

### QA events (app, dev/staging builds)
- `active_trip_open { tripId }` · `trip_ping_sent { tripId, queued }` · `trip_live_shared { tripId }`
- `waypoint_checked_in { tripId, n, xp, queued }` · `waypoint_rejected { tripId, code }`
- `sos_hold_cancelled {}` · `sos_sent { tripId, via: server|sms_app }` · `trip_checked_out { tripId, late }` (existing, + `from: active|card`)

### testIDs (app) · (web)
`active.status` `active.backby` `active.distance` `active.climb` `active.elapsed` `active.map` `active.location-off` ·
`active.contact` `active.contact.last-sent` `active.share-live` · `active.waypoint.next` `active.waypoint.checkin`
`active.waypoint.msg` `active.waypoint.xp` · `active.sos` `active.sos.ring` `sos.sheet` `sos.call` `sos.close` ·
`active.checkout` `active.checkout.confirm` · `summary.distance` `summary.climb` `summary.time` `summary.waypoints`
`summary.xp` `summary.done` · web: `live.status` `live.place` `live.backby` `live.last` `live.maps` `live.notfound` `live.ended`

### Required UI states (every touched client)
- [ ] Loading (skeleton for top card) · Error + retry (trip load) · Empty (no fix yet: "Finding you…")
- [ ] Offline: banner; pings + waypoints queue; SOS falls back to the SMS app; check-out disabled
- [ ] Permissions denied: location → "—" stats + Settings row; SOS still works (place coords)
- [ ] Safe areas, haptics (SOS, waypoint, check-out), press states, tokens + shared components, a11y label on SOS
- [ ] Web page: loading / not found / ended / error + retry, keyboard + labels, one axe check

## Media
`design/media/active-trip/MEDIA.md`: fox companion final; map, pins, SOS ring, +10 XP chip drawn (Reanimated +
MapLibre layers); icons from shared `Icon` (generic fallback OK).

## Waivers
- none

## Out of scope
- Background tracking (screen off) · named / admin-defined waypoints, trail routes, "off track" detection
- Map on the public page · auto-call (no automatic dialing) · SOS hold on/off switch, multiple contacts, Test SOS (`safety-center`)
- SOS without an active trip / without an account (`safety-center`) · Summit celebration (`check-in`)
- Real SMS provider (fake `SmsSender`, STATUS known issue) · push notifications · keep-screen-awake

## Assumptions
- Q1 (owner, 2026-10-21): waypoints are free check-ins — ≥ 500 m and ≥ 10 min apart, max 5 per trip, +10 XP each.
- Q2 (owner, 2026-10-21): SOS → server SMS via fake `SmsSender` online; offline/failure → phone SMS app pre-filled; then a call button (see Q5).
- Q3 (owner, 2026-10-21): tracking foreground only with the installed geolocation package; >50 m accuracy dropped, climb ≥ 3 m.
- Q4 (owner, 2026-10-21): contact follows via a public live link (web page) on top of 5-min server pings.
- Claude default (owner approved 2026-10-21): live page in irbis-web `/t/{token}`, no map, 60 s refresh.
- Claude default: link from Start until check-out + 2 h ("Back safe"), then "This trip has ended"; shared from ActiveTrip.
- Claude default: check-out = confirm sheet + TripSummary screen; Summit stays in `check-in`.
- Claude default: SOS sheet with a call button + Close, 60 s cooldown, hold always 3 s; auto-alert SMS text unchanged.
- Q5 (owner, 2026-10-21): the SOS call button dials the owner-given rescue number, not 112. The value lives only in
  irbis-api `.env` as `SOS_CALL_NUMBER` (E.164, zod-validated; owner fills it); no number in code, seeds or docs.
- Claude: offline SOS needs the full contact number on the device — owner-only `sos-contact` endpoint, cached until check-out.

## Open questions
- Confirm before launch that the `SOS_CALL_NUMBER` line is staffed 24/7 (it replaces 112 on the SOS sheet).
- Public page host: needs `WEB_PUBLIC_URL` (api config) and the web app deployed where contacts can reach it.
