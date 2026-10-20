# Brief lessons-4-irbis-app — completion sync, guest merge, LevelUp line

- Spec: features/lessons.md · ACs in this slice: AC7 (sync + guest), AC8
- Repo / branch: irbis-app · `feat/lessons` · Depends on: lessons-3-irbis-app (committed)

## Files
- Touch: `src/features/lessons/completionsStore.ts` (+ `syncCompletions.ts`, `useCompletionSync.ts`), a lessons guest
  item registered with `registerGuestItem` (like `src/features/onboarding/onboardingStore.ts:76`), app-level hook mount
  (where other app-wide hooks live, e.g. the root navigator / providers), `src/features/levels/screens/LevelUpScreen.tsx`
  (one line), i18n `levels.json` ×3, tests.
- Read: `src/shared/guest/guestStore.ts`, `src/shared/contexts/auth.tsx:123` (merge flow), `useNetworkStatus.ts`,
  generated `useLessonsComplete` (operationId `lessonsComplete`) and the guest-merge model (`lessons.completions`),
  `src/features/levels/` (LevelUp queue, level queries, `levels.table` data), slice-2 `catalogStore.ts`.

## Behaviour
- AC7 (sync) — Signed in: flush every `synced:false` completion with `POST /v1/me/lesson-completions`
  `{ lessonId, completedAt, attempts }`, one at a time, oldest first, when: a lesson completes, the app starts or comes
  to the foreground, the network comes back, and right after log-in / sign-up (after the guest merge).
  - 2xx → mark synced. 400 / 404 → mark synced with `dropped: true` (never retried; log code + requestId, no user data).
  - Network error / 5xx / 401 → keep queued, retry on the next trigger. Never two flushes at once.
  - After ≥ 1 success: invalidate the lessons catalog query and the level queries (`/v1/me/level`, so the LevelUp
    queue sees new levels). QA `lesson_sync { sent, queued }`.
  - Hub "done" keeps showing queued lessons (slice 2 union), so nothing disappears offline.
- AC7 (guest) — Guest item key `lessons` returns `{ completions: [unsynced, ≤ 200 newest] }` or undefined when empty.
  On merge success mark those synced. Completions made by a guest after this phone's one-time merge are still sent by
  the post-log-in flush above (the API is idempotent per lesson).
- AC8 — LevelUpScreen: below the existing unlock line, when the next level (current + 1 ≤ 7) has a lesson gate of kind
  `tier`: "Next: %{tier} lessons count toward Level %{n}" with the tier title from the cached lessons catalog
  (current locale), else "Tier %{key}" wording from `levels.json` (`lessonsTier`; `first-aid` → `lessonsFirstAid`).
  No line for `count` / `all` gates or at Level 7. testID `levelup.nextTier`.

## Copy (`levels.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| levelUp.nextTier | Next: %{tier} lessons count toward Level %{n} | Дальше: уроки «%{tier}» засчитываются для уровня %{n} | Keyingi: «%{tier}» darslari %{n}-darajaga hisoblanadi |

## testIDs · QA events
`levelup.nextTier` · `lesson_sync { sent, queued }`

## Approved packages
none

## Done when
- [ ] tests: queue flush success / 400 drop / network keep; no double flush; guest item payload + mark synced;
  LevelUp line for tier gate, none for count gate / L7. `npm run check` green (paste), committed on `feat/lessons`.
  Don't edit existing tests — report if one must change.
- [ ] Reply ≤ 10 lines.
