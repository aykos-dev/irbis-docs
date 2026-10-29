# Brief check-in-3-irbis-app — Check in button, offline queue, Summit

- Spec: features/check-in.md · ACs: AC4, AC5, AC7 (signed-in users; guests are brief 4)
- Repo / branch: irbis-app · `feat/check-in` (create from `fix/open-bugs-1029`; leave the uncommitted owner files
  `scripts/serve-apk.js`, `env/`, `src/features/campfire-core/games/packs/*.json` alone — never stage them)
- Depends on: check-in-1/2-irbis-api (run `npm run gen:api` first)

## Files
- Touch: `src/features/check-in/` (new: `checkInQueue.ts`, hooks `useCheckIn`, `useCheckInSync`, components
  `CheckInButton`, screens `SummitScreen`) · `src/app/navigation/` (Summit route, wire the button into Place and
  ActiveTrip through props from the app layer — features never import each other) · i18n en/ru/uz `checkin.*`
- Read for patterns: `src/features/active-trip/waypointQueue.ts`, `hooks/useWaypointCheckIn.ts` (fix, accuracy,
  queue, sync), `src/features/trip-plan/hooks/useStartLocation.ts` (permission flow), `src/features/levels/` LevelUp
  navigation, campfire `Confetti` (mafia GameOver) for confetti, `shared/components` Sheet/AppButton/Screen

## Behaviour
- AC4 — `CheckInButton` (testID `checkin.button`, label "Check in") on the Place screen and the active trip screen.
  Tap → locating state → one fix (accuracy ≤ 50 m, 10 s timeout; permission denied → explain + Settings). Fix
  distance (haversine) > place `checkInRadiusM` → inline `checkin.too-far` "You're {distance} away — get within
  {radius} to check in." (km with 1 decimal ≥ 1000 m) and nothing stored. Else build `{ clientId uuid, placeId,
  lat, lng, accuracyM, recordedAt }`.
- AC5 — Online: send `useCheckInsCreate`; 201/200 → haptics.success, navigate Summit with the result. Offline or
  network/5xx: store in `checkIn.queue` (MMKV via shared storage, max 20, oldest dropped) and open Summit queued
  (`summit.queued` "Checked in · XP arrives when you're online"). `useCheckInSync` (mounted in the app shell)
  sends the queue in order on start, foreground and reconnect; 422/404 → drop + one toast ("This check-in couldn't
  be verified"); network/5xx → keep; after a send invalidate `/v1/me`, `/v1/me/level`, `/v1/path`.
- AC7 — `SummitScreen` (`summit.screen`): Confetti 1.2 s; companion art of the user's level (fox summit asset,
  panda summit asset if present, else the companion's neutral image); `summit.title` peak → "Summit reached!",
  other types → "You made it!"; place name · elevation "1,940 m"; tile `summit.xp` "+{xp} XP earned" if counted,
  "Already counted this month" if not, hidden when queued; Share (`summit.share`, RN Share: "I checked in at
  {place} on Irbis!"), Continue (`summit.continue`, goBack). If `levelUps` non-empty, go to LevelUp, then Summit.
- QA events: `check_in_sent { placeId, counted, xp, queued }`, `check_in_queued { placeId }`,
  `check_in_rejected { code }`. ru/uz copy: write natural text.

## Done when
- [ ] tests: too far, online counted → Summit XP, repeat → "Already counted", offline → queued + later sync sends,
  422 on sync drops with toast, peak vs lake title
- [ ] `npm run check` green; commits on `feat/check-in`, no push
