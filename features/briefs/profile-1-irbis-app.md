# Brief profile-1-irbis-app — Profile, public profile, share

- Spec: features/profile.md · ACs in this slice: AC1, AC4
- Repo / branch: irbis-app · `feat/profile` (create from main if missing; slices stack)
- Depends on: profile-1-irbis-api (extended `/v1/me`, public `GET /v1/users/:username`)

## Files
- Touch: `src/features/profile/screens/ProfileScreen.tsx` (new; move the existing auth ProfileScreen here and
  update the tab import), `PublicProfileScreen.tsx` (new), `src/features/profile/components/` (Avatar, ProfileHeader,
  StatsCard, BadgeShowcase, RatingsCard, LeagueChip), `src/features/profile/share.ts`, `SettingsScreen.tsx`
  (temporary `Screen` placeholder replaced by profile-3), `src/shared/components/Icon.tsx` (add `share`,
  `settings`, `bell`, `trophy`, `medal`, `pin`, `camera`), `src/app/navigation/types.ts`
  (`PublicProfile: { username: string }`, `Settings: undefined`), `RootNavigator.tsx`, `linking.ts`
  (`PublicProfile: 'profile/:username'`), `src/shared/api/errors.ts` (`profileNotFound: 'PROFILE_NOT_FOUND'`),
  `src/shared/i18n/{en,ru,uz}/profile.json` + `index.ts`, tests.
- Read for patterns: current `src/features/auth/screens/ProfileScreen.tsx`, `CompanionArt`, `levelMeta`,
  `AppText`, `Screen`, `ErrorState`, `EmptyState`, `ListCard`/`ListRow`, `Icon`, `useAuth`, `useMeLevelGet`,
  `useLocale`, `t`, `ProfileScreen` tests.
- Keep the signed-in language / recovery-phone / sign-out rows and their `profile.language`,
  `profile.recovery-phone`, `profile.sign-out` testIDs **temporarily** so existing auth tests stay green;
  profile-3 moves them to Settings and deletes these rows.

## Behaviour
- AC4 — Header: avatar (photo or initials) with a pressable level ring + `CompanionArt level={user.level}`;
  primary name `displayName ?? username`; meta `@username · <region> · since <MMM yyyy>` (region only if
  `showHomeRegion`); level chip `Level N · <level name>`. Initials = first letters of the first two words of
  `displayName`, else the first two alphanumeric chars of `username`; uppercase.
- Stats card: Peaks / Lakes / Caves = `0`, Walked = `0 km` (or `0 mi` later), Climbed = `0 m` (or `0 ft`),
  Spots found = `0`; note “Stats start with your first check-in.” Do **not** copy the canvas 6/184/4.9/#7.
- Badge showcase: four locked hex tiles with a lock/trophy glyph, note “Badges unlock with check-ins.” No
  “All 23” link. Ratings card: “No buddy ratings yet.” League chip: “Unranked” + “League starts when you join a
  season.” Safety row opens `Safety`; Marketplace row is disabled with “Preview”.
- Share icon opens `Share.share({ message: t('profile.shareMessage', { name, username, link }),
  title: t('profile.share') })` with `link = irbis://profile/<encoded username>`; QA `profile_shared`.
- Settings gear opens the placeholder `Settings` route. Own profile loads from `useAuth().user`; pull-to-refresh
  calls `reloadUser`; `userError` uses `ErrorState` with retry. Keep the guest profile exactly as it is.
- AC4 public — `PublicProfileScreen` reads `route.params.username` (strip a leading `@`), uses
  `useUsersGetProfile`, and renders a back button, the same header/level/bio, home region only when returned,
  stats card only when `showStats`, the same empty badges/ratings/league, and a share icon. `PROFILE_NOT_FOUND`
  shows “This profile is private or doesn’t exist.” with back; other errors show retry. Guests can view it.
  No edit/settings actions. Back falls back to `MainTabs → Profile` when the stack is empty.
- Keep the screen scrollable, safe-area aware, light/dark via tokens; dynamic type wraps ru/uz. Extend `Icon`
  from the canvas paths, never emoji or PNG.

## API (generated hooks)
`useMeGet` (already in auth) · `useUsersGetProfile(username)` · `useMeLevelGet` if the level title needs it.

## Copy (`profile.json`; en / ru / uz)
| key | en | ru | uz |
|---|---|---|---|
| `metaRegion` | `@%{username} · %{region} · since %{date}` | `@%{username} · %{region} · с %{date}` | `@%{username} · %{region} · %{date}dan beri` |
| `metaNoRegion` | `@%{username} · since %{date}` | `@%{username} · с %{date}` | `@%{username} · %{date}dan beri` |
| `level` | `Level %{n} · %{title}` | `Уровень %{n} · %{title}` | `%{n}-daraja · %{title}` |
| `stats.title` | `Stats` | `Статистика` | `Statistika` |
| `stats.peaks` / `lakes` / `caves` | `Peaks` / `Lakes` / `Caves` | `Вершины` / `Озёра` / `Пещеры` | `Cho‘qqilar` / `Ko‘llar` / `G‘orlar` |
| `stats.walked` / `climbed` / `spots` | `Walked` / `Climbed` / `Spots found` | `Пройдено` / `Набор высоты` / `Найдено мест` | `Bosib o‘tilgan` / `Ko‘tarilish` / `Topilgan joylar` |
| `stats.km` / `stats.m` | `%{value} km` / `%{value} m` | `%{value} км` / `%{value} м` | `%{value} km` / `%{value} m` |
| `stats.empty` | `Stats start with your first check-in.` | `Статистика начнётся с первой отметки.` | `Statistika birinchi belgidan boshlanadi.` |
| `badges.title` / `badges.empty` / `badges.locked` | `Badge showcase` / `Badges unlock with check-ins.` / `Locked` | `Витрина значков` / `Значки открываются с отметками.` / `Закрыт` | `Nishonlar vitrinasi` / `Nishonlar belgilar bilan ochiladi.` / `Yopiq` |
| `ratings.title` / `ratings.empty` | `Rated by trip buddies` / `No buddy ratings yet.` | `Оценки попутчиков` / `Пока нет оценок попутчиков.` | `Sayohatdoshlar bahosi` / `Hozircha sayohatdoshlar bahosi yo‘q.` |
| `league.title` / `league.unranked` / `league.note` | `League` / `Unranked` / `League starts when you join a season.` | `Лига` / `Без лиги` / `Лига начнётся, когда вы войдёте в сезон.` | `Liga` / `Ligasiz` / `Liga mavsumga qo‘shilganda boshlanadi.` |
| `safety` / `safetyNote` | `Safety center` / `SOS, offline maps and trip safety` | `Центр безопасности` / `SOS, офлайн-карты и безопасность в поездках` | `Xavfsizlik markazi` / `SOS, oflayn xaritalar va sayohat xavfsizligi` |
| `marketplace` / `marketplace.preview` | `Marketplace` / `Preview` | `Маркетплейс` / `Превью` | `Marketpleys` / `Ko‘rish` |
| `settings` / `share` / `avatar` | `Settings` / `Share profile` / `Profile photo` | `Настройки` / `Поделиться профилем` / `Фото профиля` | `Sozlamalar` / `Profilni ulashish` / `Profil rasmi` |
| `shareMessage` | `Find %{name} on Irbis: @%{username} — %{link}` | `Найдите %{name} в Irbis: @%{username} — %{link}` | `Irbis’da %{name}ni toping: @%{username} — %{link}` |
| `public.private` / `public.privateBody` / `public.error` | `This profile is private or doesn’t exist.` / `Ask the owner to share it publicly.` / `Couldn’t load this profile.` | `Этот профиль закрыт или не существует.` / `Попросите владельца открыть профиль.` / `Не удалось загрузить профиль.` | `Bu profil yopiq yoki mavjud emas.` / `Egasi undan ochiq profilni ulashishni so‘rang.` / `Profilni yuklab bo‘lmadi.` |

`profile.regions.<enum>` in enum order — en: Tashkent city, Tashkent region, Andijan, Bukhara, Fergana, Jizzakh,
Karakalpakstan, Khorezm, Namangan, Navoiy, Kashkadarya, Samarkand, Syrdarya, Surkhandarya, Other · ru: Ташкент
(город), Ташкентская область, Андижанская область, Бухарская область, Ферганская область, Джизакская область,
Каракалпакстан, Хорезмская область, Наманганская область, Навоийская область, Кашкадарьинская область,
Самаркандская область, Сырдарьинская область, Сурхандарьинская область, Другое · uz: Toshkent shahri, Toshkent
viloyati, Andijon viloyati, Buxoro viloyati, Farg‘ona viloyati, Jizzax viloyati, Qoraqalpog‘iston, Xorazm
viloyati, Namangan viloyati, Navoiy viloyati, Qashqadaryo viloyati, Samarqand viloyati, Sirdaryo viloyati,
Surxondaryo viloyati, Boshqa.

## testIDs · QA events
`profile.avatar`, `profile.name`, `profile.username`, `profile.meta`, `profile.level`, `profile.share`,
`profile.settings`, `profile.stats`, `profile.stats-{peaks|lakes|caves|walked|climbed|spots}`, `profile.badges`,
`profile.ratings`, `profile.league`, `profile.safety`, `profile.marketplace`, `profile.loading`, `profile.error`,
`profile.retry`, plus the temporary `profile.language`, `profile.recovery-phone`, `profile.sign-out`;
`public-profile.avatar`, `public-profile.name`, `public-profile.username`, `public-profile.meta`,
`public-profile.bio`, `public-profile.stats`, `public-profile.badges`, `public-profile.ratings`,
`public-profile.league`, `public-profile.share`, `public-profile.private`, `public-profile.retry` ·
`profile_shared` · `public_profile_viewed`.

## Approved packages
none.

## Done when
- [ ] tests: own header/empty stats/badges/rating/league; share message + deep link; public profile 200, private
  404, error/retry; guest profile unchanged; existing auth profile tests still green with temporary rows
- [ ] `npm run check` green (output in summary) · committed on `feat/profile`
