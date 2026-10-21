# trip-plan

- Status: Done
- Surfaces: api | app
- Related ADRs: ADR-001 (auth, log-in for trip plans), ADR-003 (api style), ADR-004 (jobs, Asia/Tashkent cron)
- Requirements: Product Overview § Core loop step 3, § Safety (Trip plan, Auto-alert) · Screens: `design/canvas/TripPlan.dc.html`

## Goal
From a place, a signed-in user plans a trip (date, start, back-by, emergency contact, gear), saves it for later or
starts it, shares it via the phone's share sheet, and checks out when back. If they have not checked out 1 h after
their back-by time, the emergency contact gets one SMS with the last known location.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | `/v1/places/{id}/trip-preview?date=&startAt=&backBy=` | user | query | `TripPreviewDto` (sunsetAt, daylightBufferMin, gear[]) | 404 PLACE_NOT_FOUND, 400 validation |
| GET | `/v1/me/emergency-contact` | user | — | `EmergencyContactDto` (name, relation, phoneMasked) or 204 | — |
| PUT | `/v1/me/emergency-contact` | user | name ≤60, relation ≤30, phone `+998` + 9 digits | `EmergencyContactDto` | 400 validation |
| POST | `/v1/trips` | user | placeId, startAt, backBy, alertEnabled, start (bool) | `TripDto` | 404 PLACE_NOT_FOUND, 409 TRIP_ALREADY_ACTIVE, 422 TRIP_TIMES_INVALID, 422 EMERGENCY_CONTACT_REQUIRED |
| GET | `/v1/trips/current` | user | — | `{ active: TripDto \| null, planned: TripDto[] }` | — |
| PATCH | `/v1/trips/{id}` | owner | startAt?, backBy?, alertEnabled? (planned: all; active: backBy later only) | `TripDto` | 404 TRIP_NOT_FOUND, 409 TRIP_NOT_EDITABLE, 422 TRIP_TIMES_INVALID |
| POST | `/v1/trips/{id}/start` | owner | location? {lat,lng,accuracyM} | `TripDto` | 404, 409 TRIP_ALREADY_ACTIVE, 409 TRIP_NOT_EDITABLE, 422 TRIP_TIMES_INVALID |
| POST | `/v1/trips/{id}/check-out` | owner | — | `TripDto` | 404, 409 TRIP_NOT_EDITABLE |
| DELETE | `/v1/trips/{id}` | owner | — (planned only) | 204 | 404, 409 TRIP_NOT_EDITABLE |

`TripDto`: id, place {id, slug, names, type, lat, lng}, status (`planned|active|checked_out|alerted`), startAt, backBy,
alertAt (backBy + delay), alertEnabled, startedAt?, checkedOutAt?, alertSentAt?, contact {name, relation, phoneMasked}.
Another user's trip id → 404.

## Data model changes
Migration `trip_plan`:
- `EmergencyContact` (1 per user): userId PK/FK, name, relation, phone (field-cipher AES-GCM, never logged), phoneLast2, timestamps.
- `enum TripStatus { planned active checked_out alerted }`.
- `Trip`: id uuid7, userId FK, placeId FK, status, startAt, backBy, alertEnabled, contact snapshot (name, relation,
  phone cipher, phoneLast2), startedAt?, startLat?/startLng?/startAccuracyM?, checkedOutAt?, alertSentAt?, timestamps.
  Partial unique index: one `active` trip per user. Check: backBy > startAt. Index (status, backBy) for the job.
- GameConfig `trip.config` = `{ alertDelayMin: 60, maxDurationH: 72, planAheadDays: 14, gear: { waterLPerHour: 0.5,
  waterMinL: 1, frostMaxC: 0, sunMinC: 20, headlampWithinMinOfSunset: 60 } }` (zod-validated).

## Acceptance criteria
- **AC1** — Place screen shows a sticky "Start adventure" button that opens TripPlan for that place. Hidden when the
  place's condition is Not now or Seasonal lock. If the user's level is below `requiredLevel` the button still works
  and TripPlan shows a caution line "Recommended from Level N" (not a block). Guests tapping it get the log-in sheet
  (reason `trip`); after log-in they land on TripPlan.
- **AC2** — When: chips for the next Sat and next Sun (today counts) + "Other" (native date picker, today … +14 days).
  Start and Back-by are native time pickers (defaults 07:00 / 17:30). Back-by is a date+time: must be after Start and
  ≤ 72 h after it (overnight allowed); Start may not be in the past by more than 15 min. Invalid → inline error, Start /
  Save disabled; server rejects with 422 TRIP_TIMES_INVALID.
- **AC3** — Sunset line: server computes sunset at the place for the back-by date (solar formula, Asia/Tashkent) and
  shows "Sunset 18:21 · that leaves 50 min of daylight buffer". If back-by is after sunset: caution line "You'll be out
  after dark — pack a headlamp". Overnight (back-by on a later day): sunset of the start day, no buffer line.
- **AC4** — Emergency contact: name, relation, phone (+998 and 9 digits). Saved once on the account (encrypted),
  prefilled on every plan, shown as "Malika · sister" and "+998 •• ••• •• 41 · gets an SMS if you're late"; "Change"
  edits it. No contact → Start/Save disabled; server 422 EMERGENCY_CONTACT_REQUIRED. Each trip keeps a snapshot.
- **AC5** — Gear checklist from the server (`trip-preview`): always Water (0.5 L per planned hour, min 1 L, rounded up
  to 0.5 L), Warm layer, First-aid kit, Offline map; Warm layer gets note "Night frost" when forecast min ≤ 0 °C; Sun
  hat & sunscreen when forecast max ≥ 20 °C; Headlamp when back-by is within 60 min of sunset or later; Water filter at
  lake / trail / camping places ("Streams only" note). No forecast for that date → only the always-items. Header shows
  "5 / 7 packed"; ticks are stored on the device per trip (not synced) and never block Start.
- **AC6** — Footer: "Save plan" (status planned, visible in Home trip card) and "Start adventure" (status active).
  Auto-alert switch (default on) with "Malika is alerted at 18:30 (1 h after return time)". Only one active trip:
  starting a second → 409 → "You already have a trip in progress" with a link to it. Share chips Telegram / SMS / Link
  open the native share sheet with the plan text (place, date, start, back-by, alert time) — no server SMS at start.
  On Start the app asks location permission once and sends one fix (timeout 10 s); denied or no fix → trip still starts.
- **AC7** — Home trip card (top of Path): active trip → place, "Back by 17:30", "I'm back safe" (check-out, toast
  "Welcome back!") and "Change return time" (time picker; new back-by must be later than now and ≤ 72 h after start,
  only before the alert has fired). Planned trips → date, place, "Start", "Edit", "Delete" (confirm sheet).
- **AC8** — Auto-alert job (`@nestjs/schedule`, every minute, Asia/Tashkent): each `active` trip with alertEnabled,
  not checked out and now ≥ backBy + 60 min → one SMS to the snapshot phone via `SmsSender`, in the user's locale:
  "{name} planned to be back from {place} by {time} and hasn't checked out. Last location: {maps link}. — Irbis". Link =
  start fix, else place coords (`https://maps.google.com/?q=lat,lng`). Sets status `alerted` + alertSentAt in the same
  write; never resent (idempotent under overlap/restart). Check-out after the alert is still allowed (status
  `checked_out`). SMS failure is logged (no phone) and retried next minute, max 5 tries.

### QA events (app, dev/staging builds)
- `trip_plan_open { placeId, belowLevel }` · `trip_saved { tripId }` · `trip_started { tripId, hasLocation }`
- `trip_shared { channel }` · `trip_checked_out { tripId, late }` · `trip_backby_changed { tripId }` · `trip_deleted { tripId }`

### testIDs (app)
`place.start-adventure` · `trip.date.sat` `trip.date.sun` `trip.date.other` · `trip.start-time` `trip.backby-time` ·
`trip.sunset` `trip.after-dark` `trip.level-caution` · `trip.contact` `trip.contact.change` `trip.contact.name`
`trip.contact.relation` `trip.contact.phone` `trip.contact.save` · `trip.alert-switch` `trip.alert-at` ·
`trip.share.telegram` `trip.share.sms` `trip.share.link` · `trip.gear.count` `trip.gear.<key>` · `trip.save` `trip.start` ·
`home.trip-card` `home.trip.checkout` `home.trip.backby` `home.trip.planned.<id>` `home.trip.planned.start`
`home.trip.planned.edit` `home.trip.planned.delete`

### Required UI states (every touched client)
- [ ] Loading (skeleton for preview + contact) · Empty (no contact → inline form) · Error + retry
- [ ] Offline: TripPlan shows the offline banner, Save/Start disabled with "You're offline"; Home card shows cached trip, check-out disabled offline
- [ ] Permissions denied: location → trip starts without a fix, no error toast
- [ ] Keyboard over contact form; safe areas; haptics on Start/check-out; press states; tokens + shared components

## Media
`design/media/trip-plan/MEDIA.md`: place hero + fox companion exist (final); gear icons from shared `Icon` (generic
check icon placeholder OK where missing).

## Waivers
- none

## Out of scope
- Live location sharing, distance/elevation, waypoints, SOS, full check-out screen (`active-trip`)
- Trails / "Change" trail (no trail data — the card shows the place) · public live link page · server SMS at Start
- Real SMS provider (fake sender until its own ADR) · multiple contacts / Primary (`safety-center`) · push notifications
- Level gate on overnight trips (`levels` conflict stays open)

## Assumptions
- Q1 (owner, 2026-10-21): check-out → minimal "I'm back safe" + change return time in trip-plan; active-trip replaces it later.
- Q2 (owner, 2026-10-21): SMS → existing fake `SmsSender`; real provider later (STATUS known issue).
- Q3 (owner, 2026-10-21): sharing at Start → native share sheet only; no server SMS at Start.
- Q4 (owner, 2026-10-21): alert location → one fix at Start (`@react-native-community/geolocation`), else place coords.
- Q5 (owner, 2026-10-21): gear → server rules from the canvas, thresholds in GameConfig, ticks on device only.
- Q6 (owner, 2026-10-21): pickers → `@react-native-community/datetimepicker`.
- Q7 (owner, 2026-10-21): overnight allowed (back-by ≤ 72 h after start, Claude's cap); level gate not enforced.
- Q8 (owner, 2026-10-21): contact saved encrypted on the account, prefilled; +998 only.
- Q9 (owner, 2026-10-21): Place CTA; level below required = caution only; hidden for Not now / Seasonal lock (product rule).
- Q10 (owner, 2026-10-21): plans can be saved ahead (≤14 days, Claude's cap); one active trip at a time.
- Q11 (owner, 2026-10-21): change return time freely until the alert fires; no reminder.
- Q12 (owner, 2026-10-21): alert SMS in the user's locale, short, once per trip.
- Claude: sunset computed in the api (NOAA solar formula), no new weather call; forecast min/max from `PlaceForecast`.

## Open questions
- Real SMS provider + ADR before launch.
