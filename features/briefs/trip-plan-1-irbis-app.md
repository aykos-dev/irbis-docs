# Brief trip-plan-1-irbis-app — Place CTA + TripPlan screen (form, contact, gear, save/start)

- Spec: features/trip-plan.md · ACs in this brief: AC1, AC2, AC3, AC4, AC5 (+ AC6 save/start buttons, alert switch, 409)
- Repo / branch: irbis-app · `feat/trip-plan` (create from main)
- Depends on: trip-plan-1 + trip-plan-2 irbis-api (on irbis-api `feat/trip-plan`; run `npm run gen:api` first)

## Files
- Touch: `src/features/trip-plan/` (new: `screens/TripPlanScreen.tsx`, components `WhenPicker`, `TimeRow`,
  `ContactCard` + `ContactSheet`, `GearList`, `AlertSwitch`, hooks, `gearTicks.ts` storage) ·
  `src/features/places/screens/PlaceScreen.tsx` (sticky CTA) · `src/app/navigation/RootNavigator.tsx` + `types.ts`
  (route `TripPlan { placeId; tripId? }`) · `src/shared/i18n/{en,ru,uz}/trip.json` + `src/shared/i18n/index.ts`
- Read for patterns: `src/features/places/` (PlaceScreen, usePlaceCondition, LevelCard) · `src/features/lessons/`
  (a screen with sheet + mutations) · `src/shared/hooks/useRequireAccount.ts` (reason `trip` exists) ·
  `src/shared/storage/index.ts` (MMKV) · `src/shared/components/{Sheet,TextField,AppButton,StatusChip,OfflineBanner}.tsx`
- Copy: `irbis-docs/features/briefs/trip-plan-copy.md` (all keys except `card.*`, `share*`, `locationRationale`, `sms.*`)

## Behaviour
- AC1 — PlaceScreen: sticky bottom `AppButton` "Start adventure" (`place.start-adventure`) unless condition status is
  `not_now` or `seasonal_lock` (check the generated enum names). Wrapped in `useRequireAccount('trip')` → navigate
  TripPlan. TripPlan shows `trip.level-caution` when user level < place.requiredLevel (level from the existing levels hook).
- AC2 — WhenPicker: chips next Sat / next Sun (Asia/Tashkent; today counts if Sat/Sun) + Other → native date picker
  (min today, max +14 days; picked date shown on the chip). Start / Back-by: native time pickers, defaults 07:00 / 17:30;
  Back-by row also lets the user pick a later day (overnight, ≤ 72 h — use server `trip.config` values only via the
  422 error; client checks backBy > start and ≤ 72 h for the inline error `timesInvalid` / `startPast`).
- AC3 — Debounced `getTripPreview` on time change: `trip.sunset` line (sunset + buffer), `sunsetOnly` when buffer is
  null, `trip.after-dark` caution when buffer < 0.
- AC4 — `getEmergencyContact`: 204 → ContactCard shows "Add emergency contact" → ContactSheet (name, relation, phone
  with +998 prefix, zod from generated schema, keyboard-controller) → `putEmergencyContact`. Saved: initial avatar,
  "name · relation", `contactLine` with phoneMasked, Change. No contact → Save/Start disabled + `contactRequired`.
- AC5 — GearList from preview: rows with key-based label/notes, `trip.gear.<key>` Checkbox; `gearCount`; ticks in MMKV
  keyed by a draft id (new plan) or tripId; never block Start.
- AC6 (part) — AlertSwitch (default on) + `alertAt` (backBy + 60 min from server `alertAt` once created; before
  creation compute backBy + 60 for display only) / `alertOff`. Footer: `trip.save` (createTrip start:false → toast
  `saved`, back) and `trip.start` (createTrip start:true → heavy haptic, toast `started`, back to Place). 409
  TRIP_ALREADY_ACTIVE → toast `alreadyActive`. `tripId` param → edit mode (`updateTrip`; start via `startTrip`).
  Offline (`useNetworkStatus`) → OfflineBanner + buttons disabled + `offline`. Place card shows place hero + name.
- `sharedOnStart` footnote; share chips are slice 2 (leave them out here).

## API (generated hooks)
`getTripPreview`, `getEmergencyContact`, `putEmergencyContact`, `createTrip`, `updateTrip`, `startTrip`, `getCurrentTrips`
(invalidate after mutations). Errors branch on `code`.

## testIDs · QA events
Spec § testIDs (`place.*`, `trip.*` except `trip.share.*`). `trip_plan_open { placeId, belowLevel }` ·
`trip_saved { tripId }` · `trip_started { tripId, hasLocation:false }`.

## Approved packages
`@react-native-community/datetimepicker` (latest stable, must support RN 0.88 New Arch; no Expo). Native Android build
not required; tests mock it at the module boundary.

## Done when
- [ ] 1–3 RNTL tests per AC (CTA hidden for not_now; guest gate; invalid times; contact required; gear count; 409),
      `npm run check` green, committed on `feat/trip-plan`
