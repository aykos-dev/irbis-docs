# Brief active-trip-2-irbis-app — waypoint check-ins + SOS hold

- Spec: features/active-trip.md · ACs in this brief: AC6, AC7
- Repo / branch: irbis-app · `feat/active-trip`
- Depends on: brief active-trip-1-irbis-app (ActiveTrip screen with slots for waypoint + SOS)

## Files
- Touch: `src/features/active-trip/` (components `WaypointPanel`, `XpChip`, `SosButton`, `SosSheet`; hooks
  `useWaypointCheckIn`, `useSos`; `waypointQueue.ts`) · `ActiveTripScreen.tsx` (mount them) · `active.json` ×3
- Read for patterns: slice-1 `useTripTracking` (last fix), `trackStore.ts`, `shared/components/Sheet`, `haptics`
- Copy: `irbis-docs/features/briefs/active-trip-copy.md` → `active.waypoint.*`, `active.sos.*`

## Behaviour
- AC6 — `WaypointPanel` in the bottom sheet: fox + `waypoint.next` (n = waypoints+1) + `waypoint.hint`, orange
  button `waypoint.cta`. Tap → fresh fix (getCurrentPosition, high accuracy, timeout 10 s, accept ≤ 50 m) → POST
  `/waypoints`. 200 → ring fill + `XpChip` "+{xp} XP" floats up (Reanimated, after the answer — never optimistic),
  success haptic, pin added. Errors → `active.waypoint.msg`: WAYPOINT_TOO_CLOSE → `tooClose` {m=details.remainingM},
  WAYPOINT_TOO_SOON → `tooSoon` {min}, LOCATION_INACCURATE / no fix → `inaccurate`, WAYPOINT_LIMIT → allDone.
  After 5 (config maxPerTrip from TripDto if exposed, else from the 409) → `allDone` {max}, button disabled.
  Offline → check the same spacing rules locally against stored waypoints (500 m / 10 min / max 5), enqueue
  {lat,lng,accuracyM,recordedAt} in `waypointQueue` (per trip, storage), show `queued`; on reconnect send in order;
  then show the XP chip. A queued item rejected by the server is dropped with its message.
- AC7 — `SosButton` (red, 76 pt, `sos.label`, caption `sos.hold`, a11y `sos.a11y`): press-in starts a 3 s radial
  ring (Reanimated) + haptic; release before 3 s = cancel (`sos_hold_cancelled`), nothing sent. At 3 s: heavy
  haptic → online: POST `/sos` with the last fix → `SosSheet` `sos.sent` {name}. Offline, 502 or network error →
  open the phone SMS app: `Linking.openURL('sms:' + phone + (ios ? '&' : '?') + 'body=' + encodeURIComponent(text))`
  with `sos.smsText` (maps link from last fix else place coords, liveUrl) → sheet `sos.tapSend`. 429 → toast
  `sos.tooSoon` {sec}. Phone + sosCallNumber: `GET /sos-contact` when the screen opens (online), kept in storage per
  trip, cleared at check-out; never logged, never in qaLog. Sheet: `sos.call` {number} → `Linking.openURL('tel:'+number)`
  (only on tap), `sos.close`. Hidden call button when no number is known. Trip status unchanged.

## API (generated hooks)
`useTripsCheckInWaypoint` · `useTripsSendSos` · `useTripsGetSosContact`

## testIDs · QA events
`active.waypoint.next` `active.waypoint.checkin` `active.waypoint.msg` `active.waypoint.xp` `active.sos`
`active.sos.ring` `sos.sheet` `sos.call` `sos.close` · `waypoint_checked_in { tripId, n, xp, queued }`
`waypoint_rejected { tripId, code }` `sos_hold_cancelled {}` `sos_sent { tripId, via: 'server'|'sms_app' }`

## Approved packages
none

## Done when
- [ ] tests: waypoint success chip, each error message, offline queue + sync; SOS early release cancels, 3 s sends,
  offline → sms URL, call button → tel URL; `npm run check` green; commit on `feat/active-trip`
