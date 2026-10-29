# Brief streaks-2-irbis-api — weather shield

- Spec: features/streaks.md · ACs: AC3
- Repo / branch: irbis-api · `feat/streaks` (stacks on brief 1)
- Depends on: streaks-1-irbis-api (`isWeekShielded` seam)

## Files
- Touch: `src/features/streaks/` · migration `weekend_conditions` · job registration (follow ADR-004 / the
  conditions and auto-alert jobs)
- Read for patterns: `src/features/conditions/` (current status per place, hourly job), weekly-path `PathMonth` /
  `PathNode`, trip-plan trips (planned/active with startAt/backBy)

## Behaviour
- `WeekendCondition` (placeId, date, status; PK (placeId, date)).
- Job at 12:00 Asia/Tashkent every Saturday and Sunday: for every place on any user's path for the current month
  plus every place of a trip whose [startAt, backBy] overlaps that day, upsert today's current condition status.
- `isWeekShielded(userId, monday)`: places = the user's PathNodes for the month of that Saturday + places of the
  user's trips overlapping that Sat or Sun. Shielded when places is non-empty and, for both Saturday and Sunday,
  every place has a WeekendCondition row with status `not_now` or `seasonal_lock`. Missing rows → not shielded.
- `boot.shieldedLastWeek` = last week had no check-in and was shielded.

## Done when
- [ ] unit: all red → shielded; one place go → not; missing Sunday row → not; trip place included
- [ ] e2e/integration: job writes rows; GET /v1/me/streaks keeps boot through a shielded empty week
- [ ] `npm run check` green, openapi exported if changed, commits on `feat/streaks`
