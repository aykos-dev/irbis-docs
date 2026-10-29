# Brief streaks-3-irbis-app — streak chips, sheet, Summit tile, lessons line, Profile row

- Spec: features/streaks.md · ACs: AC6, AC7
- Repo / branch: irbis-app · `feat/streaks` (create from `feat/check-in`; never stage the owner's uncommitted files
  `scripts/serve-apk.js`, `env/`, campfire `packs/*.json`)
- Depends on: streaks-1/2-irbis-api (`npm run gen:api`), check-in-3/4-irbis-app

## Files
- Touch: `src/features/streaks/` (new: `StreakChips`, `StreakSheet`, hook `useStreaks`) · wire into the Path header
  (`weekly-path/screens/PathScreen.tsx` via an app-layer prop, like `tripCard`), Summit (`check-in` via prop),
  Lessons hub, account Profile (`features/auth/screens/ProfileScreen.tsx`) — all through `src/app` props, features
  never import each other · i18n `streaks.*` · `shared/constants/colors.ts` only if a needed colour is missing
- Read for patterns: Path header XP chip, `shared/components` Sheet/Skeleton, existing Irbis mascot images (sleepy,
  sad, excited), flame/boot glyphs in `Icon`

## Behaviour
- Accounts only (real + demo; `status === 'signedIn'`): `useStreaks` = `useMeStreaks`, refetch on foreground and
  invalidated after lesson completion and check-in send.
- Path header: `path.streak.flame` (flame glyph #FF9F1C + count; grey when `atRisk`), `path.streak.boot` (boot
  #8C5A33 + count), `path.streak.shield` blue #1F74C7 badge on the boot when `boot.shieldedLastWeek`. a11y:
  "{n}-day streak", "{n}-week explorer streak[, protected by weather shield]". Loading → skeleton chips; error →
  hide; offline → cached. Tap → `StreakSheet` (`streak.sheet`): counts, "Today: done / not yet", "This week:
  checked in / not yet", `streak.freezes` "{left} of {perMonth} freezes left this month", line "Bad-weather
  weekends never break your explorer streak." Irbis excited (done today and this week), sleepy (atRisk), sad
  (count 0 and previously > 0 is unknown → use sad when flame 0 and boot 0), else neutral. QA `streak_sheet_open {}`,
  `streaks_seen { flame, boot }` once per app session.
- Summit: tile `summit.week-streak` "{n} Week streak" with the boot glyph, after the check-in result (refetch).
- Lessons hub: `lessons.streak-line` "One more 3-minute lesson keeps your {n}-day streak." when `flame.atRisk`.
- Profile (account): `profile.streaks` row with flame + boot counts.
- ru/uz copy: natural text.

## Done when
- [ ] tests: chips render counts + shield, guest sees none, sheet texts + freezes, Summit tile, lessons line only at risk
- [ ] `npm run check` green; commits on `feat/streaks`, no push
