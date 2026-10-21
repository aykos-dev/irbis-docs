# Brief active-trip-1-irbis-app — ActiveTrip screen, tracking, pings, live share, check-out + summary

- Spec: features/active-trip.md · ACs in this brief: AC1, AC2, AC3, AC4, AC8
- Repo / branch: irbis-app · `feat/active-trip` — create from `feat/trip-plan` (trip-plan is not on main yet)
- Depends on: api briefs 1 + 2 committed on irbis-api `feat/active-trip` → run `npm run gen:api` first

## Files
- Touch: new `src/features/active-trip/` (screens `ActiveTripScreen.tsx`, `TripSummaryScreen.tsx`; components
  `StatsCard`, `ContactRow`, `TripMap`, `CheckoutSheet`; hooks `useTripTracking`, `useTripPings`; `trackStore.ts`)
  · `src/app/navigation/RootNavigator.tsx` + `types.ts` (routes `ActiveTrip { tripId }`, `TripSummary { tripId }`)
  · `src/features/trip-plan/` only to navigate: after Start → `ActiveTrip`; Home `TripCard` tap (active) → `ActiveTrip`
  · i18n `src/shared/i18n/{en,ru,uz}/active.json`
- Read for patterns: `src/features/trip-plan/hooks/useStartLocation.ts` (geolocation), `TripCard.tsx`,
  `useTripCardActions.ts` (check-out + toast), the places map (`grep -rl maplibre src/features/places`),
  `src/shared/storage/index.ts`, `shared/hooks/useAppState.ts`, `useNetworkStatus.ts`
- Copy: `irbis-docs/features/briefs/active-trip-copy.md` → `active.*` (all keys except `waypoint.*`, `sos.*`)

## Behaviour
- AC1 — Screen: full-bleed MapLibre map (route LineString from stored points, ✓ pins for `trip.waypoints`, user dot)
  + top card: status (`status.onTrack` before backBy, `status.late` after, `status.alerted` when status=alerted),
  `backBy`, stats km 1 decimal / `+{climb}` m / elapsed h:mm from startedAt (re-render each minute). Bottom sheet
  with the fox companion and the actions; slice 2 fills the waypoint + SOS parts — leave clear slots, no stubs/TODOs.
  Loading skeleton, error + retry, offline banner. Trip from `GET /v1/trips/current` (`active`); none → back to Path.
- AC2 — `useTripTracking`: `Geolocation.watchPosition` (distanceFilter 10, high accuracy) only while AppState is
  active and the screen is mounted; stop on background. Drop fixes with accuracy > 50 m. distance += haversine(prev,
  fix); climb: keep `anchorAlt`; if alt − anchor ≥ 3 → climb += diff, anchor = alt; if alt < anchor → anchor = alt.
  Persist {points (cap 5 000, drop every 2nd when full), distanceM, climbM, anchorAlt, last fix} per tripId in
  `trackStore` (shared storage) — restored after restart, cleared after check-out. Permission denied → stats "—" +
  `active.location-off` row (`locationOff` + `Linking.openSettings()`); no fix yet → `findingYou`.
- AC3 — `useTripPings`: every `trip.pingEveryMin` min (from TripDto) while foreground + online, POST
  `/locations` with the latest fix + rounded distanceM/climbM; offline → send the latest once on reconnect (no backlog).
  Contact row `active.contact`: avatar initial + `contact.following|justNow|notYet` from `lastLocationAt`
  (server value, updated after a ping succeeds; < 1 min = justNow).
- AC4 — `active.share-live` icon on the contact row → `Share.share` with `shareText` ({place} locale name, {time},
  {url}=trip.liveUrl). Hidden if liveUrl missing.
- AC8 — `active.checkout` ("Check out safely", white button) → `CheckoutSheet` (`confirmTitle`/`confirmBody`
  with contact name, `confirm`/`cancel`) → existing check-out hook with {distanceM, climbM} → success haptic →
  `TripSummary` (replace): distance, climb, time (startedAt→checkedOutAt), waypoints count, XP = sum of waypoint
  xpAwarded known on device (from TripDto.waypoints / slice 2 results; 0 now), `summary.title`, `summary.done` →
  Path tab. Offline → button disabled + `offline` label. Home card "I'm back safe" unchanged.

## API (generated hooks — names after gen:api)
`useTripsGetCurrent` · `useTripsPostLocation` · `useTripsCheckOut` (with body). Don't hand-write fetch/types.

## testIDs · QA events
`active.status` `active.backby` `active.distance` `active.climb` `active.elapsed` `active.map` `active.location-off`
`active.contact` `active.contact.last-sent` `active.share-live` `active.checkout` `active.checkout.confirm`
`summary.distance` `summary.climb` `summary.time` `summary.waypoints` `summary.xp` `summary.done`
· `active_trip_open { tripId }` `trip_ping_sent { tripId, queued }` `trip_live_shared { tripId }`
`trip_checked_out { tripId, late, from: 'active' }` (card keeps its existing event; add `from: 'card'`)

## Approved packages
none (geolocation + maplibre are installed)

## Done when
- [ ] tests: distance/climb math + accuracy drop (unit), restore after remount, ping timer + offline-once,
  status lines, share text, check-out → summary; `npm run check` green; commit on `feat/active-trip`
