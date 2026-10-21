# Brief trip-plan-1-irbis-api — data model, emergency contact, preview, create

- Spec: features/trip-plan.md · ACs in this brief: AC2, AC3, AC4, AC5, AC6 (create + one-active rule)
- Repo / branch: irbis-api · `feat/trip-plan` (create from main)
- Depends on: none

## Files
- Touch: `prisma/schema.prisma` + NEW migration `trip_plan` · `src/features/trip-plan/` (new: module, controllers,
  service, repository, errors, dto, `sunset.ts`, `gear.rules.ts`) · `src/app.module.ts` (register) · seed/config for
  GameConfig `trip.config` the same way `path.config` is seeded · `openapi.json` (export)
- Read for patterns: `src/features/weekly-path/` (module, GameConfig zod parse, service spec) ·
  `src/features/levels/game-config.service.ts` · `src/features/auth/phone-cipher.ts` (encrypt phone, never log) ·
  `src/features/conditions/conditions.repository.ts` (reading `PlaceForecast.daily`) · `src/lib/dates.ts`
- Copy: none in this slice (SMS text is slice 2)

## Data model (migration `trip_plan`)
- `EmergencyContact`: userId (PK, FK User cascade), name ≤60, relation ≤30, phone (PhoneCipher ciphertext),
  phoneLast2 char(2), createdAt, updatedAt. Table `emergency_contacts`.
- `enum TripStatus { planned active checked_out alerted }`.
- `Trip` (`trips`): id uuid7, userId FK, placeId FK, status, startAt, backBy, alertEnabled bool, contactName,
  contactRelation, contactPhone (cipher), contactPhoneLast2, startedAt?, startLat?, startLng?, startAccuracyM?,
  checkedOutAt?, alertSentAt?, alertAttempts int default 0, timestamps. CHECK backBy > startAt. Partial UNIQUE (userId)
  WHERE status = 'active' (raw SQL in the migration). Index (status, backBy).
- GameConfig `trip.config` (zod): `{ alertDelayMin: 60, maxDurationH: 72, planAheadDays: 14, startGraceMin: 15,
  gear: { waterLPerHour: 0.5, waterMinL: 1, frostMaxC: 0, sunMinC: 20, headlampWithinMinOfSunset: 60 } }`.

## Behaviour
- AC2 — Times valid when: backBy > startAt; backBy − startAt ≤ maxDurationH; startAt ≥ now − startGraceMin;
  startAt ≤ today(Tashkent) + planAheadDays (end of that day). Else 422 `TRIP_TIMES_INVALID`.
- AC3 — `sunset.ts`: pure NOAA solar formula (lat, lng, date) → UTC instant; no new package, no HTTP. Preview returns
  `sunsetAt` for the backBy's Tashkent date when same day as start, else for the start date; `daylightBufferMin` =
  minutes from backBy to sunset (negative = after dark) only when same day, else null. Unit-test vs a known value
  (Tashkent 41.31,69.28 on 2026-10-10 → ~17:50 local, ±3 min).
- AC4 — GET returns `{ name, relation, phoneMasked: "+998 •• ••• •• 41" }` or 204; PUT upserts (phone `^\+998\d{9}$`).
  Phone never in logs or responses beyond the mask; add the field to pino redaction if a new key name is used.
- AC5 — `gear.rules.ts` pure function (place type, hours, forecast day min/max for the start date or null,
  sunsetAt, backBy, config) → ordered `[{ key, litres?, note?, noteTime? }]`: water (litres = max(min, ceil-to-0.5 of
  hours × perHour)), warmLayer (note `frost` if min ≤ frostMaxC), firstAid, offlineMap; sun if max ≥ sunMinC;
  headlamp (note `sunset` + time) if backBy ≥ sunset − headlampWithinMinOfSunset; waterFilter (note `streams`) for
  lake/trail/camping. No forecast → only water, warmLayer, firstAid, offlineMap (+ headlamp/waterFilter which need no
  forecast). 2–3 unit tests.
- AC6 — POST /v1/trips: needs the user's EmergencyContact (else 422 `EMERGENCY_CONTACT_REQUIRED`), snapshots it,
  `start: true` → status active + startedAt (409 `TRIP_ALREADY_ACTIVE` if one exists — map the unique violation too),
  else planned. GET /v1/trips/current → `{ active, planned[] }` (planned sorted by startAt, only startAt ≥ now − 1 day).
  `TripDto.alertAt` = backBy + alertDelayMin. Another user's trip is never returned.

## API
| Method | Path | Request | Response | Errors (code → status) |
|---|---|---|---|---|
| GET | /v1/places/{id}/trip-preview | query startAt, backBy (ISO) | TripPreviewDto { sunsetAt, daylightBufferMin\|null, gear[] } | PLACE_NOT_FOUND 404, validation 400, TRIP_TIMES_INVALID 422 |
| GET | /v1/me/emergency-contact | — | EmergencyContactDto \| 204 | — |
| PUT | /v1/me/emergency-contact | { name, relation, phone } | EmergencyContactDto | 400 |
| POST | /v1/trips | { placeId, startAt, backBy, alertEnabled, start, location? {lat,lng,accuracyM} (stored only when start) } | TripDto | 404, 409 TRIP_ALREADY_ACTIVE, 422 ×2 |
| GET | /v1/trips/current | — | { active: TripDto\|null, planned: TripDto[] } | — |
All routes need a signed-in user (no `@Public()`), AccountStatusGuard as other user routes. operationIds:
`getTripPreview`, `getEmergencyContact`, `putEmergencyContact`, `createTrip`, `getCurrentTrips`.
TripDto: see spec § API (place {id, slug, nameUz/Ru/En, type, latitude, longitude}).

## Tests
Unit: sunset (1), gear rules (2–3), time validation (2), create one-active (1). e2e `test/trip-plan.e2e-spec.ts`:
contact PUT/GET, preview 200, create 200, 409 second active, 422 no contact. No PII in fixtures (`guest_1`, `+998XXXXXXXXX`-style synthetic e.g. +998900000041).

## Approved packages
none

## Done when
- [ ] tests above, `npm run check` green, `npm run openapi:export` committed, committed on `feat/trip-plan`
