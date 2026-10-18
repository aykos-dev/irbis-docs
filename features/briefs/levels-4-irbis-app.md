# Brief levels-4-irbis-app — LevelUp, Explore locks, QA grant link

- Spec: features/levels.md · ACs in this slice: AC7, AC8
- Repo / branch: irbis-app · `feat/levels`
- Depends on: levels-3-irbis-app (shared `levels/` components, `useMyLevel`, routes)

## Files
- Touch: `src/features/levels/screens/LevelUpScreen.tsx`, `components/EvolutionSequence.tsx` (Reanimated placeholder),
  `hooks/useLevelUpQueue.ts` (watches `useMyLevel` pending + navigates; marks seen), `__tests__/` · root navigator
  (LevelUp as a full-screen modal; mount the queue watcher once in the app shell) · app-start / foreground refetch of
  `/v1/me/level` when logged in (AppState) · `src/assets/svg/levelupHandL3.ts`, `levelupCatchL4.ts` from
  `irbis-docs/design/media/levels/levelup-hand-l3.svg`, `levelup-catch-l4.svg` · backpack: existing
  `backpackPlaceholder.ts` · `src/features/places/components/PlaceCard.tsx` (lock chip) ·
  `src/app/navigation/linking.ts` + `src/features/debug/` (grant link, QA builds only) · `levels.json` ×3 (add keys)
- Read for patterns: `onboarding/components/CompanionReveal.tsx` (Reanimated + haptics), `shared/components/Motion.tsx`,
  linking.ts debug routes (`appConfig.isQaEnabled`), `shared/utils/qaLog.ts`, Explore list → PlaceCard props

## Behaviour
- AC7 — Queue: when logged in and `pendingLevelUps` is non-empty and no LevelUp is open, open LevelUp for the oldest.
  Keep an in-memory set of shown ids so the same id never shows twice in one session (even if `seen` failed — it is
  retried on the next refetch). Screen (`levelup.screen`, bg #0B6F6A, sunburst + 4 confetti from canvas):
  `EvolutionSequence` (`levelup.sequence`) 3 s total — 0–0.8 s old companion glows (scale 1→1.06, white glow),
  0.8–1.8 s backpack arcs from old to new along the dotted curve, 1.8–2.1 s white flash, 2.1–3 s new companion pops
  in (spring) and the old one fades; tap skips to the end only after 1 s (`levelup_skipped { to, atMs }`). L3→L4 uses
  the hand/catch art; other transitions use neutral art (placeholder). Success haptic at the flash. Then: "LEVEL UP!"
  (#FFD95A), title `levelup.title` "You're a {name}", pill "{n} {animal} · {trait}" (number square in level colour),
  card `levelup.unlocked`: "NEWLY UNLOCKED", `maxDifficulty` boots (#FFD95A), "{Unlock} · {count} new places"
  (first letter upper-cased; count 0 → no " · …"). `levelup.share` → RN `Share.share({ message })`;
  `levelup.continue` (#FFC800) → `POST seen`, then the next pending or `goBack()`. Reduce-motion on → skip straight
  to the end state. Events `levelup_shown { from, to }`, `levelup_continue { to }`, `levelup_share { to }`.
- AC8 — Explore: `PlaceCard` gets the viewer level (`useMyLevel` level, guest 1); `requiredLevel > level` → lock
  icon + chip "Level N" in the level colour (`explore.card.<slug>.lock`). Place detail already sends the token via the
  shared axios instance — verify `viewer` changes after login (no code if it already does). QA link
  `irbis://debug/levels/grant?xp=&lessons=&tier=&checkins=&difficulty=&spots=` (all optional ints; `lessons=N` with
  `tier` → N lesson items of that tier, default tier "1"; `checkins=N` with `difficulty`, default 1) → generated grant
  mutation → invalidate `/v1/me/level`, `/v1/me`, place queries; Toast "Granted" / error; `level_grant { xp, lessons,
  checkIns, spots, ok }`. Registered only when `appConfig.isQaEnabled`; logged out → opens the log-in gate.

## Copy (namespace `levels`; ru/uz plurals via `count`)
| key | en | ru | uz |
|---|---|---|---|
| up.eyebrow / up.title | LEVEL UP! / You're a %{name} | НОВЫЙ УРОВЕНЬ! / Вы — %{name} | YANGI DARAJA! / Siz endi — %{name} |
| up.unlocked | NEWLY UNLOCKED | ТЕПЕРЬ ОТКРЫТО | YANGI OCHILDI |
| up.places (plural) | %{unlock} · %{count} new places | %{unlock} · %{count} новое место / новых места / новых мест | %{unlock} · %{count} ta yangi joy |
| up.share / up.continue | Share / Continue | Поделиться / Продолжить | Ulashish / Davom etish |
| up.shareText | I'm now a %{name} on Irbis! | Я теперь %{name} в Irbis! | Men endi Irbis’da — %{name}! |
| up.skipHint (a11y) | Tap to skip | Нажмите, чтобы пропустить | O‘tkazib yuborish uchun bosing |
| lockChip / lockA11y | Level %{n} / Locked — needs Level %{n} | Уровень %{n} / Закрыто — нужен уровень %{n} | %{n}-daraja / Yopiq — %{n}-daraja kerak |
| debug.granted / debug.grantFailed | Granted / Grant failed | Начислено / Не удалось начислить | Berildi / Berib bo‘lmadi |
Name, animal, trait, unlock: the slice-3 keys.

## Approved packages
none (Reanimated, react-native-svg, RN `Share`, existing haptics helper)

## Done when
- [ ] tests: queue opens oldest pending, never twice per session, Continue calls seen then next; sequence skip
  disabled < 1 s; places line hides at 0; PlaceCard lock above level / none at level; grant link parsing
- [ ] `npm run check` green (output in summary), committed on `feat/levels`
