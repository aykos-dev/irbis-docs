# Brief trip-plan-2-irbis-app — share sheet, start location, Home trip card

- Spec: features/trip-plan.md · ACs in this brief: AC6 (share + location fix), AC7
- Repo / branch: irbis-app · `feat/trip-plan` (slice 1 is on it)
- Depends on: trip-plan-1-irbis-app

## Files
- Touch: `src/features/trip-plan/` (components `ShareChips`, `TripCard`, `BackByPicker`, hook `useStartLocation`) ·
  `TripPlanScreen.tsx` (add share chips, pass location to start) · `src/features/weekly-path/screens/PathScreen.tsx`
  (render `TripCard` at the top — import via the app shell slot or a shared export, respecting eslint-boundaries:
  features never import each other; if needed expose the card through `src/app/` composition) ·
  `android/app/src/main/AndroidManifest.xml` (ACCESS_FINE/COARSE_LOCATION if not present) · `ios/*/Info.plist`
  (`NSLocationWhenInUseUsageDescription` = en `locationRationale`) · i18n `trip.json` (card/share keys)
- Read for patterns: slice-1 files · `src/shared/components/Sheet.tsx` (confirm sheet) · `src/features/campfire-core/`
  (how a native permission is requested, if present)
- Copy: `trip-plan-copy.md` keys `card.*`, `share*`, `welcomeBack`, `locationRationale`, `openActive`

## Behaviour
- AC6 — ShareChips Telegram / SMS / Link (`trip.share.*`): RN core `Share.share({ message: shareText })` (same sheet
  for all three; chip just records the channel). QA `trip_shared { channel }`. On Start: request when-in-use location
  once (rationale text on Android), `getCurrentPosition` with 10 s timeout, high accuracy off; send `{lat,lng,accuracyM}`
  to createTrip/startTrip if obtained; denied / timeout / error → start without it, no toast. `trip_started.hasLocation`.
  New plan → `createTrip({ start: true, location })`; saved plan → `startTrip({ location })`. One toast, one haptic.
- AC7 — TripCard (`home.trip-card`) from `getCurrentTrips`: active → place name, `card.backBy`, `home.trip.checkout`
  (checkOutTrip → success haptic + toast `welcomeBack`; QA `trip_checked_out { tripId, late }`, late = now > backBy),
  `home.trip.backby` (only when alertSentAt null) → date/time picker, value must be > now and ≤ start + 72 h →
  updateTrip({ backBy }) (QA `trip_backby_changed`). Alerted → `card.alerted` line, checkout still shown.
  Planned list (`home.trip.planned.<id>`): `card.planned` date + place, Start (startTrip with location as above),
  Edit (→ TripPlan { placeId, tripId }), Delete (confirm Sheet `card.deleteConfirm` → deleteTrip, QA `trip_deleted`).
  Nothing → card not rendered. Guest → not rendered (no request). Offline → cached data, buttons disabled.
  `openActive` link from the slice-1 409 toast navigates to Home.

## API (generated hooks)
`getCurrentTrips`, `startTrip`, `checkOutTrip`, `updateTrip`, `deleteTrip`, `createTrip`.

## testIDs · QA events
`trip.share.telegram|sms|link`, `home.trip-card`, `home.trip.checkout`, `home.trip.backby`, `home.trip.planned.<id>`,
`home.trip.planned.start|edit|delete` · events above.

## Approved packages
`@react-native-community/geolocation` (latest stable, New Arch, bare RN; no Expo). No build required; mock in tests.

## Done when
- [ ] 1–3 RNTL tests per AC (share called with text; start with/without location; check-out; change back-by hidden
      after alert; delete confirm), `npm run check` green, committed on `feat/trip-plan`
