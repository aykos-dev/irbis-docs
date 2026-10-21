# Brief trip-plan-2-irbis-api — start, edit, check-out, delete, auto-alert job

- Spec: features/trip-plan.md · ACs in this brief: AC6 (start + location), AC7 (edit/check-out/delete), AC8
- Repo / branch: irbis-api · `feat/trip-plan` (slice 1 is on it)
- Depends on: trip-plan-1-irbis-api

## Files
- Touch: `src/features/trip-plan/` (controller, service, repository, errors, dto, NEW `trip-alert.job.ts` +
  `trip-alert.sms.ts`) · module wiring for `SmsSender` · `openapi.json`
- Read for patterns: `src/features/conditions/conditions.job.ts` (+ spec: cron in Asia/Tashkent, overlap guard) ·
  `src/features/auth/sms-sender.ts` + `recovery.service.ts` (how SmsSender is injected/called) ·
  `src/features/auth/phone-cipher.ts` (decrypt)
- Copy: `irbis-docs/features/briefs/trip-plan-copy.md` → only the `sms.alert` row (uz/ru/en, server-side constant map)

## Behaviour
- AC6 — POST /trips/{id}/start: planned → active, startedAt = now, optional location {lat −90..90, lng −180..180,
  accuracyM 0..10000} stored. Not planned → 409 `TRIP_NOT_EDITABLE`; another active → 409 `TRIP_ALREADY_ACTIVE`;
  backBy ≤ now → 422 `TRIP_TIMES_INVALID`. Never log coordinates with the user id.
- AC7 — PATCH /trips/{id}: planned → startAt/backBy/alertEnabled (slice-1 time rules). Active → only backBy (must be
  > now, ≤ startAt + maxDurationH) and alertEnabled, and only while alertSentAt is null; alerted/checked_out → 409
  `TRIP_NOT_EDITABLE`. POST /check-out: active or alerted → checked_out + checkedOutAt; else 409. DELETE: planned only
  → 204; else 409. Other user's id → 404 `TRIP_NOT_FOUND`.
- AC8 — `trip-alert.job.ts`: `@Cron('0 * * * * *', { timeZone: 'Asia/Tashkent' })` with in-process overlap guard.
  Select active trips with alertEnabled, alertSentAt null, backBy + alertDelayMin ≤ now, alertAttempts < 5.
  For each: claim with a conditional update (`WHERE id AND status='active' AND alertSentAt IS NULL`) so a restart/
  overlap never sends twice; build text in the user's `locale` from `sms.alert` ({name} = the user's display
  name/username, {place} = place name in that locale with uz fallback, {time} = backBy HH:mm Tashkent, {link} =
  `https://maps.google.com/?q=<lat>,<lng>` from the start fix else place coords, 5 decimals); `SmsSender.send`.
  Success → status alerted + alertSentAt. Failure → alertAttempts + 1, log `{ tripId, attempt }` only (no phone/text),
  retried next minute; after 5 failures stop. Decide claim-then-send vs send-then-mark so that the "never resent"
  rule holds; document the choice in one comment.
- Check-out after alert allowed (AC7). alertEnabled false → never alerted.

## API
| Method | Path | Request | Response | Errors |
|---|---|---|---|---|
| POST | /v1/trips/{id}/start | { location? } | TripDto | 404 TRIP_NOT_FOUND, 409 TRIP_NOT_EDITABLE / TRIP_ALREADY_ACTIVE, 422 TRIP_TIMES_INVALID |
| PATCH | /v1/trips/{id} | { startAt?, backBy?, alertEnabled? } | TripDto | 404, 409, 422 |
| POST | /v1/trips/{id}/check-out | — | TripDto | 404, 409 |
| DELETE | /v1/trips/{id} | — | 204 | 404, 409 |
operationIds: `startTrip`, `updateTrip`, `checkOutTrip`, `deleteTrip`.

## Tests
Unit (job, fake clock + fake SmsSender): sends once at threshold, not before (1); not twice across two ticks/overlap (1);
failure → retry, stop after 5 (1); locale text + link fallback (1). Service: active edit rules (1–2).
e2e: start 200 + 409; check-out 200; delete planned 204 / active 409; patch 422; other user 404.

## Approved packages
none

## Done when
- [ ] tests above, `npm run check` green, `npm run openapi:export` committed, committed on `feat/trip-plan`
